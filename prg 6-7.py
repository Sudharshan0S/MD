import faiss
import os
import time
import psutil
import numpy as np
import pandas as pd

from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize

import nltk
#nltk.download('punkt')
nltk.download('punkt_tab')

#Read the document
with open("sample.txt", "r", encoding="utf-8") as f:
    text = f.read().lower()

sentences = [word_tokenize(s) for s in sent_tokenize(text)]

# Train Word2Vec
model = Word2Vec(
    sentences,
    vector_size=50,
    window=5,
    min_count=1,
    workers=4,
    epochs=100
)

# Create document embeddings
embeddings = []

for sentence in sentences:
    vectors = []
    for word in sentence:
        if word in model.wv:
            vectors.append(model.wv[word])

    if len(vectors) > 0:
        embeddings.append(np.mean(vectors, axis=0))

embeddings = np.array(embeddings).astype("float32")
print("Embedding Shape:", embeddings.shape)
dimension = embeddings.shape[1]

def evaluate(index, vectors, name):

    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss
    start = time.perf_counter()
    index.add(vectors)
    index_time = time.perf_counter() - start
    memory_after = process.memory_info().rss
    memory_used = (memory_after - memory_before) / (1024 * 1024)
    return {
        "Index": name,
        "Index Time(s)": round(index_time,5),
        "Memory(MB)": round(memory_used,3),
        "cpu_used": psutil.cpu_percent(interval=0)
    }

# # Flat Index
flat = faiss.IndexFlatL2(dimension)
flat_result = evaluate(flat, embeddings, "Flat")

# IVF index
nlist = 1
quantizer = faiss.IndexFlatL2(dimension)
ivf = faiss.IndexIVFFlat(
            quantizer,
            dimension,
            nlist,
            faiss.METRIC_L2)

ivf.train(embeddings)
ivf_result = evaluate(ivf, embeddings, "IVF")

# HNSW Index
M = 16
hnsw = faiss.IndexHNSWFlat(dimension, M)
hnsw_result = evaluate(hnsw, embeddings, "HNSW")

df = pd.DataFrame([
    flat_result,
    ivf_result,
    hnsw_result
    ])
print(df)

print("\nChanging IVF Parameters\n")

results=[]
for nlist in [2,4,8]:

    quantizer = faiss.IndexFlatL2(dimension)

    index = faiss.IndexIVFFlat(
        quantizer,
        dimension,
        nlist,
        faiss.METRIC_L2)

    index.train(embeddings)
    r = evaluate(index, embeddings,f"IVF nlist={nlist}")
    results.append(r)
df_ivf = pd.DataFrame(results)
print(df_ivf)    







#Program 7

print("------------ Search Begins Here----------\n")

def search_index(index, query_vector, k=2):  # k similar vectors to be retrived
    distances, indices = index.search(query_vector, k)
    return distances, indices

def query_embedding(query, model, dimension):
    words = query.lower().split()
    print(words)
    vectors = []
    for word in words:
        if word in model.wv:
            vectors.append(model.wv[word])

    if len(vectors) == 0:
        return None

    return np.mean(vectors, axis=0).astype("float32").reshape(1, dimension)

query = input("\nEnter search query: ")
query_vector = query_embedding(query, model, dimension)
#print(" The Query Vector is\n")
#print(query_vector)

if query_vector is None:
    print("No valid words found in query.")
    exit()

original_sentences = [ s.strip() for s in text.split(".") if s.strip()]
#print(original_sentences)

print("\n========== FLAT INDEX SEARCH RESULTS==========")

D, I = search_index(flat, query_vector)
for rank, idx in enumerate(I[0]):
    print(f"{rank+1}. {original_sentences[idx]} "
          f"(Distance = {D[0][rank]:.4f})")

print("\n========== IVF INDEX SEARCH RESULTS==========")

D, I = search_index(ivf, query_vector)
for rank, idx in enumerate(I[0]):
    print(f"{rank+1}. {original_sentences[idx]} "
          f"(Distance = {D[0][rank]:.4f})")


# Search using HNSW Index

print("\n========== HNSW INDEX SEARCH RESULTS==========")

D, I = search_index(hnsw, query_vector)
for rank, idx in enumerate(I[0]):
    print(f"{rank+1}. {original_sentences[idx]} "
          f"(Distance = {D[0][rank]:.4f})")
