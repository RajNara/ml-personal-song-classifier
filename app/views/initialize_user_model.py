import streamlit as st
import time
import sys
from pathlib import Path

# Add parent directory to path to import particles
sys.path.insert(0, str(Path(__file__).parent.parent))
from particles import render_particles


def initialize_user_model(client):
    """
    Renders Phase 1: Search & Seed.
    Uses a form-based search to prevent duplicate widget issues.
    """

    def remove_song(song_id, category="liked"):
        target_key = f"{category}_songs"
        st.session_state[target_key] = [
            s for s in st.session_state[target_key] if s["id"] != song_id
        ]

    def add_song(song, category="liked"):
        target_key = f"{category}_songs"
        target = st.session_state[target_key]
        if category == "disliked":
            if any(
                s["id"] == song["id"] for s in st.session_state.get("liked_songs", [])
            ):
                st.toast(
                    "This song is already in your liked songs. Remove it there before disliking."
                )
                return False
        elif category == "liked":
            if any(
                s["id"] == song["id"]
                for s in st.session_state.get("disliked_songs", [])
            ):
                st.toast(
                    "This song is already in your disliked songs. Remove it there before liking."
                )
                return False

        if not any(s["id"] == song["id"] for s in target):
            target.append(song)
            return True
        else:
            return False

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

    # If a transition to the quiz was requested, switch steps directly.
    if st.session_state.get("start_quiz_fade"):
        st.session_state.start_quiz_fade = False
        st.session_state.profile_step = "quiz"
        st.rerun()
        return  # Prevent any further rendering

    # Add particles background after intro
    if "particles_config" not in st.session_state:
        st.session_state.particles_config = None

    particles_html, st.session_state.particles_config = render_particles(
        st.session_state.particles_config
    )
    st.markdown(particles_html, unsafe_allow_html=True)

    # page header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style='margin:0;'>Build your MLody 🧬</h1>
            <p style='color: #888; margin-top:5px;'>Search for songs to establish your baseline.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col_search, col_dashboard = st.columns([1.5, 1], gap="large")

    with col_search:
        with st.form(key="search_form", clear_on_submit=False):
            search_query = st.text_input(
                "Search",
                placeholder="Type a song name...",
                label_visibility="collapsed",
            )
            search_submitted = st.form_submit_button(
                "Search 🔍", use_container_width=True
            )

        if search_submitted and search_query:
            st.session_state.current_search = search_query

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
                            if add_song(song, "liked"):
                                st.rerun()

                    with c_dislike:
                        if st.button(
                            "👎",
                            key=f"dislike_{song['id']}",
                            type="secondary",
                            use_container_width=True,
                        ):
                            if add_song(song, "disliked"):
                                st.rerun()

                    st.markdown('<hr class="sleek-divider">', unsafe_allow_html=True)

    with col_dashboard:
        with st.container(border=True):
            st.markdown(
                "<h4 style='text-align:center; margin-bottom: 20px;'>Your Selections</h4>",
                unsafe_allow_html=True,
            )

            st.markdown(
                "<div style='font-size:18px; font-weight:700; margin-top:6px;'>💚 Likes</div>",
                unsafe_allow_html=True,
            )
            if not st.session_state.liked_songs:
                st.markdown(
                    "<div style='color:#666; font-style:italic; font-size:14px;'>No songs added yet...</div>",
                    unsafe_allow_html=True,
                )
            else:
                for i, s in enumerate(st.session_state.liked_songs):
                    col_song, col_btn = st.columns([5, 1], vertical_alignment="center")
                    with col_song:
                        st.markdown(
                            f"<div style='text-align:center;'><strong>{s['name']}</strong></div>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"<div style='text-align:center; color:#888; font-size:13px;'>{s['artist']}</div>",
                            unsafe_allow_html=True,
                        )
                    with col_btn:
                        if st.button(
                            "❌", key=f"remove_liked_{s['id']}", use_container_width=True
                        ):
                            remove_song(s["id"], "liked")
                            st.toast(f"Removed {s['name']} from Likes", icon="🗑️")
                            st.rerun()
                    # faint divider between items
                    if i < len(st.session_state.liked_songs) - 1:
                        st.markdown(
                            '<hr class="sleek-divider">', unsafe_allow_html=True
                        )

            st.markdown(
                "<div style='border-top: 1px solid rgba(255,255,255,0.2); margin: 10px 0;'></div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                "<div style='font-size:18px; font-weight:700; margin-top:12px;'>❌ Dislikes</div>",
                unsafe_allow_html=True,
            )
            if not st.session_state.disliked_songs:
                st.markdown(
                    "<div style='color:#666; font-style:italic; font-size:14px;'>No songs added yet...</div>",
                    unsafe_allow_html=True,
                )
            else:
                for i, s in enumerate(st.session_state.disliked_songs):
                    col_song, col_btn = st.columns([5, 1], vertical_alignment="center")
                    with col_song:
                        st.markdown(
                            f"<div style='text-align:center;'><strong>{s['name']}</strong></div>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"<div style='text-align:center; color:#888; font-size:13px;'>{s['artist']}</div>",
                            unsafe_allow_html=True,
                        )
                    with col_btn:
                        if st.button(
                            "❌",
                            key=f"remove_disliked_{s['id']}",
                            use_container_width=True,
                        ):
                            remove_song(s["id"], "disliked")
                            st.toast(f"Removed {s['name']} from Dislikes", icon="🗑️")
                            st.rerun()
                    # faint divider between items
                    if i < len(st.session_state.disliked_songs) - 1:
                        st.markdown(
                            '<hr class="sleek-divider">', unsafe_allow_html=True
                        )

            st.markdown("</div>", unsafe_allow_html=True)
            if st.button(
                "Analyze & Continue ➡️",
                key="btn_analyze_continue",
                use_container_width=True,
            ):
                if not st.session_state.liked_songs:
                    st.error("Please add at least one liked song.")
                else:
                    # trigger a short fade transition before moving to the quiz
                    st.session_state.start_quiz_fade = True
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
