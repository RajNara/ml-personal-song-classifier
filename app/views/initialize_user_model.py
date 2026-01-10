import streamlit as st
import time
import requests


def initialize_user_model(client):
    """
    Renders Phase 1: Search & Seed.
    """

    # --- LOGIC ---
    def remove_song(song_id, category="liked"):
        target = (
            st.session_state.liked_songs
            if category == "liked"
            else st.session_state.disliked_songs
        )
        st.session_state[f"{category}_songs"] = [
            s for s in target if s["id"] != song_id
        ]
        st.rerun()

    def add_song(song, category="liked"):
        target = (
            st.session_state.liked_songs
            if category == "liked"
            else st.session_state.disliked_songs
        )
        if not any(s["id"] == song["id"] for s in target):
            target.append(song)
            st.toast(f"Added {song['name']} to {category}", icon="✅")

    # --- INTRO SEQUENCE (WITH PULSE) ---
    if not st.session_state.intro_done:
        # We inject the pulse container ONLY during the intro
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
            time.sleep(3.5)
        placeholder.empty()
        st.session_state.intro_done = True
        st.rerun()

    # --- PAGE FADE IN ---
    if "has_faded_in" not in st.session_state:
        st.session_state.has_faded_in = False
    if not st.session_state.has_faded_in:
        st.markdown(
            """<style>.block-container { animation: fadeInPage 3s ease-in-out forwards; }</style>""",
            unsafe_allow_html=True,
        )
        st.session_state.has_faded_in = True

    # ==========================
    # MAIN SPLIT-SCREEN LAYOUT
    # ==========================
    # Header spanning both columns
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style='margin:0;'>Build your Profile 🧬</h1>
            <p style='color: #888; margin-top:5px;'>Search for songs to establish your baseline.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # CREATE TWO COLUMNS
    col_search, col_dashboard = st.columns([1.5, 1], gap="large")

    # ---------------------------------------------------------
    # LEFT COLUMN: SEARCH
    # ---------------------------------------------------------
    with col_search:
        search_query = st.text_input(
            "Search", placeholder="Type a song name...", label_visibility="collapsed"
        )

        if search_query:
            st.markdown("<br>", unsafe_allow_html=True)
            results = client.search_tracks(search_query, limit=3)

            if not results:
                st.info("No tracks found.")

            for item in results:
                song = {
                    "id": item.get("trackId"),
                    "name": item.get("trackName"),
                    "artist": item.get("artistName"),
                    "img": item.get("artworkUrl100", "https://placehold.co/100"),
                    "preview": item.get("previewUrl"),
                }

                # Result Card Layout
                c_img, c_info, c_like, c_dislike = st.columns(
                    [1.5, 4, 1.2, 1.2], vertical_alignment="center"
                )

                with c_img:
                    st.image(song["img"], width=80)

                with c_info:
                    st.markdown(f"**{song['name']}**")
                    st.caption(song["artist"])
                    if song["preview"]:
                        st.audio(song["preview"], format="audio/mp4")

                with c_like:
                    if st.button(
                        "👍",
                        key=f"l_{song['id']}",
                        type="primary",
                        use_container_width=True,
                    ):
                        add_song(song, "liked")

                with c_dislike:
                    if st.button(
                        "👎",
                        key=f"d_{song['id']}",
                        type="secondary",
                        use_container_width=True,
                    ):
                        add_song(song, "disliked")

                st.markdown('<hr class="sleek-divider">', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # RIGHT COLUMN: DASHBOARD (SELECTIONS)
    # ---------------------------------------------------------
    with col_dashboard:
        # Wrap the dashboard in a container for a "Card" look
        with st.container(border=True):
            st.markdown(
                "<h4 style='text-align:center;'>Your Selections</h4>",
                unsafe_allow_html=True,
            )

            # 1. Liked Section
            st.markdown("##### 💚 My Vibe")
            if not st.session_state.liked_songs:
                st.markdown(
                    "<div style='color:#666; font-style:italic; font-size:14px;'>No songs added yet...</div>",
                    unsafe_allow_html=True,
                )
            else:
                for s in st.session_state.liked_songs:
                    r1, r2 = st.columns([5, 1], vertical_alignment="center")
                    r1.markdown(
                        f"<div style='font-size:14px;'>{s['name']} <span style='color:#888'>- {s['artist']}</span></div>",
                        unsafe_allow_html=True,
                    )
                    if r2.button("✖", key=f"rem_l_{s['id']}"):
                        remove_song(s["id"], "liked")

            st.markdown("<hr style='opacity:0.3'>", unsafe_allow_html=True)

            # 2. Disliked Section
            st.markdown("##### ❌ Blocked")
            if not st.session_state.disliked_songs:
                st.markdown(
                    "<div style='color:#666; font-style:italic; font-size:14px;'>No songs added yet...</div>",
                    unsafe_allow_html=True,
                )
            else:
                for s in st.session_state.disliked_songs:
                    r1, r2 = st.columns([5, 1], vertical_alignment="center")
                    r1.markdown(
                        f"<div style='font-size:14px;'>{s['name']} <span style='color:#888'>- {s['artist']}</span></div>",
                        unsafe_allow_html=True,
                    )
                    if r2.button("✖", key=f"rem_d_{s['id']}"):
                        remove_song(s["id"], "disliked")

            st.markdown("<br>", unsafe_allow_html=True)

            # 3. Next Step Action
            if st.button(
                "Analyze & Continue ➡️", type="primary", use_container_width=True
            ):
                if not st.session_state.liked_songs:
                    st.error("Please add at least one liked song.")
                else:
                    st.session_state.profile_step = "quiz"
                    st.rerun()
