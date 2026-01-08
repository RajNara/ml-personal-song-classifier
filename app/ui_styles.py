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
                        <stop offset="65%" style="stop-color:#007CF0;stop-opacity:1" />
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


def apply_build_profile_styles():
    """
    PAGE 1 ONLY: Intro animation, Album art hover, Quiz cards, and DNA Capsules.
    """
    st.markdown(
        """
        <style>
        .album-wrapper {
            position: relative; width: 80px; height: 80px;
            border-radius: 12px; overflow: hidden; cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5); transition: all 0.3s ease;
        }
        .album-wrapper:hover { transform: scale(1.05); box-shadow: 0 0 15px rgba(76, 210, 240, 0.6); }
        .album-img { width: 100%; height: 100%; object-fit: cover; display: block; }
        
        .play-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.6); display: flex; align-items: center;
            justify-content: center; opacity: 0; transition: opacity 0.2s ease;
        }
        .album-wrapper:hover .play-overlay { opacity: 1; }
        .play-icon { font-size: 28px; color: #fff; filter: drop-shadow(0 0 5px #4CD2F0); }

        .dna-capsule {
            display: flex; align-items: center;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 8px;
            margin-bottom: 10px;
            transition: all 0.2s ease;
        }
        .dna-capsule:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: #4CD2F0;
        }
        .capsule-img {
            width: 40px; height: 40px; border-radius: 6px; object-fit: cover; margin-right: 12px;
        }
        .capsule-info { flex-grow: 1; overflow: hidden; }
        .capsule-title { font-size: 14px; font-weight: 600; color: #eee; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .capsule-artist { font-size: 12px; color: #aaa; }
        
        /* Headers for the panels */
        .panel-header-pos { color: #4CD2F0; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; border-bottom: 1px solid rgba(76, 210, 240, 0.3); padding-bottom: 5px; }
        .panel-header-neg { color: #FF5F6D; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; border-bottom: 1px solid rgba(255, 95, 109, 0.3); padding-bottom: 5px; }

        /* --- 3. INTRO ANIMATION (Keep existing) --- */
        .intro-container { 
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            display: flex; justify-content: center; align-items: center;
            background-color: #050505; z-index: 9999;
        }
        .intro-text {
            font-size: 60px; font-weight: 700;
            background: linear-gradient(90deg, #7928CA, #4CD2F0); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            opacity: 0; animation: fadeInOut 2.5s ease-in-out forwards;
        }
        @keyframes fadeInOut { 
            0%   { opacity: 0; transform: translateY(20px); } 
            20%  { opacity: 1; transform: translateY(0); }
            80%  { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-20px); } 
        }
        @keyframes fadeInPage { 
            from { opacity: 0; transform: translateY(20px); } 
            to { opacity: 1; transform: translateY(0); } 
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
