from base64 import b64decode
from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from fastapi import HTTPException
from jose import jwt

from app.configurations import Configs
from app.core.auth import create_access_token, get_current_user, pwd_context, verify_password
from app.core.models import Document, UserInDB
from app.core.schemas import FormData
from app.usecases import AuthService, DocumentService, FormSubmissionService, RAGService


def test_generate_answer():
    # 1. Preparación (Arrange)
    question = "¿Cuál es el capital de Francia?"
    mock_document_repo = Mock()
    mock_openai_adapter = Mock()

    mock_document_repo.get_documents.return_value = [
        Document(id="1", content="París es la capital de Francia."),
        Document(id="2", content="Francia es un país en Europa."),
    ]

    expected_answer = "La capital de Francia es París."
    mock_openai_adapter.generate_text.return_value = expected_answer

    rag_service = RAGService(document_repo=mock_document_repo, openai_adapter=mock_openai_adapter)

    # 2. Ejecución (Act)
    answer = rag_service.generate_answer(question)

    # 3. Verificación (Assert)
    assert answer == expected_answer, "La respuesta generada no coincide con la esperada"


def test_save_document():
    # 1. Preparación (Arrange)
    document_content = "Este es el contenido de prueba del documento."
    mock_document_repo = Mock()
    mock_openai_adapter = Mock()

    rag_service = RAGService(document_repo=mock_document_repo, openai_adapter=mock_openai_adapter)

    # 2. Ejecución (Act)
    document_id = rag_service.save_document(document_content)

    # 3. Verificación (Assert)
    mock_document_repo.save_document.assert_called_once()
    saved_document = mock_document_repo.save_document.call_args[0][0]
    assert saved_document.content == document_content, "El contenido del documento guardado no coincide"

    assert isinstance(document_id, str) and document_id, "El ID de documento no es un string válido o está vacío"


def test_delete_document():
    # 1. Preparación (Arrange)
    document_id = "1234"
    mock_document_repo = Mock()
    mock_openai_adapter = Mock()

    rag_service = RAGService(document_repo=mock_document_repo, openai_adapter=mock_openai_adapter)

    # 2. Ejecución (Act)
    rag_service.delete_document(document_id)

    # 3. Verificación (Assert)
    mock_document_repo.delete_document.assert_called_once_with(document_id)

    assert mock_document_repo.delete_document.call_count == 1, "delete_document fue llamado más de una vez"


def test_delete_document2():
    # 1. Preparación (Arrange)
    document_id = "1234"
    mock_document_repo = Mock()
    mock_openai_adapter = Mock()

    mock_document_repo.get_document.return_value = None

    rag_service = RAGService(document_repo=mock_document_repo, openai_adapter=mock_openai_adapter)

    # 2. Ejecución (Act)
    rag_service.delete_document(document_id)

    # 3. Verificación (Assert)
    # Verificar que el método delete_document del repositorio fue llamado con el ID correcto
    mock_document_repo.delete_document.assert_called_once_with(document_id)

    deleted_document = mock_document_repo.get_document(document_id)
    assert deleted_document is None, "El documento no fue eliminado correctamente del repositorio"


def test_extract_text():
    # 1. Preparación (Arrange)
    file_content = b"Contenido simulado del archivo PDF o DOCX"
    expected_text = "Texto extraído del archivo"

    mock_text_extractor = Mock()
    mock_text_extractor.extract_text.return_value = expected_text

    document_service = DocumentService(text_extractor=mock_text_extractor)

    # 2. Ejecución (Act)
    extracted_text = document_service.extract_text(file_content)

    # 3. Verificación (Assert)
    assert extracted_text == expected_text, "El texto extraído no coincide con el esperado"


