import streamlit as st
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, "..")
sys.path.append(root_dir)

from app.ui_styles import (
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
<div class="glass-card" style="width: fit-content; padding: 50px 80px; text-align: center;">
<p class="problem-title" style="font-size: 30px;">
Streaming algorithms are <span class="highlight-error">broken.</span>
</p>
<p class="problem-desc" style="font-size: 20px;">
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
<div class="glass-card" style="max-width: 1200px; padding: 60px 40px; width: 90%;">

<p class="feature-text" style="font-size: 50px; margin-bottom: 50px;">
From raw songs to your <span class="accent">MLody.</span>
</p>

<div style="display: flex; justify-content: center; align-items: flex-start; gap: 40px; flex-wrap: wrap;">

<div style="width: 250px; text-align: center;">
<div style="font-size: 50px; margin-bottom: 15px;">🔍</div>
<div style="color: #fff; font-size: 24px; font-weight: 700; margin-bottom: 10px;">Seed</div>
<div style="color: #9CA3AF; font-size: 16px; line-height: 1.4;">
Search for a few songs you love (and hate) to establish a baseline.
</div>
</div>

<div style="font-size: 30px; color: #555; padding-top: 10px;">➜</div>

<div style="width: 250px; text-align: center;">
<div style="font-size: 50px; margin-bottom: 15px;">🧪</div>
<div style="color: #fff; font-size: 24px; font-weight: 700; margin-bottom: 10px;">Calibrate</div>
<div style="color: #9CA3AF; font-size: 16px; line-height: 1.4;">
Teach the model your taste. React to quick audio samples to sharpen its accuracy.
</div>
</div>

<div style="font-size: 30px; color: #555; padding-top: 10px;">➜</div>

<div style="width: 250px; text-align: center;">
<div style="font-size: 50px; margin-bottom: 15px;">🧬</div>
<div style="color: #fff; font-size: 24px; font-weight: 700; margin-bottom: 10px;">Evolve</div>
<div style="color: #9CA3AF; font-size: 16px; line-height: 1.4;">
Watch your data evolve into your unique MLody in real-time.
</div>
</div>
</div>

<div style="margin-top: 50px; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: center; gap: 30px; opacity: 0.8; flex-wrap: wrap;">
<span style="color: #ccc;">🎛️ <b>250+</b> Audio Dimensions</span>
<span style="color: #555;">•</span>
<span style="color: #ccc;">⚡ Real-Time</span>
<span style="color: #555;">•</span>
<span style="color: #ccc;">🔒 <b>100%</b> Private</span>
</div>

</div>
<br>
</div>
""",
    unsafe_allow_html=True,
)

_, btn_col, _ = st.columns([1, 1, 1])
with btn_col:
    st.markdown(
        """
        <style>
        .start-listening-btn-wrapper button {
            background: linear-gradient(90deg, #7928CA, #4CD2F0) !important;
            color: white !important;
            border: none !important;
            padding: 12px 30px !important;
            font-size: 18px !important;
            border-radius: 50px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(76, 210, 240, 0.4) !important;
        }
        .start-listening-btn-wrapper button:hover {
            transform: scale(1.05) !important;
            filter: brightness(1.05) !important;
        }
        </style>
        <div class="start-listening-btn-wrapper"></div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Listening 🎧", use_container_width=True, key="start_listening"):
        st.switch_page("pages/build_profile.py")

st.markdown(
    """
<div style="text-align: center; margin-top: 150px; padding: 50px 0; color: #888; border-top: 1px solid #111;">
<p style="margin-bottom: 20px; font-size: 14px;">&copy; 2026 MLody. All rights reserved.</p>
    
<div style="display: flex; justify-content: center; gap: 30px; align-items: center;">
<span class="social-link">
<svg class="social-icon" width="24" height="24" viewBox="0 0 24 24">
<path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
</svg>
</span>
<span class="social-link">
<svg class="social-icon" width="24" height="24" viewBox="0 0 24 24">
<path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
</svg>
</span>
        
<span class="social-link">
<svg class="social-icon" width="24" height="24" viewBox="0 0 24 24">
<path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
</svg>
</span>
</div>
</div>
""",
    unsafe_allow_html=True,
)
