from langchain_openai import OpenAIEmbeddings


def get_embedding_model():
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return embedding_model