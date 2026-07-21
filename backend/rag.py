from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from backend.prompt import prompt

from utils.pdf_loader import load_pdf
from utils.splitter import split_documents
from utils.embeddings import get_embedding_model
from utils.vector_store import create_vector_store, load_vector_store

load_dotenv()


def process_resume(file_path):
    """
    Runs when a resume is uploaded.
    Creates the FAISS vector store.
    """

    documents = load_pdf(file_path)

    chunks = split_documents(documents)

    embedding_model = get_embedding_model()

    create_vector_store(chunks, embedding_model)

def ask_question(question):

    embedding_model = get_embedding_model()

    vector_store = load_vector_store(
        embedding_model
    )

    docs = vector_store.similarity_search(
        question,
        k=5
    )

    print("\n==========================")
    print("Retrieved Chunks")
    print("==========================")

    for i, doc in enumerate(docs):

        print(f"\nChunk {i+1}:")

        print(doc.page_content)

        print("--------------------------")

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return response.content