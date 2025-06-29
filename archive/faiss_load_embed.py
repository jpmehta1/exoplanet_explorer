import os
import json
import pickle
import faiss
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: Load JSON knowledge files
knowledge_dir = "converted"
knowledge_texts = []
file_names = []

for file in os.listdir(knowledge_dir):
    if file.endswith(".json"):
        with open(os.path.join(knowledge_dir, file), "r") as f:
            data = f.read()
            knowledge_texts.append(data)
            file_names.append(file)

# Step 2: Convert text to TF-IDF embeddings
vectorizer = TfidfVectorizer(stop_words="english", max_features=2048)
X = vectorizer.fit_transform(knowledge_texts).toarray()

# Step 3: Store vectors in FAISS index
dimension = X.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(X).astype('float32'))

# Save supporting files
os.makedirs("faiss_store", exist_ok=True)
faiss.write_index(index, "faiss_store/exo_index.index")

with open("faiss_store/exo_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("faiss_store/exo_filenames.pkl", "wb") as f:
    pickle.dump(file_names, f)


