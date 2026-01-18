import streamlit as st
import time
import sys
from pathlib import Path

# Add parent directory to path to import particles
sys.path.insert(0, str(Path(__file__).parent.parent))
from particles import render_particles


# --- TARGET DIAGNOSTIC SONGS (ordered) ---
TARGET_SONGS = [
    {
        "name": "Levitating",
        "artist": "Dua Lipa (feat. DaBaby)",
        "deezer_id": 1124841752,
    },
    {
        "name": "The Less I Know the Better",
        "artist": "Tame Impala",
        "deezer_id": 103052662,
    },
    {"name": "HUMBLE.", "artist": "Kendrick Lamar", "deezer_id": 350171311},
    {"name": "Pretty Girl", "artist": "Clairo", "deezer_id": 3422603071},
    {
        "name": "Get Lucky",
        "artist": "Daft Punk (feat. Pharrell Williams)",
        "deezer_id": 67238735,
    },
    {"name": "Motion Sickness", "artist": "Phoebe Bridgers", "deezer_id": 397301582},
    {"name": "Do I Wanna Know?", "artist": "Arctic Monkeys", "deezer_id": 70322130},
    {"name": "Awake", "artist": "Tycho", "deezer_id": 71452919},
    {"name": "I'm Not Alone", "artist": "Calvin Harris", "deezer_id": 69304060},
    {"name": "bad guy", "artist": "Billie Eilish", "deezer_id": 655095912},
]


