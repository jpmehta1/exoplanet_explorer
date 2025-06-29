import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import faiss

genai.configure(api_key="AIzaSyB5N7rOFmxE_MeW4v_FZIzrpeRBSYAMabg") 

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("faiss_store/exo_index.index")
with open("faiss_store/exo_filenames.pkl", "rb") as f:
    documents = pickle.load(f)

def retrieve_context(query, top_k=2):
    query_vector = embedder.encode([query])
    distances, indices = index.search(np.array(query_vector), top_k)
    context_chunks = [documents[i] for i in indices[0]]
    return "\n".join(context_chunks)

def ask_gemini_with_context(query):
    context = retrieve_context(query)
    prompt = f"""Use the following exoplanet dataset information to answer the question clearly and in full sentences.

{context}

{query}

Only answer using the data above. If insufficient, say 'I don’t know.'"""

    response = model.generate_content(prompt)
    return response.text
if __name__ == "__main__":
    test_query = "Which detection method is used most frequently?"
    print("Gemini’s Answer:\n", ask_gemini_with_context(test_query))
