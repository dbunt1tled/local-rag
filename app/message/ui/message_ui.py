import uuid

import streamlit as st
import streamlit.components.v1 as components

from app.ai.service.ai_service import AIService
from app.message.dto.message_enum import MessageType
from app.message.dto.message_schema import MessageCreate
from app.message.service.message_service import MessageService


class MessageUI:
    @staticmethod
    async def chat(
            chat_id: uuid.UUID,
            message_service: MessageService,
            ai_service: AIService,
    ) -> None:
        MessageUI.styles()
        if 'input_key' not in st.session_state:
            st.session_state.input_key = 0
        messages_html = await MessageUI.list_html(chat_id=chat_id, message_service=message_service)
        st.html(messages_html)
        st.html('<div style="margin-bottom: 10px;"></div>')
        prompt = st.chat_input("Say something")

        if prompt:
            await message_service.create(
                chat_create=MessageCreate(
                    text=prompt,
                    chat_id=chat_id,
                    type=MessageType.USER
                )
            )
            st.session_state.input_key += 1
            with st.spinner("writing..."):
                answer = await ai_service.query(query=prompt, chat_id=chat_id)
                await message_service.create(
                    chat_create=MessageCreate(
                        text=answer if answer is not None else "I don't know",
                        chat_id=chat_id,
                        type=MessageType.SYSTEM
                    )
                )
            st.rerun()
        components.html("""
        <script>
            function scrollToBottom() {
                var messagesContainer = parent.document.querySelector('.messages-container');
                if (messagesContainer) {
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }
            }
            setTimeout(scrollToBottom, 300);
        </script>
        """, height=0, width=0)

    @staticmethod
    async def list_html(
        chat_id: uuid.UUID,
        message_service: MessageService
    ) -> str:
        messages = await message_service.all(conditions={"chat_id": chat_id})
        messages_html = ""

        for message in messages:
            if  message.type == MessageType.SYSTEM:
                messages_html += f"""
                <div class="message-row other">
                    <div class="avatar">👤</div>
                    <div class="message-bubble other">
                        <p class="message-text">{message.text}</p>
                        <div class="message-time other">{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}</div>
                    </div>
                </div>
                """
            else:
                messages_html += f"""
                <div class="message-row me">
                    <div class="message-bubble me">
                        <p class="message-text">{message.text}</p>
                        <div class="message-time">{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}</div>
                    </div>
                </div>
                """

        return f'<div class="messages-container">{messages_html}</div>'

    @staticmethod
    def styles() -> None:
        st.html("""
            <style>
                .main .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                    max-width: 100%;
                }
                .chat-header {
                    background: linear-gradient(90deg, #0088cc, #0066aa);
                    color: white;
                    padding: 15px 20px;
                    border-radius: 10px 10px 0 0;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }

                .chat-header h1 {
                    margin: 0;
                    font-size: 1.5rem;
                    font-weight: 600;
                }

                .chat-header .status {
                    font-size: 0.9rem;
                    opacity: 0.9;
                }
                .messages-container {
                    height: 45vh;
                    overflow-y: auto;
                    padding: 10px;
                    background: rgb(38, 39, 48);
                    border-radius: 10px;
                    margin-bottom: 20px;
                    border: 1px solid #e0e0e0;
                }

                .message-row {
                    display: flex;
                    margin-bottom: 15px;
                    align-items: flex-end;
                }

                .message-row.me {
                    justify-content: flex-end;
                }

                .message-row.other {
                    justify-content: flex-start;
                }

                .message-bubble {
                    max-width: 70%;
                    padding: 12px 16px;
                    border-radius: 18px;
                    position: relative;
                    word-wrap: break-word;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }

                .message-bubble.me {
                    background: #0088cc;
                    color: white;
                    border-bottom-right-radius: 4px;
                    margin-left: auto;
                }

                .message-bubble.other {
                    background: #333;
                    color: #ccc;
                    border-bottom-left-radius: 4px;
                    border: 1px solid #222;
                    margin-left: 10px;
                }

                .message-text {
                    font-size: 0.95rem;
                    line-height: 1.4;
                    margin: 0;
                }

                .message-time {
                    font-size: 0.75rem;
                    opacity: 0.7;
                    margin-top: 4px;
                    text-align: right;
                }

                .message-time.other {
                    text-align: left;
                }

                .avatar {
                    width: 35px;
                    height: 35px;
                    border-radius: 50%;
                    background: #ddd;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.2rem;
                    margin-bottom: 5px;
                }

                .input-container {
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    background: white;
                    padding: 15px 20px;
                    border-top: 1px solid #e0e0e0;
                    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
                    z-index: 1000;
                }

                .stButton > button {
                    background: #0088cc;
                    color: white;
                    border: none;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    font-size: 1.2rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                .stButton > button:hover {
                    background: #0077bb;
                    box-shadow: 0 2px 8px rgba(0,136,204,0.3);
                }

                .stTextArea > div > div > textarea {
                    border-radius: 25px;
                    border: 1px solid #ddd;
                    padding: 12px 20px;
                    font-size: 0.95rem;
                    resize: none;
                    max-height: 120px;
                }

                .stTextArea > div > div > textarea:focus {
                    border-color: #0088cc;
                    box-shadow: 0 0 0 2px rgba(0,136,204,0.2);
                }
            </style>
            """)
