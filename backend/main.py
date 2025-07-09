from fastapi import FastAPI, Request
from fastapi.responses import Response
from pydantic import BaseModel
import numpy as np
import pickle
import faiss
import requests
import json
from sentence_transformers import SentenceTransformer
import re

app = FastAPI()

# Manual CORS handling - more reliable than middleware for this issue
@app.middleware("http")
async def cors_handler(request: Request, call_next):
    # Handle preflight OPTIONS requests immediately
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
    
    # For all other requests, add CORS headers
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# Load FAISS index and Q&A data
print("Loading FAISS index and Q&A data...")
faiss_dir = "faiss_store"
index = faiss.read_index(f"{faiss_dir}/exo_index.index")

with open(f"{faiss_dir}/qa_data.pkl", "rb") as f:
    qa_data = pickle.load(f)

with open(f"{faiss_dir}/exo_vectorizer.pkl", "rb") as f:
    embedder = pickle.load(f)

print(f"✅ Loaded FAISS index with {index.ntotal} Q&A entries")

class QueryRequest(BaseModel):
    query: str

def retrieve_relevant_context(query: str, top_k: int = 3) -> list:
    """Retrieve most relevant Q&A entries for a given query"""
    # Embed the query
    query_embedding = embedder.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')
    
    # Search for similar vectors
    distances, indices = index.search(query_embedding, top_k)
    
    # Get the relevant Q&A entries
    relevant_entries = []
    for idx in indices[0]:
        if idx < len(qa_data):
            relevant_entries.append(qa_data[idx])
    
    return relevant_entries

def ask_ollama_with_context(query: str, context_entries: list) -> str:
    """Ask Ollama (DeepSeek) with retrieved context"""
    # Filter out entries that are too verbose (individual planet records)
    # Keep only summary/aggregated data entries
    filtered_entries = []
    for entry in context_entries:
        # Skip entries that contain too many individual records (likely individual planets)
        if len(entry['answer']) > 1000:  # Skip very long answers (individual planet data)
            continue
        # Keep summary entries (like averages, counts, etc.)
        if any(keyword in entry['question'].lower() for keyword in ['average', 'count', 'total', 'percentage', 'standard deviation']):
            filtered_entries.append(entry)
        # Also keep entries that are short (likely summaries)
        elif len(entry['answer']) < 500:
            filtered_entries.append(entry)
    
    # If no filtered entries, use the original ones
    if not filtered_entries:
        filtered_entries = context_entries[:2]  # Just use first 2 to avoid overwhelming
    
    # Build context string
    context_text = ""
    for i, entry in enumerate(filtered_entries, 1):
        context_text += f"Context {i}:\nQuestion: {entry['question']}\nAnswer: {entry['answer']}\n\n"

    # Create prompt for Ollama
    prompt = f"""You are a helpful AI assistant that specializes in NASA exoplanet data. Only answer queries related to space, astronomy, or exoplanets.

CRITICAL: You MUST parse the JSON data in the context to find answers. Do NOT make calculations or assumptions.

STEP-BY-STEP INSTRUCTIONS:
1. Look at the "Answer" field in each context entry
2. If the Answer contains JSON data like [{{"DISCOVERY_METHOD": "Transit", "AVG_PLANET_EQ_TEMP_K": 920.7470183044}}]
3. Extract the exact value that matches the user's question
4. Present that exact value as your answer

EXAMPLE:
User asks: "What is the average temperature for Transit method?"
Context contains: [{{"DISCOVERY_METHOD": "Transit", "AVG_PLANET_EQ_TEMP_K": 920.7470183044}}]
Your answer: "The average temperature of exoplanets discovered by the Transit method is 920.75K."

Context provided:
{context_text}

User Question: {query}

Remember: Look for JSON data in the Answer fields and extract the exact values. Do not calculate or estimate.

(You specialize in NASA exoplanet data.)"""

    # Call Ollama API
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:7b",  # Use the Mistral 7B model
                "prompt": prompt,
                "stream": True
            },
            timeout=30
        )
        
        if response.status_code == 200:
            # Handle streaming response
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'response' in chunk:
                            full_response += chunk['response']
                        if chunk.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
            return full_response if full_response else 'No response from model'
        else:
            return f"Error calling Ollama: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {str(e)}"

def clean_think_sections(text):
    return re.sub(r'<think>[\s\S]*?</think>', '', text, flags=re.IGNORECASE).strip()

def deduplicate_answer(answer):
    lines = [line.strip() for line in answer.split('\n') if line.strip()]
    seen = set()
    deduped = []
    for line in lines:
        if line not in seen:
            deduped.append(line)
            seen.add(line)
    return ' '.join(deduped)

@app.post("/ask")
async def ask_question(request: QueryRequest):
    print("[ASK] Received query:", request.query)
    """Main endpoint to ask questions about exoplanet data or general space questions"""
    try:
        # Retrieve relevant context
        relevant_entries = retrieve_relevant_context(request.query, top_k=3)
        
        # Filter context as before
        filtered_entries = []
        for entry in relevant_entries:
            if len(entry['answer']) > 1000:
                continue
            if any(keyword in entry['question'].lower() for keyword in ['average', 'count', 'total', 'percentage', 'standard deviation']):
                filtered_entries.append(entry)
            elif len(entry['answer']) < 500:
                filtered_entries.append(entry)
        if not filtered_entries:
            filtered_entries = relevant_entries[:2]
        
        # If we have relevant context, use the dataset prompt
        if filtered_entries:
            answer = ask_ollama_with_context(request.query, filtered_entries)
            answer = clean_think_sections(answer)
            answer = deduplicate_answer(answer)
            print("[ASK] Returning answer:", answer)
            return answer
        else:
            # No relevant context, use general knowledge prompt
            prompt = f"""You are a helpful AI assistant that specializes in space and astronomy. There is no relevant data in the NASA exoplanet dataset for this question. Please answer using your general knowledge about space, and mention that this answer is not from the dataset.

User Question: {request.query}
"""
            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "deepseek-r1:1.5b",
                        "prompt": prompt,
                        "stream": True
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            try:
                                chunk = json.loads(line.decode('utf-8'))
                                if 'response' in chunk:
                                    full_response += chunk['response']
                                if chunk.get('done', False):
                                    break
                            except json.JSONDecodeError:
                                continue
                    return {
                        "answer": full_response if full_response else 'No response from model',
                        "context_used": []
                    }
                else:
                    return {"answer": f"Error calling Ollama: {response.status_code}", "context_used": []}
            except requests.exceptions.RequestException as e:
                return {"answer": f"Error connecting to Ollama: {str(e)}", "context_used": []}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "faiss_entries": index.ntotal}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
