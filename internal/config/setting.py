from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    ollama_host: str = Field(..., validation_alias="OLLAMA_HOST")
    text_embedding_model: str = Field(..., validation_alias="TEXT_EMBEDDING_MODEL")
    llm_model: str = Field(..., validation_alias="LLM_MODEL")
    temp_folder: str = Field(..., validation_alias="TEMP_FOLDER")
    collection_name: str = Field(..., validation_alias="COLLECTION_NAME")
    pg_dsn: str = Field(..., validation_alias="PG_DSN")


load_dotenv()
setting = Settings()  # type: ignore