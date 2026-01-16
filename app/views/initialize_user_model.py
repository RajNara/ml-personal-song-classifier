import streamlit as st
import time


def initialize_user_model(client):
    """
    Renders Phase 1: Search & Seed.
    Uses a form-based search to prevent duplicate widget issues.
    """

    # --- HELPER FUNCTIONS ---
    def remove_song(song_id, category="liked"):
        target_key = f"{category}_songs"
        st.session_state[target_key] = [
            s for s in st.session_state[target_key] if s["id"] != song_id
        ]

    def add_song(song, category="liked"):
        target_key = f"{category}_songs"
        target = st.session_state[target_key]
        # Prevent cross-list duplicates: if song exists in the opposite list, show an error
        if category == "disliked":
            if any(
                s["id"] == song["id"] for s in st.session_state.get("liked_songs", [])
            ):
                st.error(
                    "This song is already in My Vibe. Remove it there before blocking."
                )
                return
        elif category == "liked":
            if any(
                s["id"] == song["id"]
                for s in st.session_state.get("disliked_songs", [])
            ):
                st.error(
                    "This song is already in Blocked. Remove it there before liking."
                )
                return

        if not any(s["id"] == song["id"] for s in target):
            target.append(song)
            st.toast(f"Added {song['name']} to {category}", icon="✅")

    # --- INTRO SEQUENCE ---
    if not st.session_state.intro_done:
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

    # --- PAGE HEADER ---
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style='margin:0;'>Build your Profile 🧬</h1>
            <p style='color: #888; margin-top:5px;'>Search for songs to establish your baseline.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # --- TWO COLUMN LAYOUT ---
    col_search, col_dashboard = st.columns([1.5, 1], gap="large")

    # ---------------------------------------------------------
    # LEFT COLUMN: SEARCH (using a form to prevent rerun issues)
    # ---------------------------------------------------------
    with col_search:
        # Use a form to handle search submission cleanly
        with st.form(key="search_form", clear_on_submit=False):
            search_query = st.text_input(
                "Search",
                placeholder="Type a song name...",
                label_visibility="collapsed",
            )
            search_submitted = st.form_submit_button(
                "Search 🔍", use_container_width=True
            )

        # Store search query in session state for persistence
        if search_submitted and search_query:
            st.session_state.current_search = search_query

        # Display results if we have a search
        current_query = st.session_state.get("current_search", "")

        if current_query:
            results = client.search_tracks(current_query, limit=3)

            if not results:
                st.info("No tracks found.")
            else:
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
                            key=f"like_{song['id']}",
                            type="primary",
                            use_container_width=True,
                        ):
                            add_song(song, "liked")
                            st.rerun()

                    with c_dislike:
                        if st.button(
                            "👎",
                            key=f"dislike_{song['id']}",
                            type="secondary",
                            use_container_width=True,
                        ):
                            add_song(song, "disliked")
                            st.rerun()

                    st.markdown('<hr class="sleek-divider">', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # RIGHT COLUMN: DASHBOARD
    # ---------------------------------------------------------
    with col_dashboard:
        with st.container(border=True):
            st.markdown(
                "<h4 style='text-align:center; margin-bottom: 20px;'>Your Selections</h4>",
                unsafe_allow_html=True,
            )

            # Liked Section (larger text, left-aligned)
            st.markdown(
                "<div style='font-size:18px; font-weight:700; margin-top:6px;'>💚 My Vibe</div>",
                unsafe_allow_html=True,
            )
            if not st.session_state.liked_songs:
                st.markdown(
                    "<div style='color:#666; font-style:italic; font-size:14px;'>No songs added yet...</div>",
                    unsafe_allow_html=True,
                )
            else:
                for i, s in enumerate(st.session_state.liked_songs):
                    r1, r2 = st.columns([5, 1], vertical_alignment="center")
                    r1.markdown(
                        f"<div style='text-align:left;'><div style='font-size:16px; font-weight:600;'>{s['name']}</div><div style='font-size:13px; color:#888; margin-top:4px;'>{s['artist']}</div></div>",
                        unsafe_allow_html=True,
                    )
                    with r2:
                        st.markdown("<div class='remove-btn'>", unsafe_allow_html=True)
                        if st.button("✕", key=f"remove_liked_{s['id']}"):
                            remove_song(s["id"], "liked")
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                    # faint divider between items
                    if i < len(st.session_state.liked_songs) - 1:
                        st.markdown(
                            '<hr style="opacity:0.18; margin:12px 0; border:none; height:1px; background:rgba(255,255,255,0.06);">',
                            unsafe_allow_html=True,
                        )

            st.markdown("<hr style='opacity:0.3'>", unsafe_allow_html=True)

            # Disliked Section (larger text, left-aligned)
            st.markdown(
                "<div style='font-size:18px; font-weight:700; margin-top:12px;'>❌ Blocked</div>",
                unsafe_allow_html=True,
            )
            if not st.session_state.disliked_songs:
                st.markdown(
                    "<div style='color:#666; font-style:italic; font-size:14px;'>No songs added yet...</div>",
                    unsafe_allow_html=True,
                )
            else:
                for i, s in enumerate(st.session_state.disliked_songs):
                    r1, r2 = st.columns([5, 1], vertical_alignment="center")
                    r1.markdown(
                        f"<div style='text-align:left;'><div style='font-size:16px; font-weight:600;'>{s['name']}</div><div style='font-size:13px; color:#888; margin-top:4px;'>{s['artist']}</div></div>",
                        unsafe_allow_html=True,
                    )
                    with r2:
                        st.markdown("<div class='remove-btn'>", unsafe_allow_html=True)
                        if st.button("✕", key=f"remove_disliked_{s['id']}"):
                            remove_song(s["id"], "disliked")
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                    # faint divider between items
                    if i < len(st.session_state.disliked_songs) - 1:
                        st.markdown(
                            '<hr style="opacity:0.18; margin:12px 0; border:none; height:1px; background:rgba(255,255,255,0.06);">',
                            unsafe_allow_html=True,
                        )

            st.markdown("<br>", unsafe_allow_html=True)

            # Analyze Button - wrapped with custom class for CSS targeting
            st.markdown("<div class='analyze-btn-container'>", unsafe_allow_html=True)
            if st.button(
                "Analyze & Continue ➡️",
                key="btn_analyze_continue",
                use_container_width=True,
            ):
                if not st.session_state.liked_songs:
                    st.error("Please add at least one liked song.")
                else:
                    st.session_state.profile_step = "quiz"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
