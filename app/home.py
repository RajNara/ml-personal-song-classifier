import streamlit as st
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, "..")
sys.path.append(root_dir)

from src.ui_styles import (
    apply_global_styles,
    apply_landing_page_styles,
    add_home_music_line,
)

st.set_page_config(page_title="MLody", page_icon="🎵", layout="wide")

# apply styles
apply_global_styles()
apply_landing_page_styles()
add_home_music_line()


if "user_data" not in st.session_state:
    st.session_state.user_data = pd.DataFrame()
if "model" not in st.session_state:
    st.session_state.model = None
if "scaler" not in st.session_state:
    st.session_state.scaler = None


st.markdown(
    """
    <div class="scroll-section gradient-bg">
        <div class="floating-element">
            <h1 class="mlody-title">MLody</h1>
        </div>
        <p class="mlody-subtitle">Find your rhythm in the data.</p>
        <div style="margin-top: 50px; animation: bounce 2s infinite; color: #555;">
            ↓ Scroll to discover
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="scroll-section">
        <p class="feature-text">
            Streaming algorithms are <span style="color: #ff3b30;">broken.</span>
        </p>
        <p style="font-size: 24px; color: #6e6e73; max-width: 600px; text-align: center; margin-top: 20px;">
            They rely on what <i>other</i> people like. <br>
            But your ears are unique.
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 1])
st.markdown(
    """
    <div class="scroll-section gradient-bg">
        <p class="feature-text">
            Powered by <span class="accent">Active Learning.</span>
        </p>
        <div style="display: flex; gap: 40px; margin-top: 50px;">
            <div style="text-align: center;">
                <h2 style="font-size: 40px; margin: 0;">250</h2>
                <p style="color: #888;">Decision Trees</p>
            </div>
            <div style="text-align: center;">
                <h2 style="font-size: 40px; margin: 0;">100%</h2>
                <p style="color: #888;">Private (In-Memory)</p>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="scroll-section">
        <p class="feature-text">
            Ready to build your<br>Audio DNA?
        </p>
        <br>
""",
    unsafe_allow_html=True,
)

_, btn_col, _ = st.columns([1, 1, 1])
with btn_col:
    if st.button("Start Listening 🎧", use_container_width=True):
        st.switch_page("pages/1_🧬_Build_Profile.py")

st.markdown("</div>", unsafe_allow_html=True)
