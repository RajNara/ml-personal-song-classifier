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
    <div class="scroll-section">
        <div class="floating-element">
            <h1 class="mlody-title" style="font-size: 8rem; font-weight: 800; color: #ffffff; text-shadow: 0 2px 4px rgba(255,255,255,0.3);">
                <span class="highlight" style="color: #ffffff;">ML</span><span class="standard-text" style="color: #ffffff;">ody</span>
            </h1>
        </div>
        <p class="mlody-subtitle" style="font-size: 2rem; color: #cccccc;">Find your rhythm in the data.</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="scroll-section">
        <div class="scroll-entrance-wrapper">
            <div class="glass-card style="width: 100%;"">
                <p class="problem-title">
                    Streaming algorithms are <span class="highlight-error">broken.</span>
                </p>
                <p class="problem-desc">
                    They rely on what <i>everyone else</i> likes.<br>
                    But your ears are unique. Why settle for an average?
                </p>
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
        st.switch_page("pages/build_profile.py")

st.markdown("</div>", unsafe_allow_html=True)
