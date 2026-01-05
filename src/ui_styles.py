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
            background-color: #111; color: #ddd; border: 1px solid #333; border-radius: 12px;
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
            font-size: 160px;
            font-weight: 800;
            letter-spacing: -8px;
            margin: 0; 
            line-height: 1.3;     
            transform-origin: center center;
            animation-name: grow-and-fade;
            animation-fill-mode: both;
            animation-timeline: scroll(nearest);
            animation-range: 0vh 90vh;
        }

        /* purple to cyan*/
        .highlight {
            background: linear-gradient(135deg, #7928CA 0%, #4CD2F0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 25px rgba(121, 40, 202, 0.4));
        }
        
        /* grey */
        .standard-text {
            background: linear-gradient(180deg, #A8A8A8 20%, #666666 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 1.0));
            padding-right: 0.15em; 
            margin-right: -0.15em;
        }

        @keyframes grow-and-fade {
            0% { transform: scale(1); opacity: 1; filter: blur(0px); }
            100% { transform: scale(4); opacity: 0; filter: blur(20px); }
        }
        
        .mlody-subtitle { 
            font-size: 36px;       
            font-weight: 500;      
            letter-spacing: 1px;   
            color: #C0C0C0;
            margin-top: -10px; 
            text-shadow: 0 4px 12px rgba(0, 0, 0, 0.9);
            padding: 0 20px;
        }
        
        .feature-text { 
            font-size: 60px; font-weight: 600; text-align: center; max-width: 800px; line-height: 1.1; 
            color: #eee; text-shadow: 0 4px 8px rgba(0,0,0,1); 
        }
        
        .accent { color: #4CD2F0; text-shadow: 0 0 15px rgba(76, 210, 240, 0.4); }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
            100% { transform: translateY(0px); }
        }
        
        .floating-element { 
            animation: float 6s ease-in-out infinite;
            padding: 20px;
        }
                
        /* --- SEARCH & PROFILE STYLES --- */
        
        /* 1. The Search Input Field Styling */
        div[data-testid="stTextInput"] input {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #fff !important;
            border-radius: 12px !important;
            padding: 10px 15px !important;
            font-size: 18px !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #4CD2F0 !important;
            box-shadow: 0 0 10px rgba(76, 210, 240, 0.3) !important;
        }

        /* 2. Search Result Strip (The "Row") */
        .result-strip {
            display: flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 15px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        .result-strip:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(76, 210, 240, 0.3);
            transform: translateX(5px); /* Subtle nudge */
        }

        /* 3. Album Art Styling */
        .album-art-img {
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            transition: transform 0.2s;
        }
        .result-strip:hover .album-art-img {
            transform: scale(1.05);
        }

        /* 4. Text Typography */
        .track-name {
            font-size: 20px;
            font-weight: 700;
            color: #fff;
            margin: 0;
            line-height: 1.2;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .track-artist {
            font-size: 14px;
            font-weight: 400;
            color: #888;
            margin: 0;
        }
                
        /* --- INTRO SEQUENCE STYLES --- */
        .intro-container {
            height: 80vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        .intro-text {
            font-size: 60px;
            font-weight: 300;
            color: #E0E0E0;
            opacity: 0;
            animation: fadeInOut 3s ease-in-out forwards;
        }
        
        @keyframes fadeInOut {
            0% { opacity: 0; transform: scale(0.9); }
            20% { opacity: 1; transform: scale(1); }
            80% { opacity: 1; transform: scale(1); }
            100% { opacity: 0; transform: scale(1.1); }
        }

        /* 1. The Scroll Animation Wrapper */
        .scroll-entrance-wrapper {
            animation: fade-up 1s ease-out both;
            animation-timeline: view();
            animation-range: entry 10% cover 30%; 
            width: 100%;
            display: flex;
            justify-content: center;
        }

        /* 2. The Glass Card */
        .glass-card {
            background: rgba(20, 20, 20, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 30px;
            
            /* Slightly more horizontal breathing room */
            padding: 60px 60px; 
            text-align: center;
            
            width: fit-content;
            min-width: 70vw;          /* 🔑 prevents text compression */
            max-width: 90vw;
            
            box-shadow: 0 20px 50px rgba(0,0,0, 0.5);
            
            transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94), 
                        box-shadow 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .glass-card:hover {
            transform: scale(1.02);
            box-shadow: 0 40px 80px rgba(0,0,0, 0.8);
            border-color: rgba(255, 255, 255, 0.2);
        }

        /* --- TEXT FIXES --- */
        .problem-title {
            font-size: 130px;
            font-weight: 800;
            color: #E0E0E0;
            margin-bottom: 30px;

            /* 🔑 critical typography fixes */
            line-height: 1.15;
            letter-spacing: -0.5px;   /* was too tight for this size */

            /* Prevent awkward word compression */
            white-space: normal;
            word-break: keep-all;
        }

        /* Subtitle / paragraph */
        .problem-desc {
            font-size: 48px;          /* ⬆️ slightly larger */
            color: #9CA3AF;
            font-weight: 400;
            line-height: 1.45;
            max-width: 1100px;
            margin: 0 auto;
        }

        /* Highlighted word */
        .highlight-error {
            background: linear-gradient(135deg, #FF5F6D 0%, #FFC371 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            /* 🔑 spacing fix for gradient text */
            letter-spacing: 0.02em;
            padding-right: 0.15em;

            filter: drop-shadow(0 0 25px rgba(255, 95, 109, 0.4));
        }

        @keyframes fade-up {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
                
        .song-card {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 10px;
            text-align: center;
            transition: transform 0.2s;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .song-card:hover {
            transform: scale(1.05);
            background-color: rgba(255, 255, 255, 0.1);
            border-color: #4CD2F0;
        }
        
        /* The Quiz Card (Centered Glass) */
        .quiz-container {
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 100%; max-width: 600px;
            z-index: 100;
        }
        
        /* Animation for the Question Fading In */
        @keyframes fadeInScale {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .quiz-card {
            background: rgba(15, 15, 20, 0.85); /* Darker for focus */
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 40px;
            padding: 50px;
            text-align: center;
            box-shadow: 0 25px 50px rgba(0,0,0, 0.7);
            
            animation: fadeInScale 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) both;
        }
        
        /* Quiz Buttons */
        .btn-yes {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: #000; font-weight: 800; border: none; font-size: 24px;
            padding: 15px 40px; border-radius: 50px; width: 100%;
            transition: transform 0.2s;
            box-shadow: 0 0 20px rgba(67, 233, 123, 0.4);
        }
        .btn-no {
            background: linear-gradient(135deg, #ff5f6d 0%, #ffc371 100%);
            color: #fff; font-weight: 800; border: none; font-size: 24px;
            padding: 15px 40px; border-radius: 50px; width: 100%;
            transition: transform 0.2s;
            box-shadow: 0 0 20px rgba(255, 95, 109, 0.4);
        }
        .btn-yes:hover, .btn-no:hover { transform: scale(1.05); filter: brightness(1.1); }
    </style>
    """,
        unsafe_allow_html=True,
    )


def add_home_music_line():
    st.markdown(
        """
        <style>
        .musical-line-container {
            position: absolute; top: 0; left: 0; width: 100vw; height: 400vh;
            z-index: 0; pointer-events: none; overflow: hidden;
        }
        .neon-path {
            fill: none;
            stroke: url(#multiColorGradient);
            stroke-width: 6;
            stroke-linecap: round;
            stroke-dasharray: 20 40;
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
