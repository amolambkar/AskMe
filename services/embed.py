"""
Purpose : embedding related functions.
"""

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
)


def create_embeddings_of_docs(text_list):
    """
    Function: create embeddings of given batch
    """
    return embeddings.embed_documents(text_list)


def create_embedding(text):
    """
    Function: create embedding of given text
    """
    return embeddings.embed_query(text)
