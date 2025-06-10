import uuid

import streamlit as st

from app.ai.service.ai_service import AIService
from app.chat.dto.chat_schema import ChatCreate
from app.chat.service.chat_service import ChatService
from app.file.service.file_service import FileService
from app.file.ui.file_ui import FileUI
from app.message.service.message_service import MessageService
from app.message.ui.message_ui import MessageUI


class ChatUI:

    @staticmethod
    async def view(
        chat_id: uuid.UUID,
        chat_service: ChatService,
        file_service: FileService,
        message_service: MessageService,
        ai_service: AIService,
    ) -> None:
        chat = await chat_service.get_by_id(chat_id)
        st.title(f"💬 {chat.name}")
        st.markdown("---")

        with st.sidebar:
            await FileUI.view(
                chat_id=chat_id,
                file_service=file_service
            )

            st.subheader("🔧 Chat Available:")
            st.markdown("""
            - 📎 Upload PDF files
            - 🔍 Automated content analysis
            - 💬 Discussion of file content
            - 💾 Save chat history
            """)

        await MessageUI.chat(
            chat_id=chat_id,
            message_service=message_service,
            ai_service=ai_service,
        )


    @staticmethod
    async def list(
        chat_service: ChatService
    ) -> None:
        st.title("💬 Chat Manager")
        st.markdown("---")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.header("📋 Chats")

            chats = await chat_service.all()

            if not chats:
                st.info("No chats yet")
            else:
                for chat in chats:
                    with st.container():
                        chat_col1, chat_col2, chat_col3 = st.columns([3, 1, 1])

                        with chat_col1:
                            st.subheader(f"💬 {chat.name}")
                            st.caption(f"Created: {chat.created_at.strftime('%d.%m.%Y %H:%M')}")

                        with chat_col2:
                            if st.button("Open", key=f"open_{chat.id}"):
                                st.query_params["chat_id"] = str(chat.id)
                                st.rerun()

                        with chat_col3:
                            if st.button("🗑️", key=f"delete_{chat.id}", help="Remove"):
                                await chat_service.delete(chat.id)
                                st.rerun()

                        st.markdown("---")

        with col2:
            st.header("➕ Create a new chat")

            with st.form("new_chat_form"):
                chat_name = st.text_input("Name", placeholder="Enter chat name")
                if st.form_submit_button("Submit", type="primary"):
                    if chat_name:
                        await  chat_service.create(ChatCreate(name=chat_name))
                        st.success(f"Chat '{chat_name}' created!")
                        st.rerun()
                    else:
                        st.error("Enter chat name")
