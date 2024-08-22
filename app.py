import json
import base64
import requests

import streamlit as st

from uuid import uuid4
from navigation import DEFAULT_ASSISTANT_MESSAGE, OllamaClient

st.set_page_config(layout="wide")

def init():
    if not st.session_state.get("init") or st.session_state.get("logged_out"):
        st.session_state.init = True
        st.session_state.logged_in = False
        st.session_state.logged_out = False
        st.session_state.display_name = None
        st.session_state.user_avatar = "😒"
        st.session_state.assistant_avatar = "😈"
        st.session_state.messages = [DEFAULT_ASSISTANT_MESSAGE]
        st.session_state.chat_id = str(uuid4())
        st.session_state.ollama_client = OllamaClient(host="192.168.1.2")
        st.session_state.models = st.session_state.ollama_client.models()
        st.session_state.default_image_payload = {
            "prompt": "",
            "negative_prompt": "",
            "quality": 2,
            "cfg_scale": 5.0,
            "steps": 25,
            "seed": -1,
            "upscale_model": "Latent",
            "sample_set": "DDIM",
            "images": 1
        }


def main():
    init()

    login_page = st.Page("navigation/login.py", title="Login", icon=":material/login:")
    settings_page = st.Page("navigation/settings.py", title="Settings", icon=":material/settings:")
    chat_page = st.Page("navigation/chat.py", title="Chat", icon=":material/forum:")

    if st.session_state.logged_in:
        pg = st.navigation([chat_page, settings_page])
    else:
        pg = st.navigation([login_page])
    
    pg.run()



if __name__ == "__main__":
    main()