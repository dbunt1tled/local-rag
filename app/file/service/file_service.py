import os
import tempfile
import uuid
from dataclasses import dataclass
from typing import Sequence

from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import TextSplitter
from pdf2image import convert_from_bytes
from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.file.dto.file_schema import FileCreate
from app.file.model.file import File
from app.file.repository.file_repository import FileRepository


@dataclass
class FileService:
    file_repository: FileRepository
    text_specifier: TextSplitter
    vector_store: VectorStore

    @staticmethod
    def pdf_to_image(pdf_bytes: bytes, only_first_page=False) -> list[Image.Image]:
        if only_first_page:
            images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
        else:
            images = convert_from_bytes(pdf_bytes)
        return images

    async def create(self, file_create: FileCreate) -> File:
        f = File(name=file_create.name, chat_id=file_create.chat_id, content=file_create.content)
        return await self.file_repository.create(f)

    async def all(self, conditions: dict = {}) -> Sequence[File]:
        return await self.file_repository.all(conditions=conditions)

    async def get_by_id(self, file_id: uuid.UUID) -> File:
        return await self.file_repository.get_by_id(file_id)

    async def delete(self, file_id: uuid.UUID) -> bool:
        return await self.file_repository.delete(file_id)

    async def upload_file(self, u_file: UploadedFile, chat_id: uuid.UUID) -> File:
        file = await self.create(FileCreate(name=u_file.name, chat_id=chat_id, content=u_file.getvalue()))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(u_file.getvalue())
            tmp_file.flush()
            tmp_file_path = tmp_file.name
            try:
                loader = UnstructuredPDFLoader(
                    file_path=tmp_file_path,
                    # mode="elements",  # "paged"
                    # strategy="fast"   # "hi_res", "auto"
                )
                data = loader.load()
                chunks = self.text_specifier.split_documents(data)
                for document in chunks:
                    document.metadata["file_name"] = u_file.name
                    document.metadata["file_id"] = str(file.id)
                await self.vector_store.aadd_documents(chunks)

            finally:
                os.unlink(tmp_file_path)

        return file

    async def search_documents(self, query: str, chat_id: uuid.UUID) -> list[Document]:
        fileIds = await self.find_files_ids(chat_id=chat_id)
        return await self.vector_store.asimilarity_search(query, filter={"file_id": {"$in": fileIds}})

    async def find_files_ids(self, chat_id: uuid.UUID) -> list[str]:
        files = await self.all(conditions={"chat_id": chat_id})
        return [str(file.id) for file in files]
