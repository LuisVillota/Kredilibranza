from abc import ABC, abstractmethod
from typing import Any, Dict, List, Protocol

from app.core import models
from app.core.models import UserInDB


class DocumentRepositoryPort(ABC):
    @abstractmethod
    def save_document(self, document: models.Document) -> None:
        pass

    @abstractmethod
    def get_documents(self, query: str, n_results: int | None = None) -> List[models.Document]:
        pass

    def delete_document(self, document_id: str) -> None:
        pass


class LlmPort(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, retrieval_context: str) -> str:
        pass


class DocumentTextExtractorPort(ABC):
    @abstractmethod
    def extract_text(self, file_bytes: bytes) -> str:
        pass


class UserRepositoryPort(ABC):
    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserInDB | None:
        pass


class FormRepositoryPort(Protocol):
    async def insert_form_submission(self, data: Dict[str, Any]) -> Any:
        pass

    async def get_form_submission(self, submission_id: str) -> Dict[str, Any]:
        pass
