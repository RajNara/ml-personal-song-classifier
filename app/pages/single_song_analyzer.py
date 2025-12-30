import os
import sys
import numpy as np
import streamlit as st
import pandas as pd
import joblib

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, "..", "..")
sys.path.append(root_dir)

from src.audio_client import AudioClient

MODEL_PATH = os.path.join(root_dir, "models", "music_classifier.pkl")
SCALER_PATH = os.path.join(root_dir, "models", "scaler.pkl")


# loading assets
def load_assets():
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    except FileNotFoundError as e:
        print("Cannot load assets")
        return None, None


model, scaler = load_assets()

st.set_page_config(page_title="AI Music Curator", page_icon="🎶")
st.title("AI Music Curator 🎧")
st.write("This model was trained on hardcoded artists for a demo (likes vs. dislikes)")

if model is None or scaler is None:
    st.error("Cannot find model! Please run model_trainer.py first.")
    st.stop()

query = st.text_input("Search for a song!", "")

if query:
    client = AudioClient()
    with st.spinner(f"Searching iTunes for '{query}'..."):
        results = client.search_tracks(query, limit=5)

    if not results:
        st.warning(f"No songs found with '{query}. Please try again!")
    else:
        # displaying top 5 matches
        st.subheader("Results")

        for track in results:
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                st.image(track["artworkUrl100"])

            with col2:
                st.markdown(f"**{track['trackName']}**")
                st.caption(track["artistName"])
                st.audio(track["previewUrl"])

            with col3:
                button = f"Analyze_{track['trackId']}"

                if st.button("Do I like this song?", key=button):
                    with st.spinner("Listening and analyzing..."):
                        path = client.download_preview(
                            track["previewUrl"], track["trackId"]
                        )

                        if path:
                            features = client.extract_features(path)

                            if features:
                                features_df = pd.DataFrame([features])

                                X_scaled = scaler.transform(features_df)

                                prediction = model.predict(X_scaled)[0]
                                probability_of_likedness = model.predict_proba(
                                    X_scaled
                                )[0][1]

                                if prediction == 1:
                                    st.success(
                                        f"MATCH!! ({probability_of_likedness*100:.0f}%)"
                                    )
                                    st.write(
                                        "The model predicts you should like this song!"
                                    )
                                else:
                                    st.error(
                                        f"SKIP!! ({probability_of_likedness*100:.0f}%)"
                                    )
                                    st.write(
                                        "The model predicts you should skip this song."
                                    )

                                st.caption(f"Tempo: {features['tempo']:.0f} BPM")
                            else:
                                st.error("Could not analyze this audio")
