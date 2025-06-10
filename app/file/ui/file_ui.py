import uuid
from io import BytesIO

import streamlit as st

from app.file.model.file import File
from app.file.service.file_service import FileService


class FileUI:

    @staticmethod
    async def view(
        chat_id: uuid.UUID,
        file_service: FileService
    ) -> None:
        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = set()
        st.header("📁 Upload")
        uploaded_file = st.file_uploader(
            "📎 File",
            type=["pdf"],
            help="Allowed file types: pdf"
        )

        if uploaded_file is not None:
            file_id = f"{uploaded_file.name}_{uploaded_file.size}_{chat_id}"
            if file_id not in st.session_state.uploaded_files:
                await file_service.upload_file(u_file=uploaded_file, chat_id=chat_id)
                st.session_state.uploaded_files.add(file_id)
                st.success(f"File '{uploaded_file.name}' ready")
                st.rerun()

        with st.expander("👁️ Preview"):
            files = await file_service.all(conditions={"chat_id": chat_id})
            if files:
                for file in files:
                    FileUI.file_preview(file, file_service)
        st.markdown("---")

    @staticmethod
    def file_preview(
            file: File,
            file_service: FileService
    ) -> None:
        img = file_service.pdf_to_image(file.content, only_first_page=True)
        img_byte_arr = BytesIO()
        img[0].save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        st.image(img_byte_arr, caption=f"First page of {file.name}", use_container_width=True)
