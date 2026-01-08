import streamlit as st
import time


def add_song(song, category):
    target = (
        st.session_state.liked_songs
        if category == "liked"
        else st.session_state.disliked_songs
    )
    if not any(s["id"] == song["id"] for s in target):
        target.append(song)
        st.toast(f"Sequenced: {song['name']}", icon="🧬")


def remove_song(song_id, category):
    target = (
        st.session_state.liked_songs
        if category == "liked"
        else st.session_state.disliked_songs
    )
    st.session_state[f"{category}_songs"] = [s for s in target if s["id"] != song_id]
    st.rerun()


def initialize_user_model(client):
    # --- INTRO SEQUENCE ---
    if not st.session_state.intro_done:
        placeholder = st.empty()
        messages = [
            "Initializing your personal model...",
            "We need some baseline data.",
            "Let's start with what you know.",
        ]
        for msg in messages:
            placeholder.empty()
            time.sleep(0.1)
            placeholder.markdown(
                f"""<div class="intro-container"><h1 class="intro-text">{msg}</h1></div>""",
                unsafe_allow_html=True,
            )
            time.sleep(3)
        placeholder.empty()
        st.session_state.intro_done = True
        st.rerun()

    # --- LAYOUT ---
    # Using a 60/40 split for a "Dashboard" feel
    left_col, right_col = st.columns([1.6, 1], gap="large")

    # ==========================
    # LEFT: SEARCH INTERFACE
    # ==========================
    with left_col:
        st.markdown(
            """
            <h1 style='font-size: 48px; font-weight: 800; margin-bottom: 0px;'>
                <span style='color:white'>Build your</span> <span class='highlight'>DNA</span> 🧬
            </h1>
            <p style='color: #888; font-size: 16px; margin-bottom: 30px;'>
                Search for tracks to establish your baseline audio profile.
            </p>
        """,
            unsafe_allow_html=True,
        )

        # Search Bar
        search_query = st.text_input(
            "Search", placeholder="Search for a track...", label_visibility="collapsed"
        )

        # Results Area
        if search_query:
            st.markdown("<br>", unsafe_allow_html=True)
            results = client.search_tracks(
                search_query, limit=4
            )  # Increased limit slightly

            if not results:
                st.info("No tracks found. Try a different spelling.")

            for item in results:
                song = {
                    "id": item.get("trackId"),
                    "name": item.get("trackName"),
                    "artist": item.get("artistName"),
                    "img": item.get(
                        "artworkUrl100", "https://placehold.co/80"
                    ),  # standard size
                    "preview": item.get("previewUrl"),
                }

                # --- RESULT CARD ---
                with st.container():
                    # Layout: Image | Info | Buttons
                    c1, c2, c3, c4 = st.columns([1.2, 3.5, 1, 1])

                    with c1:
                        # Audio Player logic
                        if song["preview"]:
                            st.markdown(
                                f"""
                                <audio id="aud_{song['id']}" src="{song['preview']}"></audio>
                                <div class="album-wrapper" onclick="document.getElementById('aud_{song['id']}').play()">
                                    <img src="{song['img']}" class="album-img">
                                    <div class="play-overlay"><div class="play-icon">▶</div></div>
                                </div>
                            """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.image(song["img"], width=80)

                    with c2:
                        st.markdown(
                            f"""
                            <div style="padding-top: 10px;">
                                <div style="font-size: 18px; font-weight: 600; color: #fff;">{song['name']}</div>
                                <div style="font-size: 14px; color: #4CD2F0;">{song['artist']}</div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    # Action Buttons
                    with c3:
                        st.markdown(
                            '<div style="height: 15px;"></div>', unsafe_allow_html=True
                        )
                        if st.button(
                            "💚",
                            key=f"add_l_{song['id']}",
                            help="Add to Vibes",
                            use_container_width=True,
                        ):
                            add_song(song, "liked")

                    with c4:
                        st.markdown(
                            '<div style="height: 15px;"></div>', unsafe_allow_html=True
                        )
                        if st.button(
                            "❌",
                            key=f"add_d_{song['id']}",
                            help="Add to Filter",
                            use_container_width=True,
                        ):
                            add_song(song, "disliked")

                # Divider
                st.markdown(
                    '<hr style="border-color: rgba(255,255,255,0.05); margin: 15px 0;">',
                    unsafe_allow_html=True,
                )

    # ==========================
    # RIGHT: DNA DASHBOARD
    # ==========================
    with right_col:
        # We use a container to create a background panel effect
        with st.container(border=True):
            # --- POSITIVE SIGNAL SECTION ---
            st.markdown(
                '<div class="panel-header-pos">💚 Positive Signal</div>',
                unsafe_allow_html=True,
            )

            if not st.session_state.liked_songs:
                st.markdown(
                    """
                    <div style="text-align: center; padding: 20px; color: #444; border: 1px dashed #333; border-radius: 10px;">
                        Waiting for input...
                    </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                for s in st.session_state.liked_songs:
                    # Using columns inside the container for the "Capsule" look
                    # Note: We can't put buttons inside HTML, so we use columns
                    cap_c1, cap_c2, cap_c3 = st.columns([0.8, 3, 0.5])
                    with cap_c1:
                        st.image(s["img"], width=40)
                    with cap_c2:
                        st.markdown(
                            f"""
                            <div style="line-height: 1.2; margin-top: 2px;">
                                <div style="font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{s['name']}</div>
                                <div style="font-size: 11px; color: #888;">{s['artist']}</div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    with cap_c3:
                        if st.button("✖", key=f"rem_l_{s['id']}", help="Remove"):
                            remove_song(s["id"], "liked")

                    st.markdown(
                        '<div style="height: 5px;"></div>', unsafe_allow_html=True
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            # --- NEGATIVE SIGNAL SECTION ---
            st.markdown(
                '<div class="panel-header-neg">❌ Negative Noise</div>',
                unsafe_allow_html=True,
            )

            if not st.session_state.disliked_songs:
                st.markdown(
                    """
                    <div style="text-align: center; padding: 20px; color: #444; border: 1px dashed #333; border-radius: 10px;">
                        Optional filter...
                    </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                for s in st.session_state.disliked_songs:
                    cap_c1, cap_c2, cap_c3 = st.columns([0.8, 3, 0.5])
                    with cap_c1:
                        st.image(s["img"], width=40)
                    with cap_c2:
                        st.markdown(
                            f"""
                            <div style="line-height: 1.2; margin-top: 2px;">
                                <div style="font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{s['name']}</div>
                                <div style="font-size: 11px; color: #888;">{s['artist']}</div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    with cap_c3:
                        if st.button("✖", key=f"rem_d_{s['id']}", help="Remove"):
                            remove_song(s["id"], "disliked")

                    st.markdown(
                        '<div style="height: 5px;"></div>', unsafe_allow_html=True
                    )

        # --- ACTION FOOTER ---
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            "🧬 Sequence & Calibrate ➡️", use_container_width=True, type="primary"
        ):
            if len(st.session_state.liked_songs) < 1:
                st.error("Insufficent DNA. Add at least 1 liked song.")
            else:
                st.session_state.profile_step = "quiz"
                st.rerun()
