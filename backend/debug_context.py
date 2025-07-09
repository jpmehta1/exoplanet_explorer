import numpy as np
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Load FAISS index and data
print("Loading FAISS index and data...")
faiss_dir = "faiss_store"
index = faiss.read_index(f"{faiss_dir}/exo_index.index")

with open(f"{faiss_dir}/qa_data.pkl", "rb") as f:
    qa_data = pickle.load(f)

with open(f"{faiss_dir}/exo_vectorizer.pkl", "rb") as f:
    embedder = pickle.load(f)

# Test query
test_query = "What is the average temperature of exoplanets discovered by the transit method?"

# Embed the query
query_embedding = embedder.encode([test_query])
query_embedding = np.array(query_embedding).astype('float32')

# Search for similar vectors
distances, indices = index.search(query_embedding, k=3)

print(f"\n🔍 Query: '{test_query}'")
print(f"\n📊 Top 3 retrieved entries:")

context_entries = []
for i, (idx, distance) in enumerate(zip(indices[0], distances[0])):
    if idx < len(qa_data):
        entry = qa_data[idx]
        context_entries.append(entry)
        print(f"\n{i+1}. Distance: {distance:.4f}")
        print(f"   ID: {entry['id']}")
        print(f"   Question: {entry['question']}")
        print(f"   Answer: {entry['answer']}")
        print(f"   Answer length: {len(entry['answer'])} characters")

# Build the exact context that would be sent to the model
print(f"\n📝 EXACT CONTEXT BEING SENT TO MODEL:")
context_text = ""
for i, entry in enumerate(context_entries, 1):
    context_text += f"Context {i}:\nQuestion: {entry['question']}\nAnswer: {entry['answer']}\n\n"

print(context_text)
print(f"Total context length: {len(context_text)} characters") 