@pytest.mark.asyncio
async def test_send_email_notification():
    # 1. Preparación (Arrange)
    form_data = FormData(
        nombre_completo="Juan Pérez",
        cedula="1234567890",
        convenio="Convenio Ejemplo",
        telefono="123456789",
        fecha_nacimiento="1990-01-01",
        politica_privacidad=True,
    )

    configs = Configs(
        email_username="test@example.com",
        email_password="password",
        email_from="from@example.com",
        email_to="to@example.com",
        email_subject="Nuevo registro recibido",
        email_smtp_server="smtp.test.com",
        email_smtp_port=587,
    )

    form_service = FormSubmissionService(form_repository=Mock(), configs=configs)

    with patch("aiosmtplib.send", return_value=True) as mock_send:
        # 2. Ejecución (Act)
        result = await form_service._send_email_notification(form_data)

        # 3. Verificación (Assert)
        assert result is True, "El envío del correo debería haber sido exitoso"

        mock_send.assert_called_once()

        email_message = mock_send.call_args[0][0]

        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body_encoded = part.get_payload()
                body_decoded = b64decode(body_encoded).decode("utf-8")

                assert form_data.nombre_completo in body_decoded
                assert form_data.cedula in body_decoded
                assert form_data.telefono in body_decoded
                break


@pytest.mark.asyncio
async def test_submit_form():
    # 1. Preparación (Arrange)
    form_data = FormData(
        nombre_completo="Juan Pérez",
        cedula="1234567890",
        convenio="Convenio Ejemplo",
        telefono="123456789",
        fecha_nacimiento="1990-01-01",
        politica_privacidad=True,
    )

    mock_form_repository = Mock()
    mock_form_repository.insert_form_submission = AsyncMock(return_value="mocked_id")
    mock_configs = Configs()

    form_service = FormSubmissionService(form_repository=mock_form_repository, configs=mock_configs)

    with patch.object(form_service, "_send_email_notification", new=AsyncMock(return_value=True)):
        # 2. Ejecución (Act)
        success, message, data = await form_service.submit_form(form_data)

        # 3. Verificación (Assert)
        # Verificar que submit_form retorne un mensaje de éxito y los datos esperados
        assert success is True, "El formulario debería haberse enviado con éxito"
        assert message == "Formulario enviado exitosamente", "El mensaje no coincide con el esperado"
        assert data["inserted_id"] == "mocked_id", "El ID de inserción no coincide con el esperado"
        assert data["email_sent"] is True, "El envío del correo debería haber sido exitoso"


@pytest.mark.asyncio
async def test_get_form_submissions():
    # Preparación (Arrange)
    mock_repository = MagicMock()
    configs = Configs()

    # Datos simulados de prueba
    mock_data = [
        {
            "_id": "1",
            "nombre_completo": "Juan Pérez",
            "cedula": "123456789",
            "convenio": "Empresa X",
            "telefono": "555-1234",
            "fecha_nacimiento": "1980-01-01T00:00:00",
            "politica_privacidad": True,
            "created_at": "2023-10-01T12:00:00",
        },
        {
            "_id": "2",
            "nombre_completo": "Ana Gómez",
            "cedula": "987654321",
            "convenio": "Empresa Y",
            "telefono": "555-5678",
            "fecha_nacimiento": "1990-05-15T00:00:00",
            "politica_privacidad": True,
            "created_at": "2023-10-02T15:30:00",
        },
    ]

    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = mock_data
    mock_repository.db["form_submissions"].find.return_value = mock_cursor

    form_service = FormSubmissionService(form_repository=mock_repository, configs=configs)

    # Ejecución (Act)
    submissions = await form_service.get_form_submissions()

    # Verificación (Assert)
    assert len(submissions) == len(mock_data)
    for i, submission in enumerate(submissions):
        assert submission.id == str(mock_data[i]["_id"])
        assert submission.nombre_completo == mock_data[i]["nombre_completo"]
        assert submission.cedula == mock_data[i]["cedula"]
        assert submission.convenio == mock_data[i]["convenio"]
        assert submission.telefono == mock_data[i]["telefono"]
        assert submission.politica_privacidad == mock_data[i]["politica_privacidad"]


