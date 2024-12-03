from typing import Any, Dict, List

import pydantic
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app import usecases
from app.api import dependencies
from app.api.dependencies import AuthServiceSingleton, FormServiceSingleton, RAGServiceSingleton, get_document_service
from app.core.models import User
from app.core.schemas import FormData, Submission
from app.usecases import AuthService, DocumentService, FormSubmissionService, RAGService

rag_router = APIRouter()


class DocumentInput(BaseModel):
    content: str = pydantic.Field(..., min_length=1)


class QueryInput(BaseModel):
    question: str = pydantic.Field(..., min_length=1)


@rag_router.post("/generate-answer/", status_code=200)
async def generate_answer(
    query_input: QueryInput,
    rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance),
):
    return {"answer": rag_service.generate_answer(query_input.question)}


@rag_router.post("/save-document/", status_code=201)
def save_document(
    document: DocumentInput,
    rag_service: usecases.RAGService = Depends(dependencies.RAGServiceSingleton.get_instance),
):
    rag_service.save_document(content=document.content)
    return {"status": "Document saved successfully"}


@rag_router.post("/upload-file/", status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
    rag_service: RAGService = Depends(RAGServiceSingleton.get_instance),
):
    file_content = await file.read()
    extracted_text = document_service.extract_text(file_content)
    document_id = rag_service.save_document(extracted_text)
    return {"inserted_id": document_id}


@rag_router.delete("/delete-document/{document_id}", status_code=200)
async def delete_document(
    document_id: str,
    rag_service: RAGService = Depends(RAGServiceSingleton.get_instance),
):
    rag_service.delete_document(document_id)
    return {"status": "Document deleted successfully"}


@rag_router.post("/token", response_model=dict)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(AuthServiceSingleton.get_instance),
):
    result = await auth_service.login(form_data.username, form_data.password)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["error"],
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


@rag_router.post("/submit-form/", status_code=201, response_model=Dict[str, Any])
async def submit_form(
    form_data: FormData,
    form_service: FormSubmissionService = Depends(FormServiceSingleton.get_instance),
):
    success, message, data = await form_service.submit_form(form_data)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    response_data = {
        "status": message,
        "inserted_id": data.get("inserted_id"),
        "email_sent": data.get("email_sent", False),
    }

    return response_data


@rag_router.get("/get-requests/", response_model=List[Submission], status_code=200)
async def get_requests(
    cedula: str = Query(None, description="Cédula para buscar"),
    form_service: FormSubmissionService = Depends(FormServiceSingleton.get_instance),
    current_user: User = Depends(AuthServiceSingleton.get_instance),
):
    try:
        submissions = await form_service.get_form_submissions(cedula=cedula)
        return submissions
    except Exception as e:
        print(f"Error al obtener las solicitudes: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener los datos.")
