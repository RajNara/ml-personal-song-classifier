import streamlit as st
import time
import requests
from app.ui_styles import apply_build_profile_styles, apply_global_styles


def initialize_user_model(client):
    """
    Renders Phase 1: Search & Seed.
    """

    # Apply the dedicated styles for this page (from ui_styles.py)
    apply_build_profile_styles()
    apply_global_styles()

    # =========================================================
    # LOGIC & HELPERS
    # =========================================================
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
        if category == "liked":
            target = st.session_state.liked_songs
            opposite = st.session_state.disliked_songs
            opposite_name = "Dislikes"
        else:
            target = st.session_state.disliked_songs
            opposite = st.session_state.liked_songs
            opposite_name = "Likes"

        # Check if song exists in the opposite category
        if any(s["id"] == song["id"] for s in opposite):
            # Shows a warning toast in the top right
            st.toast(f"⚠️ '{song['name']}' is already in your {opposite_name} list.")
            return

        # Proceed with adding if it's not already in the target list
        if not any(s["id"] == song["id"] for s in target):
            target.append(song)
            st.toast(f"Added {song['name']} to {category}", icon="✅")

    # =========================================================
    # INTRO SEQUENCE
    # =========================================================
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

    # =========================================================
    # PAGE LAYOUT
    # =========================================================

    # Page Fade In
    if "has_faded_in" not in st.session_state:
        st.session_state.has_faded_in = False
    if not st.session_state.has_faded_in:
        st.markdown(
            """<style>.block-container { animation: fadeInPage 3s ease-in-out forwards; }</style>""",
            unsafe_allow_html=True,
        )
        st.session_state.has_faded_in = True

    # Main Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style='margin:0;'>Build your Profile 🧬</h1>
            <p style='color: #888; margin-top:5px;'>Search for songs to establish your baseline.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # COLUMNS WITH MARGINS
    # 0.2 fractions on ends act as margins to prevent hugging the sides
    _, col_search, col_dashboard, _ = st.columns([0.2, 1.5, 1, 0.2], gap="large")

    # ---------------------------------------------------------
    # LEFT COLUMN: SEARCH
    # ---------------------------------------------------------
    with col_search:
        # Search Input with fixed key to prevent duplicate render bug
        search_query = st.text_input(
            "Search",
            placeholder="Type a song name...",
            label_visibility="collapsed",
            key="search_query_unique_fixed",
            on_change=None,
        )

        # Only show results if search query exists and has content
        if search_query and len(search_query.strip()) > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            results = client.search_tracks(search_query, limit=3)

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
        with st.container(border=True):
            st.markdown(
                "<h4 style='text-align:center;'>Your Selections</h4>",
                unsafe_allow_html=True,
            )

            # 1. Liked Section
            st.markdown("##### 💚 Likes")
            if not st.session_state.liked_songs:
                st.markdown(
                    "<div style='color:#666; font-style:italic; font-size:14px;'>No songs added yet...</div>",
                    unsafe_allow_html=True,
                )
            else:
                for s in st.session_state.liked_songs:
                    r1, r2 = st.columns([5, 1], vertical_alignment="center")
                    r1.markdown(
                        f"<div style='font-size:14px; text-align:center;'>{s['name']} <span style='color:#888'>- {s['artist']}</span></div>",
                        unsafe_allow_html=True,
                    )
                    # The '✖' button - using use_container_width=False and help to style
                    if r2.button("✖", key=f"rem_l_{s['id']}", help="Remove song"):
                        remove_song(s["id"], "liked")

            st.markdown("<hr style='opacity:0.3'>", unsafe_allow_html=True)

            # 2. Disliked Section
            st.markdown("##### ❌ Dislikes")
            if not st.session_state.disliked_songs:
                st.markdown(
                    "<div style='color:#666; font-style:italic; font-size:14px;'>No songs added yet...</div>",
                    unsafe_allow_html=True,
                )
            else:
                for s in st.session_state.disliked_songs:
                    r1, r2 = st.columns([5, 1], vertical_alignment="center")
                    r1.markdown(
                        f"<div style='font-size:14px; text-align:center;'>{s['name']} <span style='color:#888'>- {s['artist']}</span></div>",
                        unsafe_allow_html=True,
                    )
                    if r2.button("✖", key=f"rem_d_{s['id']}", help="Remove song"):
                        remove_song(s["id"], "disliked")

            st.markdown("<br>", unsafe_allow_html=True)

            # 3. Next Step Action - Custom HTML button with inline styles
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(
                    "Analyze & Continue ➡️",
                    type="primary",
                    use_container_width=True,
                    key="analyze_btn_unique",
                    help="Analyze your music preferences",
                ):
                    if not st.session_state.liked_songs:
                        st.error("Please add at least three liked songs.")
                    else:
                        st.session_state.profile_step = "quiz"
                        st.rerun()

            # Apply gradient styling to the button we just created
            st.markdown(
                """
                <style>
                button[key="analyze_btn_unique"],
                button:has(+ button[key="analyze_btn_unique"]),
                div.stColumn:nth-child(2) button[data-testid="stBaseButton-primary"] {
                    background: #C97FBF !important;
                    background: radial-gradient(circle, rgba(201, 127, 191, 1) 0%, rgba(79, 130, 185, 1) 100%) !important;
                    color: white !important;
                    border: none !important;
                    font-weight: 700 !important;
                    box-shadow: 0 4px 20px rgba(201, 127, 191, 0.5) !important;
                }
                div.stColumn:nth-child(2) button[data-testid="stBaseButton-primary"]:hover {
                    box-shadow: 0 4px 20px rgba(201, 127, 191, 0.6) !important;
                    transform: scale(1.05) !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
