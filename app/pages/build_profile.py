import streamlit as st
import pandas as pd
import time
import os
import sys

# Path Setup
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, "..", "..")
sys.path.append(root_dir)

# --- IMPORTS ---
from app.ui_styles import apply_global_styles, apply_landing_page_styles
from src.audio_client import AudioClient

# --- PAGE CONFIG ---
st.set_page_config(page_title="Build Profile | MLody", page_icon="🧬", layout="wide")
apply_global_styles()
apply_landing_page_styles()

# --- INJECT CSS FOR ALBUM ART HOVER ---
# We inject this directly here to guarantee the hover effect works
# regardless of what is in ui_styles.py
st.markdown(
    """
    <style>
        /* CSS FOR THE ALBUM HOVER EFFECT */
        .album-wrapper {
            position: relative;
            width: 70px;
            height: 70px;
            border-radius: 8px;
            overflow: hidden;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: transform 0.2s ease;
        }
        .album-wrapper:hover {
            transform: scale(1.05);
        }
        
        /* The Image */
        .album-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
        
        /* The Overlay (Hidden by default) */
        .play-overlay {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.2s ease;
        }
        
        /* Show Overlay on Hover */
        .album-wrapper:hover .play-overlay {
            opacity: 1;
        }
        
        /* The Play Icon */
        .play-icon {
            font-size: 24px;
            color: white;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.8));
        }
    </style>
""",
    unsafe_allow_html=True,
)


# --- SESSION STATE INIT ---
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

# --- INIT AUDIO CLIENT ---
client = AudioClient()

# --- DIAGNOSTIC SONGS ---
DIAGNOSTIC_SONGS = [
    {
        "name": "Bohemian Rhapsody",
        "artist": "Queen",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview115/v4/4a/02/33/4a023308-c8b1-362c-850d-6a58a939f605/mzaf_6765793086383637845.plus.aac.p.m4a",
    },
    {
        "name": "Sicko Mode",
        "artist": "Travis Scott",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview115/v4/4e/c9/28/4ec92815-5e6e-3151-692a-74dfa96860d5/mzaf_995276662479906429.plus.aac.p.m4a",
    },
    {
        "name": "Shape of You",
        "artist": "Ed Sheeran",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview125/v4/e5/23/c3/e523c348-7359-573e-329b-90f7d6df8326/mzaf_7302458421882834079.plus.aac.p.m4a",
    },
]


# --- HELPERS ---
def add_song(song, category="liked"):
    target = (
        st.session_state.liked_songs
        if category == "liked"
        else st.session_state.disliked_songs
    )
    if not any(s["id"] == song["id"] for s in target):
        target.append(song)
        st.toast(f"Added {song['name']} to {category}!", icon="🎵")


def next_question(liked):
    current_song = DIAGNOSTIC_SONGS[st.session_state.quiz_index]
    song_data = {
        "id": f"diag_{st.session_state.quiz_index}",
        "name": current_song["name"],
        "artist": current_song["artist"],
        "img": "https://placehold.co/100",
        "preview": current_song.get("preview_url"),
    }

    if liked:
        st.session_state.liked_songs.append(song_data)
    else:
        st.session_state.disliked_songs.append(song_data)

    if st.session_state.quiz_index < len(DIAGNOSTIC_SONGS) - 1:
        st.session_state.quiz_index += 1
        st.rerun()
    else:
        st.session_state.profile_step = "complete"
        st.rerun()


