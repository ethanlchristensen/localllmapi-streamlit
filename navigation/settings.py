import streamlit as st

from navigation import DEFAULT_ASSISTANT_MESSAGE


def settings():
    if st.button(
        label=f"Clear **:blue[{len(st.session_state.messages)}]** Messages from the Chat History",
        use_container_width=True,
    ):
        st.session_state.messages = [DEFAULT_ASSISTANT_MESSAGE]
        st.rerun()


settings()
