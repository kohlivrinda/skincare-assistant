from typing import List, Optional
import chromadb


class SkinCareRAGBuilder:
    def __init__(self, collection_name="skincare_db", path_to_save="temp_db"):
        self.collection_name = collection_name

        self.chroma_client = chromadb.PersistentClient(path=path_to_save)
        self.collection = self.chroma_client.create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )

    def _gemini_embeddings(self, documents: List[str]):
        return None

    def insert_products_targeted_skin_issues(self, product_infos: List[dict], ids=Optional[List[str]]):
        """
        Take product_infos -> Gemini API (Embeddings) -> insert embeddings into db
        """

        product_infos_serialised = str(product_infos)

        product_embeddings = self._gemini_embeddings(product_infos_serialised)

        self.collection.add(embeddings=product_embeddings, ids=ids)

    def get_relevant_products(self, query_embeds):
        query_results = self.collection.query(query_embeddings=query_embeds)
        return query_results
