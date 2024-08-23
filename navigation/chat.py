import base64
import requests

from uuid import uuid4

import streamlit as st

from navigation import (
    Message,
    MessageComponent,
    MessageComponentType,
    render_message_history,
    save_chat_history,
    show_previous_chats,
    DEFAULT_ASSISTANT_MESSAGE
)


def sidebar():
    with st.sidebar:
        if st.button(label="New Chat :material/add:", use_container_width=True):
            save_chat_history()
            st.session_state.chat_id = str(uuid4())
            st.session_state.messages = [DEFAULT_ASSISTANT_MESSAGE]
            st.rerun()

        if st.button(label="Save Chat :material/save:", use_container_width=True):
            save_chat_history()
            st.rerun()

        if st.button(label="Logout :material/logout:", use_container_width=True):
            st.session_state.logged_out = True
            st.session_state.logged_in = False
            st.rerun()

        st.selectbox(
            label="Model", options=st.session_state.models, key="current_model"
        )


def chat():
    render_message_history()

    sidebar()

    show_previous_chats()

    query = st.chat_input()

    if query:
        user_message = Message(
            components=[
                MessageComponent(
                    message_component_type=MessageComponentType.TEXT, data=query
                )
            ],
            user="user",
            icon=st.session_state.user_avatar,
        )
        st.session_state.messages.append(user_message)
        user_message.render_message()

        if "<IMAGE>" in query:
            with st.spinner("Generating your image . . ."):
                payload = st.session_state.default_image_payload
                payload["prompt"] = query.lstrip("<IMAGE>")
                payload["hr_prompt"] = query.lstrip("<IMAGE>")
                image = requests.post("http://127.0.0.1:7861/sdapi/v1/txt2img", json=payload).json()["images"][0]
                ai_message = Message(
                    components=[
                        MessageComponent(
                            message_component_type=MessageComponentType.IMAGE, data=image
                        )
                    ]
                )
                st.session_state.messages.append(ai_message)
                ai_message.render_message()
        else:
            with st.chat_message("assistant", avatar=st.session_state.assistant_avatar):
                with st.spinner("Thinking . . ."):
                    response = st.session_state.ollama_client.get_chat_completion(
                        model=st.session_state.current_model, query=query
                    )["message"]["content"]
                ai_message = Message(
                    components=[
                        MessageComponent(
                            message_component_type=MessageComponentType.TEXT, data=response
                        )
                    ]
                )
                st.session_state.messages.append(ai_message)
                st.markdown(response)


chat()
