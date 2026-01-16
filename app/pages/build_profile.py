import streamlit as st
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, "..")
sys.path.append(root_dir)

from src.audio_client import AudioClient

from app.ui_styles import apply_global_styles, apply_build_profile_styles
from app.views.initialize_user_model import initialize_user_model
from app.views.active_learning import render_quiz_step

st.set_page_config(page_title="Build Profile | MLody", page_icon="🧬", layout="wide")

apply_global_styles()
apply_build_profile_styles()

if "profile_step" not in st.session_state:
    st.session_state.profile_step = "search"
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False
if "liked_songs" not in st.session_state:
    st.session_state.liked_songs = []
if "disliked_songs" not in st.session_state:
    st.session_state.disliked_songs = []
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_intro_done" not in st.session_state:
    st.session_state.quiz_intro_done = False

client = AudioClient()

if st.session_state.profile_step == "search":
    initialize_user_model(client)

elif st.session_state.profile_step == "quiz":
    render_quiz_step(client)

elif st.session_state.profile_step == "complete":
    st.balloons()
    st.markdown(
        """
        <div style="text-align: center; margin-top: 100px;">
            <h1 class="mlody-title" style="font-size: 80px;">Profile Built.</h1>
            <p class="feature-text">Your Audio DNA has been sequenced.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("Go to Dashboard", use_container_width=True):
        st.switch_page("pages/2_📊_Dashboard.py")
