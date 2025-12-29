import os
import requests
import warnings
import librosa
import numpy as np

warnings.filterwarnings("ignore")


class AudioClient:
    def __init__(self, temp_directory="../data/temp"):
        """
        Initializes the AudioClient with a temporary directory for storing
        audio files
        Uses the ITunes Search API as the audio source.
        """
        self.base_url = "https://itunes.apple.com/search"
        self.temp_directory = temp_directory

        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory)

    def search_tracks(self, query, limit=5):
        """
        Searches for audio tracks using the ITunes Search API.

        Args:
            query (str): The search query.
            limit (int): The maximum number of results to return.
        """
        params = {"term": query, "media": "music", "entity": "song", "limit": limit}

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            results = response.json().get("results", [])
            return results
        except Exception as e:
            print(f"Error during search: {e}")
            return []

    def download_preview(self, preview_url, track_id):
        """
        Downloads the audio preview for a given track to /data/temp.

        Args:
        track_id (int): The ID of the track.
        preview_url (str): The URL of the audio preview.
        """
        if not preview_url:
            print("No preview URL provided.")
            return None

        filename = os.path.join(self.temp_directory, f"{track_id}.m4a")

        # if track alr exists, return filename
        if os.path.exists(filename):
            return filename

        try:
            response = requests.get(preview_url)
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        except Exception as e:
            print(f"Error downloading preview: {e}")
            return None

    def extract_features(self, file_path, duration=30):
        """
        Extracts Mel-Frequency Cepstral Coefficients (MFCCs) and tempo
        from the audio file
        """
        try:
            # librosa.load decodes the audio
            # then resamples it to 22050 Hz to analyze texture
            # then mixes to mono
            raw_waveform, sample_rate = librosa.load(file_path, duration=duration)

            # find when notes start (onsets)
            # this creates a graph of energy spikes over the sample
            onset = librosa.onset.onset_strength(y=raw_waveform, sr=sample_rate)

            # finds potential tempos of the song
            tempo = librosa.beat.tempo(onset_envelope=onset, sr=sample_rate)[0]

            # MFCCs (Mel-Frequency Cepstral Coefficients) describes the shape of the sound spectrum
            mfcc = librosa.feature.mfcc(y=raw_waveform, sr=sample_rate, n_mfcc=13)

            # flatten 2d mfcc grid to average across time
            mfcc_flatten_mean = np.mean(mfcc, axis=1)

            # create dict
            features = {
                "tempo": float(tempo),
                # dictionary comprehension to unpack the grid
                **{f"mfcc_{i+1}": float(m) for i, m in enumerate(mfcc_flatten_mean)},
            }

            return features
        except Exception as e:
            print(f"Error extracting features from {file_path}: {e}")
            return None
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)


if __name__ == "__main__":
    client = AudioClient()

    # Example usage
    tracks = client.search_tracks("Imagine Dragons", limit=3)
    for track in tracks:
        print(f"Downloading preview for: {track['trackName']} by {track['artistName']}")
        file_path = client.download_preview(track["previewUrl"], track["trackId"])
        if file_path:
            features = client.extract_features(file_path)
            print(f"Extracted features: {features}")
