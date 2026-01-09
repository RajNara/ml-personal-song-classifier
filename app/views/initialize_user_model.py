import streamlit as st
import time


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

    # --- INTRO SEQUENCE (PRESERVED) ---
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
    # UI HEADER
    # ==========================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <h1 style='text-align: center; margin-bottom: 10px;'>Build your Profile 🧬</h1>
        <p style='text-align: center; color: #888;'>Search for songs to establish your baseline.</p>
    """,
        unsafe_allow_html=True,
    )

    # SEARCH BAR (Centered)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        search_query = st.text_input(
            "Search", placeholder="Type a song name...", label_visibility="collapsed"
        )

    # ==========================
    # SEARCH RESULTS
    # ==========================
    if search_query:
        st.markdown("<br>", unsafe_allow_html=True)

        # CONSTRAIN WIDTH: Use columns so it doesn't stretch edge-to-edge
        # 1 part padding | 2 parts content | 1 part padding
        layout_c1, layout_c2, layout_c3 = st.columns([1, 2, 1])

        with layout_c2:
            results = client.search_tracks(search_query, limit=25)

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

                # ROW LAYOUT
                # Adjusted ratios for cleaner button fit: [1.5, 3.5, 1.5, 1.5]
                col_img, col_info, col_like, col_dislike = st.columns(
                    [1.5, 3.5, 1.5, 1.5]
                )

                with col_img:
                    # LARGER IMAGE (100px)
                    st.image(song["img"], width=100)

                with col_info:
                    st.markdown(f"**{song['name']}**")
                    st.caption(song["artist"])
                    # Native Audio Player
                    if song["preview"]:
                        st.audio(song["preview"], format="audio/mp4")

                with col_like:
                    st.markdown(
                        "<div style='height: 10px'></div>", unsafe_allow_html=True
                    )
                    # Green Gradient Button
                    if st.button(
                        "Like",
                        key=f"l_{song['id']}",
                        type="primary",
                        use_container_width=True,
                    ):
                        add_song(song, "liked")

                with col_dislike:
                    st.markdown(
                        "<div style='height: 10px'></div>", unsafe_allow_html=True
                    )
                    # Red Gradient Button (Secondary)
                    if st.button(
                        "Dislike",
                        key=f"d_{song['id']}",
                        type="secondary",
                        use_container_width=True,
                    ):
                        add_song(song, "disliked")

                # SLEEK DIVIDER
                st.markdown('<hr class="sleek-divider">', unsafe_allow_html=True)

    # ==========================
    # YOUR SELECTIONS
    # ==========================
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Your Selections")

    col_likes, col_dislikes = st.columns(2, gap="large")

    with col_likes:
        st.markdown("##### 💚 Liked Songs")
        if not st.session_state.liked_songs:
            st.caption("No songs added yet.")
        else:
            for s in st.session_state.liked_songs:
                with st.container(border=True):
                    cl1, cl2 = st.columns([5, 1])
                    cl1.text(f"{s['name']} - {s['artist']}")
                    if cl2.button("✖", key=f"rem_l_{s['id']}"):
                        remove_song(s["id"], "liked")

    with col_dislikes:
        st.markdown("##### ❌ Disliked Songs")
        if not st.session_state.disliked_songs:
            st.caption("No songs added yet.")
        else:
            for s in st.session_state.disliked_songs:
                with st.container(border=True):
                    cd1, cd2 = st.columns([5, 1])
                    cd1.text(f"{s['name']} - {s['artist']}")
                    if cd2.button("✖", key=f"rem_d_{s['id']}"):
                        remove_song(s["id"], "disliked")

    # NEXT STEP
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Analyze & Continue ➡️", type="primary", use_container_width=True):
        if not st.session_state.liked_songs:
            st.error("Please add at least one liked song.")
        else:
            st.session_state.profile_step = "quiz"
            st.rerun()
