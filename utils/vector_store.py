from langchain_community.vectorstores import FAISS
import os


def create_vector_store(chunks, embedding_model):
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    os.makedirs("vector_store", exist_ok=True)

    vector_store.save_local("vector_store")

    return vector_store


def load_vector_store(embedding_model):
    vector_store = FAISS.load_local(
        "vector_store",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return vector_store