def render_quiz_step(client):
    """
    Renders Phase 2: The Calibration Quiz.

    Uses the provided `client` (AudioClient) to look up preview URLs and artwork
    for each target track. The Deezer preview API provides short previews (typically
    30s). If no preview is found, a warning will be shown.
    """

    # Show intro messages before the quiz starts
    if not st.session_state.get("quiz_intro_done"):
        # Add particles background
        if "particles_config" not in st.session_state:
            st.session_state.particles_config = None

        particles_html, st.session_state.particles_config = render_particles(
            st.session_state.particles_config
        )
        st.markdown(particles_html, unsafe_allow_html=True)

        st.markdown(
            """
            <div class="pulse-container">
                <div class="pulse-circle pulse-1"></div>
                <div class="pulse-circle pulse-2"></div>
                <div class="pulse-circle pulse-3"></div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        placeholder = st.empty()
        messages = [
            "Time to calibrate your taste.",
            "You'll hear 10 songs.",
            "Tell us if you like them or not.",
        ]
        for msg in messages:
            placeholder.empty()
            time.sleep(0.1)
            placeholder.markdown(
                f"""<div class="intro-container"><h1 class="intro-text">{msg}</h1></div>""",
                unsafe_allow_html=True,
            )
            time.sleep(3.5)
        placeholder.empty()
        st.session_state.quiz_intro_done = True
        st.rerun()

    # initialize cached diag tracks on first run
    if "diag_tracks" not in st.session_state:
        st.session_state.diag_tracks = []
        for i, t in enumerate(TARGET_SONGS):
            # If we have an explicit Deezer track id, prefer the track lookup (exact version)
            if t.get("deezer_id"):
                data = None
                try:
                    data = client.get_track(t["deezer_id"])
                except Exception:
                    data = None

                if data:
                    song = {
                        "id": data.get("trackId") or f"diag_{i}",
                        "name": data.get("trackName") or t["name"],
                        "artist": data.get("artistName") or t["artist"],
                        "img": data.get("artworkUrl100", "https://placehold.co/100"),
                        "preview": data.get("previewUrl"),
                    }
                    st.session_state.diag_tracks.append(song)
                    continue

            # fallback: simple search (take first result)
            query = f"{t['name']} {t['artist']}"
            results = []
            try:
                results = client.search_tracks(query, limit=1)
            except Exception:
                results = []

            if results:
                r = results[0]
                song = {
                    "id": r.get("trackId") or f"diag_{i}",
                    "name": r.get("trackName") or t["name"],
                    "artist": r.get("artistName") or t["artist"],
                    "img": r.get("artworkUrl100", "https://placehold.co/100"),
                    "preview": r.get("previewUrl"),
                }

            st.session_state.diag_tracks.append(song)

    # helper to advance
    def next_question(liked):
        current = st.session_state.diag_tracks[st.session_state.quiz_index]
        song_data = {
            "id": current["id"],
            "name": current["name"],
            "artist": current["artist"],
            "img": current.get("img", "https://placehold.co/100"),
            "preview": current.get("preview"),
        }

        if liked:
            st.session_state.liked_songs.append(song_data)
        else:
            st.session_state.disliked_songs.append(song_data)

        if st.session_state.quiz_index < len(st.session_state.diag_tracks) - 1:
            st.session_state.quiz_index += 1
            st.rerun()
        else:
            st.session_state.profile_step = "complete"
            st.rerun()

    # --- MAIN UI ---
    current_song = st.session_state.diag_tracks[st.session_state.quiz_index]
    progress = (st.session_state.quiz_index + 1) / len(st.session_state.diag_tracks)

    # Floating particles background - maintain same particles across reruns
    if "quiz_particles_config" not in st.session_state:
        st.session_state.quiz_particles_config = None

    particles_html, st.session_state.quiz_particles_config = render_particles(
        st.session_state.quiz_particles_config
    )
    st.markdown(particles_html, unsafe_allow_html=True)

    _, main_col, _ = st.columns([1, 2, 1])

    with main_col:
        # Calculate gradient position that grows with progress
        # The gradient colors should only appear in the filled portion
        gradient_start = 0
        gradient_end = progress * 100

        # Modern progress bar - black background, gradient only shows as it grows
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="font-size: 24px; font-weight: 600; color: #4CD2F0; margin: 0 0 20px 0;">Calibration: Song {st.session_state.quiz_index + 1} of {len(st.session_state.diag_tracks)}</h2>
                <div style="position: relative; width: 100%; height: 8px; background: #0a0a0a; border-radius: 10px; overflow: hidden; border: 1px solid rgba(255,255,255,0.15);">
                    <div style="position: absolute; left: 0; top: 0; height: 100%; width: {progress * 100}%; background: linear-gradient(to right, #1E90FF 0%, #4CD2F0 33%, #9D50BB 66%, #FF1493 100%); background-size: {100/progress if progress > 0 else 100}% 100%; background-position: left; border-radius: 10px; transition: width 0.3s ease; box-shadow: 0 0 15px rgba(76, 210, 240, 0.6);"></div>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Centered card + more professional header
        st.markdown(
            f"""
            <div style="text-align:center; padding: 10px 0;">
                <h2 style="color: #ccc; font-weight: 500; margin-bottom: 8px; font-size:18px;">Do you like this song?</h2>
                <h1 style="font-size:28px; margin: 0;">{current_song['name']}</h1>
                <p style="color: #4CD2F0; font-size:14px; margin-top:4px;">{current_song['artist']}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # artwork centered
        if current_song.get("img"):
            st.markdown(
                f"<div style='text-align:center; margin-bottom:8px;'><img src=\"{current_song['img']}\" style=\"width:120px; border-radius:6px;\" /></div>",
                unsafe_allow_html=True,
            )

        # Audio player - manual play for first song, autoplay for rest
        if current_song.get("preview"):
            # Only autoplay after the first song
            autoplay_attr = "" if st.session_state.quiz_index == 0 else "autoplay"
            st.markdown(
                f"<div style='text-align:center; margin-bottom:6px;'><audio controls {autoplay_attr} src=\"{current_song['preview']}\" style=\"width:100%; max-width:520px;\">Your browser does not support the audio element.</audio></div>",
                unsafe_allow_html=True,
            )
        else:
            st.warning("No audio preview available for this track.")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Buttons: flipped (Yes on left), Yes = green (primary), No = red (secondary)
        c_yes, c_no = st.columns([1, 1])
        with c_yes:
            if st.button(
                "💚 Yes",
                key=f"like_diag_{current_song['id']}",
                type="primary",
                use_container_width=True,
            ):
                next_question(liked=True)
        with c_no:
            if st.button(
                "👎 No",
                key=f"dislike_diag_{current_song['id']}",
                type="secondary",
                use_container_width=True,
            ):
                next_question(liked=False)
