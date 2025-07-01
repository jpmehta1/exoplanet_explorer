# main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
import google.generativeai as genai
import numpy as np
import pickle
import faiss
from sentence_transformers import SentenceTransformer

app = FastAPI()
genai.configure(api_key="AIzaSyB5N7rOFmxE_MeW4v_FZIzrpeRBSYAMabg") 

model = genai.GenerativeModel("models/gemini-1.5-flash")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index and document mapping
index = faiss.read_index("faiss_store/exo_index.index")
with open("faiss_store/exo_filenames.pkl", "rb") as f:
    documents = pickle.load(f)

# --- Request schema ---
class Question(BaseModel):
    query: str

# --- Core logic ---
def retrieve_context(query, top_k=5):
    query_vector = embedder.encode([query])
    distances, indices = index.search(np.array(query_vector), top_k)
    return "\n".join([documents[i] for i in indices[0]])

def ask_gemini_with_context(query: str, min_chars=50) -> str:
    context = retrieve_context(query)

    # If FAISS context is too weak, try all docs
    if len(context.strip()) < min_chars:
        print("🔁 Using fallback: All knowledge documents")
        context = "\n".join(documents)

    prompt = f"""Use the following exoplanet dataset to answer in **full sentences**:

### Knowledge:
{context}

### Question:
{query}

Only use the information above. If not present, reply with "I don’t know."
"""
    response = model.generate_content(prompt)
    return response.text

# --- API Route ---
@app.post("/ask")
async def ask_question(q: Question):
    answer = ask_gemini_with_context(q.query)
    return {"question": q.query, "answer": answer}

