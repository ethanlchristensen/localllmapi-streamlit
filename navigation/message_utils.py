import os
import json
import base64
import requests

import streamlit as st

from uuid import uuid4
from enum import Enum

ASSISTANT_AVATAR = ":material/smart_toy:"


class MessageComponentType(Enum):
    TEXT = "text"
    IMAGE = "image"


def get_enum_from_value(text):
    for member in MessageComponentType:
        if member.value == text:
            return member


class MessageComponent:
    def __init__(
        self,
        message_component_type: MessageComponentType,
        data: any,
        expander: bool = False,
        expander_label: str | None = None,
        **kwargs,
    ):
        self.message_component_type = message_component_type
        self.data = data
        self.expander = expander
        self.expander_label = expander_label
        self.kwargs = kwargs if kwargs else {}

    def get_streamlit_component(self):
        if self.message_component_type == MessageComponentType.TEXT:
            st.markdown(body=self.data, **self.kwargs)
        elif self.message_component_type == MessageComponentType.IMAGE:
            st.image(image=base64.b64decode(self.data), **self.kwargs)


class Message:
    def __init__(
        self,
        components: list[MessageComponent],
        user: str = "assistant",
        icon: str = ASSISTANT_AVATAR,
    ):
        self.components = components
        self.user = user
        self.icon = icon

    def add_component(self, component: MessageComponent):
        self.components.append(component)

    def render_message(self):
        with st.chat_message(name=self.user, avatar=self.icon):
            for component in self.components:
                component.get_streamlit_component()


DEFAULT_ASSISTANT_MESSAGE = Message(
    components=[
        MessageComponent(
            message_component_type=MessageComponentType.TEXT, data="How can I help?"
        )
    ]
)


def render_message_history():
    for message in st.session_state.messages:
        message.render_message()


def save_chat_history():
    chat_id = st.session_state.chat_id
    db_entry = {}

    messages = []
    for message in st.session_state.messages:
        messages.append(
            {
                "user": message.user,
                "icon": message.icon,
                "components":[{
                    "message_component_type": component.message_component_type.value,
                    "data": component.data,
                    "expander": component.expander,
                    "expander_label": component.expander_label,
                    **component.kwargs,
                } for component in message.components],
            }
        )

    db_entry["username"] = st.session_state.display_name
    db_entry["messages"] = messages

    chats = json.loads(open(os.path.join(os.getcwd(), "db", "chats.json"), "r").read())
    chats[chat_id] = db_entry
    with open(os.path.join(os.getcwd(), "db", "chats.json"), "w") as db_file:
        db_file.write(json.dumps(chats, indent=4))


def on_previous_chat_click(*args):
    save_chat_history()
    chat_id = args[0]
    chat_messages = json.loads(
        open(os.path.join(os.getcwd(), "db", "chats.json"), "r").read()
    )[chat_id]

    st.session_state.chat_id = chat_id
    messages = []
    for message in chat_messages["messages"]:
        messages.append(
            Message(
                user=message["user"],
                icon=message["icon"],
                components=[
                    MessageComponent(
                        message_component_type=get_enum_from_value(
                            component["message_component_type"]
                        ),
                        data=component["data"],
                        expander=component["expander"],
                        expander_label=component["expander_label"],
                        **{
                            k: v
                            for k, v in component.items()
                            if k
                            not in {
                                "data",
                                "expander",
                                "expander_label",
                                "message_component_type",
                            }
                        },
                    )
                    for component in message["components"]
                ],
            )
        )

    st.session_state.messages = messages


def on_delete_chat(*args):
    chat_id = args[0]
    chats = json.loads(open(os.path.join(os.getcwd(), "db", "chats.json"), "r").read())
    del chats[chat_id]
    with open(os.path.join(os.getcwd(), "db", "chats.json"), "w") as file:
        file.write(json.dumps(chats, indent=4))


def show_previous_chats():
    chats = [
        chat_id
        for chat_id, data in json.loads(
            open(os.path.join(os.getcwd(), "db", "chats.json"), "r").read()
        ).items()
        if data["username"] == st.session_state.display_name
    ]
    if chats:
        with st.sidebar:
            with st.expander(label="Previous Chats", expanded=False):
                chat_columns = st.columns([1, 0.25])
                for chat_id in chats:
                    with chat_columns[0]:
                        st.button(
                            label=(
                                "Currently Selected"
                                if st.session_state.chat_id == chat_id
                                else (chat_id[:25] + "...")
                            ),
                            use_container_width=True,
                            disabled=st.session_state.chat_id == chat_id,
                            args=(chat_id,),
                            on_click=on_previous_chat_click,
                        )
                    with chat_columns[1]:
                        st.button(
                            label=":material/delete:",
                            key=f"delete_{chat_id}",
                            on_click=on_delete_chat,
                            args=(chat_id,),
                        )
