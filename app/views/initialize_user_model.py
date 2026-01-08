import streamlit as st
import time


def add_song(song, category="liked"):
    target = (
        st.session_state.liked_songs
        if category == "liked"
        else st.session_state.disliked_songs
    )
    # Prevent duplicates
    if not any(s["id"] == song["id"] for s in target):
        target.append(song)
        st.toast(f"Added {song['name']} to {category}!", icon="🎵")


def initialize_user_model(client):
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
            # Use the 'client' passed from the main page
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
                        preview_src = song["preview"] if song["preview"] else ""

                        if preview_src:
                            st.markdown(
                                f"""
                                <audio id="audio_{song['id']}" src="{preview_src}"></audio>
                                
                                <div class="album-wrapper" 
                                     onclick="
                                         var audio = document.getElementById('audio_{song['id']}');
                                         document.querySelectorAll('audio').forEach(el => el.pause()); 
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
                            "💚", key=f"l_{song['id']}", use_container_width=True
                        ):
                            add_song(song, "liked")

                    with c_btn2:
                        st.markdown(
                            '<div style="height: 10px;"></div>', unsafe_allow_html=True
                        )
                        if st.button(
                            "❌", key=f"d_{song['id']}", use_container_width=True
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
