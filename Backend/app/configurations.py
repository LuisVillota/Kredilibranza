import pydantic_settings


class Configs(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    openai_api_key: str
    model: str
    max_tokens: int
    temperature: float
    number_of_vectorial_results: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    mongodb_uri: str
    mongodb_name: str

    email_username: str
    email_password: str
    email_from: str
    email_to: str
    email_subject: str = "Nuevo registro recibido"
    email_smtp_server: str = "smtp.gmail.com"
    email_smtp_port: int = 587
