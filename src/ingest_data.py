import sys
import os
import pandas as pd
import time
import random

from audio_client import AudioClient

LIKED_ARTISTS = [
    "Playboi Carti",
    "Drake",
    "Kendrick Lamar",
    "J. Cole",
    "Travis Scott",
    "Lil Uzi Vert",
    "Post Malone",
    "21 Savage",
    "Lil Baby",
]

DISLIKED_ARTISTS = [
    "Nickelback",
    "Justin Bieber",
    "Rebecca Black",
    "Limp Bizkit",
    "Insane Clown Posse",
    "Soulja Boy",
    "Hanson",
    "Celine Dion",
    "Rebecca Black",
]

client = AudioClient()


def ingest_data():
    dataset = []

    print("--- starting data ingestion ---")

    liked_artists = process_artists(LIKED_ARTISTS, 1)
    disliked_artists = process_artists(DISLIKED_ARTISTS, 0)

    dataset.extend(liked_artists)
    dataset.extend(disliked_artists)

    if dataset:
        os.makedirs("../data/raw", exist_ok=True)
        output_path = "../data/raw/training_data.csv"

        df = pd.DataFrame(data=dataset)
        df.to_csv(output_path, index=False)

        print(f"Success! Saved {len(df)} songs to {output_path}")
    else:
        print("Dataset does not exist")


def process_artists(artist_list, label):
    count = 0
    dataset = []
    for artist in artist_list:
        print(f"\n Searching for {artist}")
        tracks = client.search_tracks(artist, limit=5)

        for track in tracks:
            print(f" -- processing: {track['trackName']}", end=" ", flush=True)

            path = client.download_preview(track["previewUrl"], track["trackId"])
            if not path:
                print("download failed")
                continue

            features = client.extract_features(path)
            if not features:
                print("feature extraction failed")
                continue

            features["label"] = label
            features["track_name"] = track["trackName"]
            features["artist"] = track["artistName"]
            features["track_id"] = track["trackId"]

            dataset.append(features)
            time.sleep(1.0)

    return dataset


if __name__ == "__main__":
    ingest_data()
