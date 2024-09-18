import streamlit as st
from streamlit_mic_recorder import speech_to_text

state = st.session_state

if 'text_received' not in state:
    state.text_received = []


text = speech_to_text(language='th', use_container_width=True, just_once=True, key='STT')

if text:
    state.text_received.append(text)

for text in state.text_received:
    st.text(text)
