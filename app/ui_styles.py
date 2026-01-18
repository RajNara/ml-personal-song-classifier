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
        
        div.stButton > button {
            background: linear-gradient(90deg, #7928CA, #4CD2F0); 
            color: black; border: none;
            padding: 12px 30px; font-size: 18px; border-radius: 50px;
            font-weight: 700; 
            box-shadow: 0 4px 15px rgba(76, 210, 240, 0.4);
            transition: all 0.3s ease;
        }
        div.stButton > button:hover { transform: scale(1.05); filter: brightness(1.2); }
        
        .stTextArea textarea, .stTextInput input {
            background-color: #111; color: #ddd; 
            border: 1px solid #333; border-radius: 12px;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #4CD2F0 !important;
            box-shadow: 0 0 10px rgba(76, 210, 240, 0.3) !important;
        }

        .stToast {
            background: rgba(0, 0, 0, 0.9) !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
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
            animation: fade-up 1s ease-out forwards;
            animation-timeline: view();
            animation-range: entry 10% cover 30%;
            display: flex; justify-content: center; width: 100%;
            opacity: 1;
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
        </style>
    """,
        unsafe_allow_html=True,
    )


def apply_build_profile_styles():
    """
    Build Profile page styles with multi-color button support.
    Buttons are targeted by their key attribute using CSS substring selectors.
    """
    st.markdown(
        """
        <style>
        /* ===== PAGE BACKGROUND ===== */
        .stApp {
            background: linear-gradient(-45deg, #050505, #120a1f, #08111f, #000000) !important;
            background-size: 400% 400% !important;
            animation: gradientBG 15s ease infinite !important;
            background-attachment: fixed !important;
        }

        .block-container {
            max-width: 1200px !important;
            padding: 0 3rem 2rem 3rem !important;
            margin: 0 auto !important;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .pulse-container {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; overflow: hidden; z-index: 9998;
            display: flex; justify-content: center; align-items: center;
        }
        .pulse-circle {
            position: absolute; border: 1px solid rgba(76, 210, 240, 0.15); 
            border-radius: 50%; box-shadow: 0 0 40px rgba(121, 40, 202, 0.1); 
            animation: pulseRipple 10s linear infinite; opacity: 0;
        }
        .pulse-1 { animation-delay: 0s; }
        .pulse-2 { animation-delay: 3.3s; }
        .pulse-3 { animation-delay: 6.6s; }
        @keyframes pulseRipple {
            0% { width: 0; height: 0; opacity: 0.8; border-width: 4px; }
            100% { width: 150vw; height: 150vw; opacity: 0; border-width: 0px; }
        }

        .intro-container { 
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            display: flex; justify-content: center; align-items: center; 
            background-color: transparent !important; backdrop-filter: blur(8px); z-index: 9999; 
        }
        .intro-text { 
            font-size: 60px; font-weight: 700; 
            background: linear-gradient(90deg, #7928CA, #4CD2F0); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
            opacity: 0; animation: fadeInOut 3s ease-in-out forwards; 
        }
        @keyframes fadeInOut { 
            0% { opacity: 0; transform: translateY(20px); } 
            15% { opacity: 1; transform: translateY(0); } 
            85% { opacity: 1; transform: translateY(0); } 
            100% { opacity: 0; transform: translateY(-20px); } 
        }
        
        @keyframes fadeInContent {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .block-container {
            animation: fadeInContent 0.8s ease-out !important;
        }

        hr.sleek-divider {
            border: 0; height: 1px; 
            background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(255, 255, 255, 0.2), rgba(0, 0, 0, 0)); 
            margin: 20px 0;
        }

        div.stButton > button {
            white-space: nowrap !important;
            padding: 0.5rem 1rem !important;
            font-size: 18px !important;
            line-height: 1 !important;
            min-height: 50px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border-radius: 50px !important;
            font-weight: 700 !important;
            transition: all 0.3s ease !important;
        }
        
        /* 1. GREEN BUTTONS - primary type buttons (like) */
        div.stButton > button[kind="primary"],
        div.stButton > button[data-testid="stBaseButton-primary"] {
            background: linear-gradient(135deg, #15803d 0%, #0f766e 100%) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #f0fdf4 !important;
            box-shadow: 0 4px 15px rgba(15, 118, 110, 0.4) !important;
        }
        div.stButton > button[kind="primary"]:hover,
        div.stButton > button[data-testid="stBaseButton-primary"]:hover {
            transform: scale(1.05) !important; 
            box-shadow: 0 0 20px rgba(20, 184, 166, 0.6) !important; 
            filter: brightness(1.2) !important;
        }

        /* 2. RED/PURPLE BUTTONS - secondary type buttons (dislike) */
        div.stButton > button[kind="secondary"],
        div.stButton > button[data-testid="stBaseButton-secondary"] {
            background: linear-gradient(135deg, #be123c 0%, #7e22ce 100%) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #fff1f2 !important;
            box-shadow: 0 4px 15px rgba(126, 34, 206, 0.4) !important;
        }
        div.stButton > button[kind="secondary"]:hover,
        div.stButton > button[data-testid="stBaseButton-secondary"]:hover {
            transform: scale(1.05) !important; 
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.6) !important; 
            filter: brightness(1.2) !important;
        }

        /* 3. ANALYZE BUTTON - Special styling using custom class */
        .analyze-btn-container div.stButton > button {
            background: linear-gradient(135deg, #FFFFFF 0%, #f472b6 100%) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            color: white !important;
            font-size: 18px !important;
            min-height: 55px !important;
            box-shadow: 0 4px 20px rgba(236, 72, 153, 0.5) !important;
        }
        .analyze-btn-container div.stButton > button:hover {
            transform: scale(1.03) !important;
            filter: brightness(1.15) !important;
            box-shadow: 0 0 25px rgba(244, 114, 182, 0.7) !important;
        }
        
        div[data-testid="stVerticalBlock"] div[data-testid="column"]:last-child div.stButton > button:not([kind="primary"]):not([kind="secondary"]):not([data-testid*="btn_analyze"]) {
            min-width: 36px !important;
            width: 36px !important;
            height: 36px !important;
            min-height: 36px !important;
            padding: 0 !important;
            font-size: 14px !important;
            border-radius: 8px !important;
            background: #7f1d1d !important;
            border: 1px solid #991b1b !important;
            color: white !important;
        }
        div[data-testid="stVerticalBlock"] div[data-testid="column"]:last-child div.stButton > button:not([kind="primary"]):not([kind="secondary"]):not([data-testid*="btn_analyze"]):hover {
            background: #dc2626 !important;
            transform: scale(1.05) !important;
        }
        
        .stCaption {
            text-align: center !important;
        }

        .stApp a, .stMarkdown a {
            pointer-events: none !important;
            display: none !important;
        }

        a[href^="#"], .anchor-link, .stMarkdown .anchor-link {
            display: none !important;
            pointer-events: none !important;
        }

        div[data-testid="stForm"] button[kind="secondaryFormSubmit"],
        div[data-testid="stForm"] button[type="submit"] {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
        }
        div[data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover,
        div[data-testid="stForm"] button[type="submit"]:hover {
            transform: scale(1.02) !important;
            filter: brightness(1.15) !important;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.6) !important;
        }

        /* ===== COMPLETION / PROFILE BUILT STYLES ===== */
        .completion-hero h1 {
            font-size: 56px; font-weight: 800; margin: 0;
            line-height: 1.05;
            background: linear-gradient(90deg, #7928CA, #4CD2F0);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-wrap: balance;
        }
        .completion-hero p { color: #cfcfcf; margin-top: 8px; font-size: 18px; }

        .completion-stats { display: flex; gap: 12px; margin-top: 18px; align-items: center; }
        .completion-stats .stat-chip {
            background: rgba(255,255,255,0.03); padding: 14px 18px; border-radius: 12px; min-width: 110px; text-align: center;
        }
        .completion-stats .stat-chip .value { font-size: 20px; font-weight: 800; color: #ffffff; }
        .completion-stats .stat-chip .label { font-size: 12px; color: #9aa0a6; margin-top: 6px; }

        .completion-badge { width: 160px; height: 160px; border-radius: 18px; background: linear-gradient(135deg,#050505, #0b1220); display:flex; align-items:center; justify-content:center; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
        .completion-badge .check { font-size: 48px; font-weight: 900; background: linear-gradient(90deg,#7928CA,#4CD2F0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

        @media (max-width: 900px) {
            .glass-card { flex-direction: column !important; padding: 24px !important; gap: 20px !important; }
            .completion-badge { width: 120px; height: 120px; }
            .completion-hero h1 { font-size: 36px; }
            .completion-stats { flex-wrap: wrap; justify-content: flex-start; }
        }

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
