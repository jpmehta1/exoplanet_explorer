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

print(f"✅ Loaded FAISS index with {index.ntotal} Q&A entries")

# Test query
test_query = "What is the average temperature of exoplanets discovered by the transit method?"

print(f"\n🔍 Testing query: '{test_query}'")

# Embed the query
query_embedding = embedder.encode([test_query])
query_embedding = np.array(query_embedding).astype('float32')

# Search for similar vectors
distances, indices = index.search(query_embedding, k=10)  # Get top 10 to see more results

print(f"\n📊 Top 10 retrieved entries:")
for i, (idx, distance) in enumerate(zip(indices[0], distances[0])):
    if idx < len(qa_data):
        entry = qa_data[idx]
        print(f"{i+1}. Distance: {distance:.4f}")
        print(f"   ID: {entry['id']}")
        print(f"   Question: {entry['question']}")
        print(f"   Answer preview: {entry['answer'][:100]}...")
        print()

# Look for the specific entry we want
print("🔎 Looking for q2_planets_avg_temp_discovery_method:")
for i, entry in enumerate(qa_data):
    if entry['id'] == 'q2_planets_avg_temp_discovery_method':
        print(f"Found at index {i}")
        print(f"Question: {entry['question']}")
        print(f"Answer: {entry['answer']}")
        break
else:
    print("❌ Entry not found in qa_data!")

# Test embedding similarity directly
print(f"\n🧮 Testing direct embedding similarity...")
target_entry = None
for entry in qa_data:
    if entry['id'] == 'q2_planets_avg_temp_discovery_method':
        target_entry = entry
        break

if target_entry:
    # Create embedding for the target entry
    target_text = f"Question: {target_entry['question']} Answer: {target_entry['answer']}"
    target_embedding = embedder.encode([target_text])
    target_embedding = np.array(target_embedding).astype('float32')
    
    # Calculate cosine similarity
    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity(query_embedding, target_embedding)[0][0]
    print(f"Cosine similarity with target entry: {similarity:.4f}")
    
    # Compare with retrieved entries
    print(f"\nSimilarity with retrieved entries:")
    for i, idx in enumerate(indices[0][:5]):
        if idx < len(qa_data):
            entry = qa_data[idx]
            entry_text = f"Question: {entry['question']} Answer: {entry['answer']}"
            entry_embedding = embedder.encode([entry_text])
            entry_embedding = np.array(entry_embedding).astype('float32')
            entry_similarity = cosine_similarity(query_embedding, entry_embedding)[0][0]
            print(f"{i+1}. {entry['id']}: {entry_similarity:.4f}") 