# ==========================================
# PHASE 1: SEARCH & BUILD
# ==========================================
if st.session_state.profile_step == "search":
    # --- INTRO SEQUENCE (Runs Once) ---
    if not st.session_state.intro_done:
        placeholder = st.empty()
        messages = [
            "Initializing your personal model...",
            "We need some baseline data.",
            "Let's start with what you know.",
        ]

        for i, msg in enumerate(messages):
            placeholder.empty()
            time.sleep(0.1)
            placeholder.markdown(
                f"""
                <div class="intro-container">
                    <h1 id="msg-{i}" class="intro-text">{msg}</h1>
                </div>
            """,
                unsafe_allow_html=True,
            )
            time.sleep(3.5)

        placeholder.empty()
        st.session_state.intro_done = True
        st.rerun()

    # --- MAIN SPLIT LAYOUT ---
    left_col, right_col = st.columns([1.4, 1], gap="large")

    # === LEFT COLUMN: SEARCH ===
    with left_col:
        st.markdown(
            """
            <h1 style='font-size: 50px; margin-bottom: 0px;'>Build your DNA 🧬</h1>
            <p style='color: #888; font-size: 18px; margin-bottom: 20px;'>Search for songs to build your baseline model.</p>
        """,
            unsafe_allow_html=True,
        )

        search_query = st.text_input(
            "Search for a song...",
            placeholder="Type 'Starboy' or 'Daft Punk'...",
            label_visibility="collapsed",
        )

        if search_query:
            st.markdown("<br>", unsafe_allow_html=True)
            raw_results = client.search_tracks(search_query, limit=3)

            for item in raw_results:
                song = {
                    "id": item.get("trackId"),
                    "name": item.get("trackName"),
                    "artist": item.get("artistName"),
                    "img": item.get("artworkUrl100", "https://placehold.co/100"),
                    "preview": item.get("previewUrl"),
                }

                # GLASS STRIP UI
                with st.container():
                    c_img, c_info, c_btn1, c_btn2 = st.columns([1, 3.5, 1.2, 1.2])

                    with c_img:
                        # --- ROBUST AUDIO PLAYER ---
                        # 1. We inject an invisible audio tag
                        preview_src = song["preview"] if song["preview"] else ""

                        if preview_src:
                            st.markdown(
                                f"""
                                <audio id="audio_{song['id']}" src="{preview_src}"></audio>
                                
                                <div class="album-wrapper" 
                                     onclick="
                                        var audio = document.getElementById('audio_{song['id']}');
                                        // Stop all other audio
                                        document.querySelectorAll('audio').forEach(el => el.pause()); 
                                        // Play this one
                                        if (audio) audio.play();
                                     "
                                     title="Click to preview">
                                    <img src="{song['img']}" class="album-img">
                                    <div class="play-overlay">
                                        <div class="play-icon">▶</div>
                                    </div>
                                </div>
                            """,
                                unsafe_allow_html=True,
                            )
                        else:
                            # Fallback if no preview (just image)
                            st.image(song["img"], width=70)

                    with c_info:
                        st.markdown(
                            f"""
                            <div style="display: flex; flex-direction: column; justify-content: center; height: 70px;">
                                <div class="track-name" style="font-size: 18px;">{song['name']}</div>
                                <div class="track-artist" style="font-size: 14px;">{song['artist']}</div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with c_btn1:
                        st.markdown(
                            '<div style="height: 10px;"></div>', unsafe_allow_html=True
                        )
                        if st.button(
                            "💚",
                            key=f"l_{song['id']}",
                            help="Like this song",
                            use_container_width=True,
                        ):
                            add_song(song, "liked")

                    with c_btn2:
                        st.markdown(
                            '<div style="height: 10px;"></div>', unsafe_allow_html=True
                        )
                        if st.button(
                            "❌",
                            key=f"d_{song['id']}",
                            help="Dislike this song",
                            use_container_width=True,
                        ):
                            add_song(song, "disliked")

                st.markdown(
                    '<hr style="border-color: rgba(255,255,255,0.08); margin: 8px 0 16px 0;">',
                    unsafe_allow_html=True,
                )

    # === RIGHT COLUMN: LISTS ===
    with right_col:
        # 1. LIKES
        st.markdown("### 💚 Your Vibes")
        with st.container(border=True):
            if not st.session_state.liked_songs:
                st.info("Search for songs to add them here.")
            else:
                cols = st.columns(3)
                for i, song in enumerate(st.session_state.liked_songs):
                    with cols[i % 3]:
                        st.image(
                            song.get("img", "https://placehold.co/100"),
                            use_container_width=True,
                        )
                        st.markdown(
                            f"<div style='font-size: 12px; line-height: 1.2; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{song['name']}</div>",
                            unsafe_allow_html=True,
                        )

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. DISLIKES
        st.markdown("### ❌ Hard Pass")
        with st.container(border=True):
            if not st.session_state.disliked_songs:
                st.caption("Optional: Add songs you hate to refine the model.")
            else:
                cols = st.columns(3)
                for i, song in enumerate(st.session_state.disliked_songs):
                    with cols[i % 3]:
                        st.image(
                            song.get("img", "https://placehold.co/100"),
                            use_container_width=True,
                        )
                        st.markdown(
                            f"<div style='font-size: 12px; line-height: 1.2; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{song['name']}</div>",
                            unsafe_allow_html=True,
                        )

    # --- FOOTER ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, center_btn, _ = st.columns([1, 1, 1])
    if center_btn.button(
        "Analyze & Calibrate ➡️", use_container_width=True, type="primary"
    ):
        if len(st.session_state.liked_songs) < 1:
            st.error("Please add at least 1 song you like!")
        else:
            st.session_state.profile_step = "quiz"
            st.rerun()

# ==========================================
# PHASE 2: THE QUIZ
# ==========================================
elif st.session_state.profile_step == "quiz":
    current_song = DIAGNOSTIC_SONGS[st.session_state.quiz_index]
    progress = (st.session_state.quiz_index + 1) / len(DIAGNOSTIC_SONGS)

    _, main_col, _ = st.columns([1, 2, 1])

    with main_col:
        st.progress(
            progress,
            text=f"Calibration: Song {st.session_state.quiz_index + 1} of {len(DIAGNOSTIC_SONGS)}",
        )

        st.markdown(
            f"""
            <div class="quiz-card">
                <h2 style="color: #ccc; font-weight: 300; margin-bottom: 30px;">Do you vibe with this?</h2>
                <h1 style="font-size: 40px; margin: 0;">{current_song['name']}</h1>
                <p style="color: #4CD2F0; font-size: 24px;">{current_song['artist']}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        if "preview_url" in current_song:
            st.audio(current_song["preview_url"], format="audio/mp4")
        else:
            st.warning("No audio preview available for this track.")

        st.markdown("<br>", unsafe_allow_html=True)

        c_no, c_yes = st.columns(2)
        with c_no:
            if st.button("👎 No", use_container_width=True):
                next_question(liked=False)
        with c_yes:
            if st.button("💚 Yes", use_container_width=True):
                next_question(liked=True)

# ==========================================
# PHASE 3: COMPLETE
# ==========================================
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