@pytest.mark.asyncio
async def test_authenticate_user():
    # Preparación (Arrange)
    mock_user_repo = AsyncMock()
    configs = Configs()
    auth_service = AuthService(user_repo=mock_user_repo)

    # Datos de usuario y contraseña
    username = "admin"
    password = "password123"
    hashed_password = "$2b$12$K9H1v/FHGI5QUDR.xK9LxO.EBOp6F3MsRz5GmfzSXzDa1Nsd8Mvay"

    # Caso 1: Usuario y contraseña correctos
    user_in_db = UserInDB(username=username, full_name="Admin", hashed_password=hashed_password)
    mock_user_repo.get_user_by_username = AsyncMock(return_value=user_in_db)

    with patch("app.usecases.verify_password", return_value=True) as mock_verify_password, patch(
        "app.usecases.create_access_token", return_value="mocked_token"
    ) as mock_create_access_token:
        token = await auth_service.authenticate_user(username=username, password=password)

        # Verificación
        assert token == "mocked_token"
        mock_verify_password.assert_called_once_with(password, user_in_db.hashed_password)
        mock_create_access_token.assert_called_once_with(
            data={"sub": user_in_db.username},
            expires_delta=timedelta(minutes=configs.access_token_expire_minutes),
        )

    # Caso 2: Usuario no encontrado
    mock_user_repo.get_user_by_username.return_value = None
    token = await auth_service.authenticate_user(username="unknown_user", password=password)
    assert token is None

    # Caso 3: Contraseña incorrecta
    mock_user_repo.get_user_by_username.return_value = user_in_db
    mock_verify_password.return_value = False
    token = await auth_service.authenticate_user(username=username, password="wrongpassword")
    assert token is None


@pytest.mark.asyncio
async def test_login():
    # Preparación (Arrange)
    mock_user_repo = AsyncMock()
    Configs()
    auth_service = AuthService(user_repo=mock_user_repo)

    username = "admin"
    password = "password123"
    hashed_password = "$2b$12$K9H1v/FHGI5QUDR.xK9LxO.EBOp6F3MsRz5GmfzSXzDa1Nsd8Mvay"

    user_in_db = UserInDB(username=username, full_name="Admin", hashed_password=hashed_password)
    mock_user_repo.get_user_by_username = AsyncMock(return_value=user_in_db)

    with patch("app.usecases.verify_password", return_value=True) as mock_verify_password, patch(
        "app.usecases.create_access_token", return_value="mocked_token"
    ) as mock_create_access_token:
        # Ejecución (Act) y Verificación (Assert) para el inicio de sesión exitoso
        response = await auth_service.login(username=username, password=password)

        # Mensajes de depuración
        print("Respuesta de login:", response)

        assert response == {"access_token": "mocked_token", "token_type": "bearer"}
        mock_verify_password.assert_called_once_with(password, user_in_db.hashed_password)
        mock_create_access_token.assert_called_once()

    # Caso 2: Usuario válido pero contraseña incorrecta
    mock_verify_password.return_value = False
    response = await auth_service.login(username=username, password="wrongpassword")
    assert response == {"error": "Nombre de usuario o contraseña incorrectos"}

    # Caso 3: Usuario inexistente
    mock_user_repo.get_user_by_username.return_value = None
    response = await auth_service.login(username="unknown_user", password=password)
    assert response == {"error": "Nombre de usuario o contraseña incorrectos"}


def test_create_access_token():
    configs = Configs()
    data = {"sub": "test_user"}
    expires_delta = timedelta(minutes=10)

    token = create_access_token(data=data, expires_delta=expires_delta)

    # Verificar que el token decodificado contiene los datos correctos
    decoded_token = jwt.decode(token, configs.secret_key, algorithms=[configs.algorithm])
    assert decoded_token["sub"] == data["sub"]
    assert "exp" in decoded_token


def test_verify_password():
    password = "test_password"
    hashed_password = pwd_context.hash(password)

    # Prueba con contraseña correcta
    assert verify_password(password, hashed_password) is True

    # Prueba con contraseña incorrecta
    assert verify_password("wrong_password", hashed_password) is False


@pytest.mark.asyncio
async def test_get_current_user_valid():
    Configs()
    user_data = {"sub": "test_user"}
    token = create_access_token(data=user_data)

    with patch("app.core.auth.get_user", return_value=AsyncMock()) as mock_get_user:
        mock_get_user.return_value = UserInDB(username="test_user", hashed_password="fakehashed")
        user = await get_current_user(token)
        assert user.username == "test_user"


@pytest.mark.asyncio
async def test_get_current_user_invalid():
    Configs()
    invalid_token = "invalid.token.value"

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(invalid_token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "No se pudieron validar las credenciales"
