from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional, Tuple

import aiosmtplib
from app.configurations import Configs
from app.core import ports
from app.core.auth import create_access_token, verify_password
from app.core.models import Document
from app.core.ports import DocumentTextExtractorPort, UserRepositoryPort
from app.core.schemas import FormData, Submission
from app.adapters.mongodb_adapter import MongoDBAdapter


class RAGService:
    def __init__(self, document_repo: ports.DocumentRepositoryPort, openai_adapter: ports.LlmPort):
        self.document_repo = document_repo
        self.openai_adapter = openai_adapter

    def generate_answer(self, query: str) -> str:
        try:
            documents = self.document_repo.get_documents(query)
            if not documents:
                return "No se encontró información relevante en los documentos cargados."

            context = " ".join([doc.content for doc in documents])
            context = context[:2000]
            return self.openai_adapter.generate_text(prompt=query, retrieval_context=context)

        except Exception:
            return "Ocurrió un error al procesar la consulta."

    def save_document(self, content: str) -> str:
        document = Document(content=content)
        self.document_repo.save_document(document)
        return document.id

    def delete_document(self, document_id: str) -> None:
        self.document_repo.delete_document(document_id)


class DocumentService:
    def __init__(self, text_extractor: DocumentTextExtractorPort):
        self.text_extractor = text_extractor

    def extract_text(self, file_bytes: bytes) -> str:
        return self.text_extractor.extract_text(file_bytes)


class FormSubmissionService:
    def __init__(self, form_repository: ports.FormRepositoryPort, configs: Configs):
        self.form_repository = form_repository
        self.configs = configs

    async def _send_email_notification(self, form_data: FormData) -> bool:
        message = MIMEMultipart()
        message["From"] = self.configs.email_from
        message["To"] = self.configs.email_to
        message["Subject"] = self.configs.email_subject

        body = f"""
        Se ha recibido un nuevo registro:

        Nombre Completo: {form_data.nombre_completo}
        Cédula: {form_data.cedula}
        Convenio: {form_data.convenio}
        Teléfono: {form_data.telefono}
        Fecha de Nacimiento: {form_data.fecha_nacimiento.strftime('%Y-%m-%d')}
        """

        message.attach(MIMEText(body, "plain"))

        try:
            await aiosmtplib.send(
                message,
                hostname=self.configs.email_smtp_server,
                port=self.configs.email_smtp_port,
                start_tls=True,
                username=self.configs.email_username,
                password=self.configs.email_password,
            )
            return True
        except Exception:
            return False

    async def submit_form(self, form_data: FormData) -> Tuple[bool, str, Dict[str, Any]]:
        if not form_data.politica_privacidad:
            return False, "Debe aceptar la política de privacidad.", {}

        try:
            if isinstance(form_data.fecha_nacimiento, date):
                form_data.fecha_nacimiento = datetime.combine(form_data.fecha_nacimiento, datetime.min.time())

            data = form_data.dict()
            inserted_id = await self.form_repository.insert_form_submission(data)

            if not inserted_id:
                return False, "Error al guardar los datos en la base de datos.", {}

            str_id = str(inserted_id)
            email_sent = await self._send_email_notification(form_data)

            return (
                True,
                "Formulario enviado exitosamente",
                {"inserted_id": str_id, "email_sent": email_sent},
            )

        except Exception as e:
            return False, f"Error al procesar el formulario: {str(e)}", {}

    async def get_form_submissions(self, cedula: Optional[str] = None) -> List[Submission]:
        if not isinstance(self.form_repository, MongoDBAdapter):
            raise TypeError("El repositorio no tiene acceso a la base de datos.")
        query = {"cedula": cedula} if cedula else {}
        submissions_cursor = self.form_repository.db["form_submissions"].find(query)

        submissions = []
        async for submission in submissions_cursor:
            submission_data = {
                "id": str(submission["_id"]),
                "nombre_completo": submission["nombre_completo"],
                "cedula": submission["cedula"],
                "convenio": submission["convenio"],
                "telefono": submission["telefono"],
                "fecha_nacimiento": submission["fecha_nacimiento"],
                "politica_privacidad": submission["politica_privacidad"],
                "created_at": submission.get("created_at"),
            }
            submissions.append(Submission(**submission_data))

        return submissions


class AuthService:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo
        self.configs = Configs()

    async def authenticate_user(self, username: str, password: str) -> Optional[str]:
        user = await self.user_repo.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=self.configs.access_token_expire_minutes),
        )
        return access_token

    async def login(self, username: str, password: str) -> dict:
        token = await self.authenticate_user(username, password)
        if not token:
            return {"error": "Nombre de usuario o contraseña incorrectos"}
        return {"access_token": token, "token_type": "bearer"}
