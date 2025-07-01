# faiss_embedder.py

import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load data
knowledge_dir = "converted"
knowledge_texts = []
file_names = []

for file in os.listdir(knowledge_dir):
    if file.endswith(".json"):
        with open(os.path.join(knowledge_dir, file), "r") as f:
            data = f.read()
            knowledge_texts.append(data)
            file_names.append(file)

# Create dense embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")
X = embedder.encode([f"{f} {t}" for f, t in zip(file_names, knowledge_texts)])

# Create FAISS index
dimension = X.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(X).astype("float32"))

# Save index and filenames
os.makedirs("faiss_store", exist_ok=True)
faiss.write_index(index, "faiss_store/exo_index.index")

with open("faiss_store/exo_filenames.pkl", "wb") as f:
    pickle.dump(file_names, f)

print("✅ FAISS index built using SentenceTransformer.")

