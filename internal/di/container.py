from dependency_injector import containers, providers
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ai.service.ai_service import AIService
from app.chat.repository.chat_repository import ChatRepository
from app.chat.service.chat_service import ChatService
from app.file.repository.file_repository import FileRepository
from app.file.service.file_service import FileService
from app.message.repository.message_repository import MessageRepository
from app.message.service.message_service import MessageService
from internal.config.db_config import DBConfig
from internal.config.setting import setting


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db_config = providers.Singleton(DBConfig, dsn=setting.pg_dsn)

    text_specifier = providers.Object(RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        add_start_index=True,
    ))

    vector_store = providers.Object(PGVector(
        embeddings=OllamaEmbeddings(
            model=setting.text_embedding_model,
            base_url=setting.ollama_host
        ),
        collection_name=setting.collection_name,
        connection=setting.pg_dsn,
        use_jsonb=True,
        async_mode=True,
    ))

    llm = providers.Object(ChatOllama(model=setting.llm_model, base_url=setting.ollama_host))

    chat_repository = providers.Singleton(
        ChatRepository,
        db_config=db_config,
    )

    file_repository = providers.Singleton(
        FileRepository,
        db_config=db_config,
    )

    message_repository = providers.Singleton(
        MessageRepository,
        db_config=db_config,
    )

    chat_service = providers.Singleton(
        ChatService,
        chat_repository=chat_repository,
    )

    file_service = providers.Singleton(
        FileService,
        file_repository=file_repository,
        text_specifier=text_specifier,
        vector_store=vector_store,
    )

    message_service = providers.Singleton(
        MessageService,
        message_repository=message_repository
    )

    ai_service = providers.Singleton(
        AIService,
        llm=llm,
        vector_store=vector_store,
        file_service=file_service,
    )


