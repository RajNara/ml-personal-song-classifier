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
