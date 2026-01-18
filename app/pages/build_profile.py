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

    # Summary counts
    likes = len(st.session_state.get("liked_songs", []))
    dislikes = len(st.session_state.get("disliked_songs", []))

    # Complete HTML structure without interruption
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center; padding:40px 0 20px 0;">
            <div class="glass-card" style="max-width:900px; width:100%; padding:40px;">
                <div style="display:flex; gap:40px; align-items:center; flex-wrap: wrap;">
                    <div style="flex:1; min-width:300px; text-align:left;">
                        <h1 style='margin:0; font-size:56px; line-height:1.05; font-weight:800;'>Profile Built.</h1>
                        <p style='margin-top:10px; font-size:20px; color:#cfcfcf;'>Your Audio DNA has been sequenced — we now understand your taste much better.</p>

                        <div style="display:flex; gap:12px; margin-top:22px; flex-wrap:wrap;">
                            <div style="background:rgba(255,255,255,0.03); padding:18px 24px; border-radius:14px; min-width:110px; text-align:center;">
                                <div style="font-size:20px; font-weight:800;">{likes}</div>
                                <div style="font-size:13px; color:#9aa0a6; margin-top:6px;">Likes</div>
                            </div>
                            <div style="background:rgba(255,255,255,0.03); padding:18px 24px; border-radius:14px; min-width:110px; text-align:center;">
                                <div style="font-size:20px; font-weight:800;">{dislikes}</div>
                                <div style="font-size:13px; color:#9aa0a6; margin-top:6px;">Dislikes</div>
                            </div>
                            <div style="background:linear-gradient(90deg,#7928CA,#4CD2F0); padding:18px 24px; border-radius:14px; min-width:200px; text-align:center; color:#000; font-weight:800;">
                                <div style="font-size:16px;">Model Confidence</div>
                                <div style="font-size:20px; margin-top:6px;">High</div>
                            </div>
                        </div>
                    </div>
                    
                    <div style="width:160px; display:flex; align-items:center; justify-content:center;">
                        <div style="width:160px; height:160px; border-radius:20px; background: linear-gradient(135deg,#050505, #0b1220); display:flex; align-items:center; justify-content:center; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
                            <div style="text-align:center;">
                                <div style="font-size:48px; font-weight:900; background: linear-gradient(90deg, #7928CA, #4CD2F0); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">✓</div>
                                <div style="font-size:12px; color:#9aa0a6; margin-top:8px;">Calibration Complete</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Buttons below the card
    st.markdown(
        "<div style='max-width:900px; margin:0 auto; padding:0 40px;'>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([1, 1], gap="medium")
    with c1:
        if st.button("Go to Dashboard", use_container_width=True):
            st.switch_page("pages/2_📊_Dashboard.py")
    with c2:
        if st.button("Recalibrate", use_container_width=True):
            # Reset relevant session state to allow re-calibration
            st.session_state.profile_step = "search"
            st.session_state.intro_done = False
            st.session_state.quiz_intro_done = False
            st.session_state.liked_songs = []
            st.session_state.disliked_songs = []
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
