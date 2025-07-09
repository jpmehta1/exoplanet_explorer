import os
import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Config
DATA_FILE = os.path.join(os.path.dirname(__file__), 'qa_data.json')
FAISS_DIR = os.path.join(os.path.dirname(__file__), 'faiss_store')
EMBED_MODEL = 'all-MiniLM-L6-v2'

# 1. Load Q&A data
print("Loading Q&A data...")
with open(DATA_FILE, 'r') as f:
    qa_entries = json.load(f)

print(f"Loaded {len(qa_entries)} Q&A entries")

# 2. Initialize embedder
print("Initializing sentence transformer...")
embedder = SentenceTransformer(EMBED_MODEL)

# 3. Prepare texts for embedding (combine question and answer)
texts_for_embedding = []
qa_data_for_storage = []

for entry in qa_entries:
    # Combine question and answer for embedding
    combined_text = f"Question: {entry['question']} Answer: {entry['answer']}"
    texts_for_embedding.append(combined_text)
    
    # Store the full entry for retrieval
    qa_data_for_storage.append(entry)

# 4. Create embeddings
print("Creating embeddings...")
embeddings = embedder.encode(texts_for_embedding, show_progress_bar=True)
embeddings = np.array(embeddings).astype('float32')

print(f"Created embeddings with shape: {embeddings.shape}")

# 5. Create FAISS index
print("Creating FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
index.add(embeddings)

print(f"FAISS index created with {index.ntotal} vectors")

# 6. Save everything
print("Saving FAISS index and data...")
os.makedirs(FAISS_DIR, exist_ok=True)

# Save FAISS index
faiss.write_index(index, os.path.join(FAISS_DIR, 'exo_index.index'))

# Save Q&A data for retrieval
with open(os.path.join(FAISS_DIR, 'qa_data.pkl'), 'wb') as f:
    pickle.dump(qa_data_for_storage, f)

# Save embedder for future use
with open(os.path.join(FAISS_DIR, 'exo_vectorizer.pkl'), 'wb') as f:
    pickle.dump(embedder, f)

print("✅ FAISS index and Q&A data saved successfully!")
print(f"Index location: {os.path.join(FAISS_DIR, 'exo_index.index')}")
print(f"Q&A data location: {os.path.join(FAISS_DIR, 'qa_data.pkl')}")
print(f"Embedder location: {os.path.join(FAISS_DIR, 'exo_vectorizer.pkl')}") 