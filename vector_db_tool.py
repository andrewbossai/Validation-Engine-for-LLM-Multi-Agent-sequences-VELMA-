import faiss
from sentence_transformers import SentenceTransformer

model = None
index = None
sentences = []

def init_vector_db():

    global model
    global index
    global sentences

    with open('vector_sentences.txt', 'r', encoding='utf-8') as file:
        sentences = []
        for line in file:
            if len(line) > 0:
                sentences.append(line)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentence_embeddings = model.encode(sentences).astype('float32')
    dimension = sentence_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(sentence_embeddings)



def use_vector(query):
    if model is None:
        init_vector_db()

    query_embedding = model.encode([query]).astype('float32')

    k = 3
    distances, indices = index.search(query_embedding, k)

    closest_sentences = ""
    for i, idx in enumerate(indices[0]):
        closest_sentences += sentences[idx]

    return f"\nVector Tool Input:{query}\nVector Tool Output: \n{closest_sentences}"

# print(use_vector("Which bird can eat as many as 2,000 ants per day?"))