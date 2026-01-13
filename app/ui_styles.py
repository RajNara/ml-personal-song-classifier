import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #050505; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        .block-container {
            background-color: transparent !important;
            padding: 0 !important;
            max-width: 100% !important;
            z-index: 10;
            position: relative;
        }
        
        header, footer {visibility: hidden;}
        
        /* Keep button layout but DO NOT override background or color here
           to avoid unintentionally recoloring Streamlit primary/secondary buttons. */
        div.stButton > button {
            padding: 12px 30px; font-size: 18px; border-radius: 50px;
            font-weight: 700; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.15s ease;
            border: 0 !important;
        }
        div.stButton > button:not([kind="secondary"]) {
            padding: 12px 30px; font-size: 18px; border-radius: 50px;
            font-weight: 700; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.15s ease;
            border: 0 !important;
        }
        div.stButton > button[kind="secondary"] {
            padding: 12px 30px; font-size: 18px; border-radius: 50px;
            font-weight: 700; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.15s ease;
            border: 0 !important;
        }
        div.stButton > button:hover { transform: scale(1.02); }
        
        .stTextArea textarea, .stTextInput input {
            background-color: #111; color: #ddd; 
            border: 1px solid #333; border-radius: 12px;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #4CD2F0 !important;
            box-shadow: 0 0 10px rgba(76, 210, 240, 0.3) !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


def apply_landing_page_styles():
    st.markdown(
        """
        <style>
        html { scroll-behavior: smooth; scroll-snap-type: y mandatory; }
        
        .scroll-section {
            height: 100vh; width: 100vw;
            scroll-snap-align: start;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            position: relative; background: transparent; z-index: 20; border-bottom: none;
            overflow: visible;
        }
        
        .mlody-title {
            font-size: 160px; font-weight: 800; letter-spacing: -8px; margin: 0; 
            line-height: 1.3; padding-bottom: 30px; 
            padding-right: 0.2em; margin-right: -0.2em;
            
            transform-origin: center center;
            animation: grow-and-fade both;
            animation-timeline: scroll(nearest);
            animation-range: 0vh 90vh;
        }

        .highlight {
            background: linear-gradient(135deg, #7928CA 0%, #4CD2F0 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 25px rgba(121, 40, 202, 0.4));
        }
        .standard-text {
            background: linear-gradient(180deg, #A8A8A8 20%, #666666 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 1.0));
            padding-right: 0.15em; margin-right: -0.15em;
        }
        .mlody-subtitle { 
            font-size: 36px; font-weight: 500; letter-spacing: 1px; color: #C0C0C0;
            margin-top: -10px; text-shadow: 0 4px 12px rgba(0, 0, 0, 0.9);
        }

        @keyframes grow-and-fade {
            0% { transform: scale(1); opacity: 1; filter: blur(0px); }
            100% { transform: scale(4); opacity: 0; filter: blur(20px); }
        }
        
        .scroll-entrance-wrapper {
            animation: fade-up 1s ease-out both;
            animation-timeline: view();
            animation-range: entry 10% cover 30%;
            display: flex; justify-content: center; width: 100%;
        }

        .glass-card {
            background: rgba(20, 20, 20, 0.6) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 40px !important;
            box-shadow: 0 20px 50px rgba(0,0,0, 0.5) !important;
            transition: transform 0.3s ease !important;
            margin: 0 auto;
        }

        .glass-card:hover {
            transform: scale(1.02) !important;
            border-color: rgba(255,255,255,0.2) !important;
        }

        .problem-title {
            font-weight: 800; color: #E0E0E0; margin-bottom: 20px;
            line-height: 1.2;
        }

        .problem-desc {
            color: #9CA3AF; font-weight: 400; 
            line-height: 1.5; margin-top: 10px;
        }
        
        .highlight-error {
            background: linear-gradient(135deg, #FF5F6D 0%, #FFC371 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            padding-right: 0.1em;
        }
        
        @keyframes fade-up {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
                
        .social-icon { fill: #aaa; transition: fill 0.2s ease; }
        .social-icon:hover { fill: #4CD2F0; }

        .feature-text { 
            font-size: 60px; font-weight: 600; text-align: center; 
            color: #eee; text-shadow: 0 4px 8px rgba(0,0,0,1); 
        }
        .accent { color: #4CD2F0; text-shadow: 0 0 15px rgba(76, 210, 240, 0.4); }
        .floating-element { animation: float 6s ease-in-out infinite; padding: 20px; }
        @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-20px); } 100% { transform: translateY(0px); } }
        /* Start Listening button on home page - higher specificity to override global transparent background */
        .start-listening-btn-wrapper div.stButton > button {
            background: linear-gradient(90deg, #7928CA, #4CD2F0) !important;
            color: white !important;
            border: none !important;
            padding: 12px 30px !important;
            font-size: 18px !important;
            border-radius: 50px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(76, 210, 240, 0.4) !important;
        }
        .start-listening-btn-wrapper div.stButton > button:hover {
            transform: scale(1.05) !important;
            filter: brightness(1.05) !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


def apply_build_profile_styles():
    """
    PAGE 1 ONLY: Background + Intro + Buttons + PULSE CIRCLES.
    """
    st.markdown(
        """
        <style>
        /* 1. DARK GRADIENT BACKGROUND */
        .stApp {
            background: linear-gradient(-45deg, #050505, #120a1f, #08111f, #000000) !important;
            background-size: 400% 400% !important;
            animation: gradientBG 15s ease infinite !important;
            background-attachment: fixed !important;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* 2. THE PULSE CIRCLES (Intro Only) */
        .pulse-container {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; overflow: hidden; z-index: 9998;
            display: flex; justify-content: center; align-items: center;
        }
        .pulse-circle {
            position: absolute; border: 1px solid rgba(76, 210, 240, 0.15); border-radius: 50%; box-shadow: 0 0 40px rgba(121, 40, 202, 0.1); animation: pulseRipple 10s linear infinite; opacity: 0;
        }
        .pulse-1 { animation-delay: 0s; }
        .pulse-2 { animation-delay: 3.3s; }
        .pulse-3 { animation-delay: 6.6s; }
        @keyframes pulseRipple {
            0% { width: 0; height: 0; opacity: 0.8; border-width: 4px; }
            100% { width: 150vw; height: 150vw; opacity: 0; border-width: 0px; }
        }

        /* SLEEK DIVIDER */
        hr.sleek-divider {
            border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(255, 255, 255, 0.2), rgba(0, 0, 0, 0)); margin: 20px 0;
        }

        /* INTRO TEXT CONTAINER */
        .intro-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; display: flex; justify-content: center; align-items: center; background-color: transparent !important; backdrop-filter: blur(8px); z-index: 9999; }
        .intro-text { font-size: 60px; font-weight: 700; background: linear-gradient(90deg, #7928CA, #4CD2F0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; opacity: 0; animation: fadeInOut 3s ease-in-out forwards; }
        @keyframes fadeInOut { 0% { opacity: 0; transform: translateY(20px); } 15% { opacity: 1; transform: translateY(0); } 85% { opacity: 1; transform: translateY(0); } 100% { opacity: 0; transform: translateY(-20px); } }
        @keyframes fadeInPage { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

        /* --- BUTTON OVERRIDES --- */
        
        /* 1. GENERAL BUTTON RESET */
        div.stButton > button {
            white-space: nowrap !important;
            padding: 0.5rem 1rem !important;
            font-size: 20px !important;
            line-height: 1 !important;
            min-height: 50px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* 2. LIKE BUTTON (Green) - override Streamlit's inline styles */
        div.stButton > button[kind="primary"],
        div[data-testid="stBaseButton-primary"] {
            background-color: #15803d !important;
            background: #15803d !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #f0fdf4 !important;
            font-weight: 800 !important;
            border-radius: 50px !important;
            box-shadow: 0 4px 15px rgba(21, 128, 61, 0.6) !important;
        }
        div.stButton > button[kind="primary"]:hover,
        div[data-testid="stBaseButton-primary"]:hover {
            transform: scale(1.05) !important; box-shadow: 0 0 20px rgba(21, 128, 61, 0.8) !important; filter: brightness(1.2) !important;
        }

        /* 3. DISLIKE BUTTON (Red) */
        div.stButton > button[kind="secondary"],
        div.stButton > button[data-testid="stBaseButton-secondary"] {
            background: linear-gradient(135deg, #be123c 0%, #7e22ce 100%) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #fff1f2 !important;
            font-weight: 800 !important;
            border-radius: 50px !important;
            box-shadow: 0 4px 15px rgba(126, 34, 206, 0.4) !important;
        }
        div.stButton > button[kind="secondary"]:hover,
        div.stButton > button[data-testid="stBaseButton-secondary"]:hover {
            transform: scale(1.05) !important; box-shadow: 0 0 20px rgba(168, 85, 247, 0.6) !important; filter: brightness(1.2) !important;
        }

        /* 4. REMOVE BUTTON ("X") - Solid red styling, very small */
        button[aria-label="✖"],
        .stApp button[aria-label="✖"],
        [role="button"][aria-label="✖"] {
            width: 8px !important;
            height: 8px !important;
            min-width: 8px !important;
            min-height: 8px !important;
            max-width: 8px !important;
            max-height: 8px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 6px !important;
            line-height: 8px !important;
            border-radius: 50% !important;
            background: #991B1B !important;
            border: 0 !important;
            box-shadow: none !important;
            color: white !important;
        }
        button[aria-label="✖"]:hover,
        .stApp button[aria-label="✖"]:hover,
        [role="button"][aria-label="✖"]:hover {
            background: #B91C1C !important;
            transform: scale(1.2) !important;
            cursor: pointer !important;
        }

        /* 5. ANALYZE BUTTON - Handled by inline styles in Python */

        </style>
    """,
        unsafe_allow_html=True,
    )


def add_home_music_line():
    st.markdown(
        """
        <style>
        .musical-line-container {
            position: absolute; top: 0; left: 0; width: 100vw; height: 350vh;
            z-index: 0; pointer-events: none; overflow: hidden;
        }
        .neon-path {
            fill: none;
            stroke: url(#multiColorGradient);
            stroke-width: 6; stroke-linecap: round; stroke-dasharray: 20 40;
            animation: flowData 4s linear infinite;
            filter: drop-shadow(0 0 8px rgba(76, 210, 240, 0.4));
            opacity: 0.8;
        }
        @keyframes flowData { to { stroke-dashoffset: -60; } }
        </style>
        <div class="musical-line-container">
            <svg width="100%" height="100%" viewBox="0 0 100 4000" preserveAspectRatio="none">
                <defs>
                    <linearGradient id="multiColorGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" style="stop-color:#7928CA;stop-opacity:0" />
                        <stop offset="10%" style="stop-color:#7928CA;stop-opacity:1" />
                        <stop offset="35%" style="stop-color:#4CD2F0;stop-opacity:1" />
                        <stop offset="90%" style="stop-color:#FF0080;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#FF0080;stop-opacity:0" />
                    </linearGradient>
                </defs>
                <path d="M -10 100 C 50 100, 50 500, 50 1000 S 90 1500, 50 2000 S 10 2500, 50 3000 S 50 3500, 50 3800" class="neon-path" />
            </svg>
        </div>
    """,
        unsafe_allow_html=True,
    )
