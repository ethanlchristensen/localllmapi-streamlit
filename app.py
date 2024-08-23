import json
import base64
import requests

import streamlit as st

from uuid import uuid4
from navigation import DEFAULT_ASSISTANT_MESSAGE, OllamaClient, ASSISTANT_AVATAR

st.set_page_config(layout="wide")


def init():
    if not st.session_state.get("init") or st.session_state.get("logged_out"):
        st.session_state.init = True
        st.session_state.logged_in = False
        st.session_state.logged_out = False
        st.session_state.display_name = None
        st.session_state.user_avatar = ":material/person:"
        st.session_state.assistant_avatar = ASSISTANT_AVATAR
        st.session_state.messages = [DEFAULT_ASSISTANT_MESSAGE]
        st.session_state.chat_id = str(uuid4())
        st.session_state.ollama_client = OllamaClient()
        st.session_state.models = st.session_state.ollama_client.models()
        st.session_state.default_image_payload = {
            "batch_size": 1,
            "cfg_scale": 1,
            "denoising_strength": 0.7,
            "disable_extra_networks": False,
            "do_not_save_grid": False,
            "do_not_save_samples": False,
            "enable_hr": True,
            "height": 450,
            "hr_negative_prompt": "",
            "hr_prompt": "",
            "hr_scale": 2,
            "hr_second_pass_steps": 5,
            "hr_upscaler": "4xNMKDSuperscale_4xNMKDSuperscale",
            "n_iter": 1,
            "override_settings_restore_afterwards": True,
            "prompt": "",
            "restore_faces": False,
            "s_noise": 1.0,
            "s_tmin": 0.0,
            "sampler_name": "DPM++ SDE",
            "seed": -1,
            "steps": 5,
            "width": 800,
        }


def main():
    init()

    login_page = st.Page("navigation/login.py", title="Login", icon=":material/login:")
    settings_page = st.Page(
        "navigation/settings.py", title="Settings", icon=":material/settings:"
    )
    chat_page = st.Page("navigation/chat.py", title="Chat", icon=":material/forum:")

    if st.session_state.logged_in:
        pg = st.navigation([chat_page, settings_page])
    else:
        pg = st.navigation([login_page])

    pg.run()


if __name__ == "__main__":
    main()
