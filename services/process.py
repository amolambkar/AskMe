"""
Purpose: Utility functions
"""
import os
import uuid
from langchain.text_splitter import CharacterTextSplitter
from qdrant_client import QdrantClient, models
from services.embed import create_embedding
from services.qdrant import QdrantClientWrapper

qd_client = QdrantClientWrapper(host=os.getenv('QDRANT_HOST'), port=os.getenv('QDRANT_PORT'), api_key=os.getenv('QDRANT_API'))


def get_text_chunks(text):
    """
    Function to split text into chunks
    """
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def store_to_vector_db(text):
    """
    Function to store text data to vector db
    """

    collections = qd_client.get_collections()
    if os.getenv('QDRANT_COLLECTION')not in collections:
        qd_client.create_collection(os.getenv('QDRANT_COLLECTION'), 1536)

    points = []
    chunks = get_text_chunks(text)
    for chunk in chunks:
        embedding = create_embedding(chunk)
        point = models.PointStruct(
            id=str(uuid.uuid4()), payload={"text": chunk}, vector=embedding
        )
        points.append(point)
        if len(points) % 10 == 0:
            qd_client.upload_points(os.getenv('QDRANT_COLLECTION'), points)
            points = []

    if len(points) > 0:
        qd_client.upload_points(os.getenv('QDRANT_COLLECTION'), points)


def create_context(question):
    """
    Function to create a context using question embedding and qdrant data
    """
    que_embedding = create_embedding(question)
    points = qd_client.search(os.getenv('QDRANT_COLLECTION'), que_embedding, 3)

    text_list = []
    if len(points) > 0:
        text_list.append(points[0].payload.get("text", ""))

    return " ".join(text_list)
