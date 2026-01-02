import streamlit as st

# make style look as "Apple" as possible


def apply_global_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #000000;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        .block-container {
            background-color: transparent !important;
            padding: 0 !important;
            max-width: 100% !important;
            z-index: 10;
            position: relative;
        }
        
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        div.stButton > button {
            background: #2997ff;
            color: white; 
            border: none;
            padding: 12px 30px; 
            font-size: 18px; 
            border-radius: 50px;
            font-weight: 500; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        div.stButton > button:hover { transform: scale(1.05); background: #0071e3; }
        
        .stTextArea textarea, .stTextInput input {
            background-color: #1c1c1e; color: white; border: 1px solid #333; border-radius: 12px;
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
            height: 100vh;
            width: 100vw;
            scroll-snap-align: start;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            background: transparent;
            z-index: 20;
            border-bottom: none;
        }
        
        .mlody-title {
            font-size: 120px; font-weight: 700; letter-spacing: -4px;
            background: linear-gradient(180deg, #fff, #666);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin: 0; line-height: 1;
        }

        .mlody-subtitle { 
            font-size: 32px;
            color: #86868b;
            margin-top: 20px; 
        }

        .feature-text { font-size: 60px; font-weight: 600; text-align: center; max-width: 800px; line-height: 1.1; }
        .accent { color: #00C9FF; }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
            100% { transform: translateY(0px); }
        }
        .floating-element { animation: float 6s ease-in-out infinite; }
        </style>
    """,
        unsafe_allow_html=True,
    )


def add_home_music_line():
    st.markdown(
        """
        <style>
        .musical-line-container {
            position: absolute;
            top: 0; left: 0;
            width: 100vw; height: 400vh;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }
        .neon-path {
            fill: none;
            stroke: url(#neonGradient);
            stroke-width: 6;
            stroke-linecap: round;
            stroke-dasharray: 20 40;
            animation: flowData 2s linear infinite;
            filter: drop-shadow(0 0 8px rgba(0, 201, 255, 0.8));
            opacity: 0.8;
        }
        @keyframes flowData {
            to { stroke-dashoffset: -60; }
        }
        </style>

        <div class="musical-line-container">
            <svg width="100%" height="100%" viewBox="0 0 100 4000" preserveAspectRatio="none">
                <defs>
                    <linearGradient id="neonGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" style="stop-color:#00C9FF;stop-opacity:0" />
                        <stop offset="20%" style="stop-color:#00C9FF;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#92FE9D;stop-opacity:1" />
                        <stop offset="80%" style="stop-color:#00C9FF;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#00C9FF;stop-opacity:0" />
                    </linearGradient>
                </defs>
                <path d="M -10 100 C 50 100, 50 500, 50 1000 S 90 1500, 50 2000 S 10 2500, 50 3000 S 50 3500, 50 3800" class="neon-path" />
            </svg>
        </div>
    """,
        unsafe_allow_html=True,
    )
