import streamlit as st

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


def render_quiz_step():
    """
    Renders Phase 2: The Calibration Quiz.
    """

    # --- HELPER: NEXT QUESTION ---
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

    # --- MAIN UI ---
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
