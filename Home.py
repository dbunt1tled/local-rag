import asyncio
import uuid

import nest_asyncio  # type: ignore
import streamlit as st

from app.chat.ui.chat_ui import ChatUI
from internal.di.container import Container

nest_asyncio.apply()
async def main() -> None:
    st.set_page_config(
        page_title="Home",
        layout="wide",
        page_icon="👋",
        menu_items={
            'Get Help': 'https://my_website.com/help',
            'Report a bug': "https://my_website.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )
    st.title("Welcome to Local RAG! 👋")
    query_params = st.query_params
    di = Container()
    chat_service = di.chat_service()
    file_service = di.file_service()
    message_service = di.message_service()
    ai_service = di.ai_service()
    if "chat_id" in query_params:
        chat_id = uuid.UUID(query_params["chat_id"])
        await ChatUI.view(
            chat_id=chat_id,
            chat_service=chat_service,
            file_service=file_service,
            message_service=message_service,
            ai_service=ai_service,
        )
    else:
        await ChatUI.list(chat_service=chat_service)



if __name__ == "__main__":
    asyncio.run(main())
