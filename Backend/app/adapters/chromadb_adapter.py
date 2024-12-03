from typing import List

import chromadb
from chromadb.config import Settings

from app.core import models, ports


class ChromaDBAdapter(ports.DocumentRepositoryPort):
    def __init__(self, number_of_vectorial_results: int) -> None:
        self.client = chromadb.Client(Settings(persist_directory="./chromadb_data"))
        self.collection = self.client.get_or_create_collection("documents")
        self._number_of_vectorial_results = number_of_vectorial_results

    def save_document(self, document: models.Document) -> None:
        print(f"Document: {document}")
        self.collection.add(ids=[document.id], documents=[document.content])

    def get_documents(self, query: str, n_results: int | None = None) -> List[models.Document]:
        if not n_results:
            n_results = self._number_of_vectorial_results
        results = self.collection.query(query_texts=[query], n_results=n_results)
        print(query)
        print(f"Results: {results}")
        documents = []
        for doc_ids, docs in zip(results["ids"], results["documents"]):
            for doc_id, doc_content in zip(doc_ids, docs):
                documents.append(models.Document(id=doc_id, content=doc_content))
        return documents

    def delete_document(self, document_id: str) -> None:
        self.collection.delete(ids=[document_id])
