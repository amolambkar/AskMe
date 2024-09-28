"""
Purpose: Qdrant Wrapper
"""

from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from typing import List, Dict, Any, Optional


class QdrantClientWrapper:
    def __init__(self, host: str, port: int, api_key: Optional[str] = None):
        """
        Initialize the Qdrant client.

        :param host: Qdrant server host.
        :param port: Qdrant server port.
        :param api_key: Optional API key for authentication.
        """
        self.client = QdrantClient(host=host, port=port, api_key=api_key)

    def create_collection(self, collection_name: str, vector_size: int):
        """
        Create a new collection.

        :param collection_name: Name of the collection.
        :param vector_size: Size of the vectors.
        """
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size, distance=models.Distance.COSINE
            ),
        )
        print(f"Collection '{collection_name}' created with vector size {vector_size}.")

    def delete_collection(self, collection_name: str):
        """
        Delete a collection.

        :param collection_name: Name of the collection to delete.
        """
        self.client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' deleted.")

    def upload_points(self, collection_name: str, points: List[PointStruct]):
        """
        Upload points to a collection.

        :param collection_name: Name of the collection.
        :param points: List of PointStruct to upload.
        """
        self.client.upsert(collection_name, points)
        print(f"Uploaded {len(points)} points to collection '{collection_name}'.")

    def search(
        self, collection_name: str, query_vector: List[float], limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for similar points in a collection.

        :param collection_name: Name of the collection.
        :param query_vector: The vector to search for.
        :param limit: Maximum number of results to return.
        :return: List of matching points.
        """
        results = self.client.search(
            collection_name=collection_name,
            query_vector=("", query_vector),
            limit=limit,
        )
        return results

    def get_collections(self) -> List[str]:
        """
        Retrieve a list of all collections.

        :return: List of collection names.
        """
        collections = self.client.get_collections()
        print(collections)
        return [collection.name for collection in collections.collections]
