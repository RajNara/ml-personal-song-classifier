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
        Uses the Deezer Search API as the audio source.
        """
        self.base_url = "https://api.deezer.com/search"
        self.temp_directory = temp_directory

        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory)

    def summarize_data(self, x, prefix):
        """
        Compute mean, standard deviation, max and min for a data entry array
        """
        return {
            f"{prefix}_mean": float(np.mean(x)),
            f"{prefix}_std": float(np.std(x)),
            f"{prefix}_min": float(np.min(x)),
            f"{prefix}_max": float(np.max(x)),
        }

    def search_tracks(self, query, limit=3):
        """
        Searches Deezer API for query
        """
        params = {"q": query, "limit": 10}

        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            raw_results = data.get("data", [])
            clean_results = []

            for item in raw_results:
                clean_results.append(
                    {
                        "trackId": item.get("id"),
                        "trackName": item.get("title"),
                        "artistName": item.get("artist", {}).get("name"),
                        "artworkUrl100": item.get("album", {}).get("cover_medium"),
                        "previewUrl": item.get("preview"),
                    }
                )

            query_tokens = set(query.lower().split())

            def get_score(song):
                title = song["trackName"].lower()
                title_tokens = set(title.split())
                matches = query_tokens.intersection(title_tokens)
                return len(matches)

            clean_results.sort(key=get_score, reverse=True)
            return clean_results[:limit]

        except Exception as e:
            print(f"Error during Deezer search: {e}")
            return []

    def get_track(self, track_id):
        """
        Fetch a single track by Deezer track ID.

        Returns a dict with keys similar to search_tracks items, or None on failure.
        """
        try:
            url = f"https://api.deezer.com/track/{track_id}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if not data or data.get("error"):
                return None

            return {
                "trackId": data.get("id"),
                "trackName": data.get("title"),
                "artistName": (data.get("artist") or {}).get("name"),
                "artworkUrl100": (data.get("album") or {}).get("cover_medium"),
                "previewUrl": data.get("preview"),
            }
        except Exception as e:
            print(f"Error fetching Deezer track {track_id}: {e}")
            return None

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

            features = {}

            # -- rhythm --
            # find when notes start (onsets)
            # this creates a graph of energy spikes over the sample
            onset = librosa.onset.onset_strength(y=raw_waveform, sr=sample_rate)

            # finds potential tempos of the song
            tempo = librosa.beat.tempo(onset_envelope=onset, sr=sample_rate)[0]
            features["tempo"] = float(tempo)

            beat_frames = librosa.beat.beat_track(onset_envelope=onset, sr=sample_rate)[
                1
            ]

            if len(beat_frames) > 1:
                beat_times = librosa.frames_to_time(beat_frames, sr=sample_rate)
                beat_intervals = np.diff(beat_times)
                features.update(self.summarize_data(beat_intervals, "beat_interval"))
            else:
                features.update(
                    {
                        "beat_interval_mean": 0.0,
                        "beat_interval_std": 0.0,
                        "beat_interval_min": 0.0,
                        "beat_interval_max": 0.0,
                    }
                )

            # -- MFCCs and deltas --
            # MFCCs (Mel-Frequency Cepstral Coefficients) describes the shape of the sound spectrum
            mfcc = librosa.feature.mfcc(y=raw_waveform, sr=sample_rate, n_mfcc=13)
            mfcc_delta = librosa.feature.delta(mfcc)
            mfcc_delta_2 = librosa.feature.delta(mfcc, order=2)

            for i in range(mfcc.shape[0]):
                features.update(self.summarize_data(mfcc[i], f"mfcc_{i+1}"))
                features.update(self.summarize_data(mfcc_delta[i], f"mfcc_delta_{i+1}"))
                features.update(
                    self.summarize_data(mfcc_delta_2[i], f"mfcc_delta_2_{i+1}")
                )

            # -- spectral features --
            spectral_centroid = librosa.feature.spectral_centroid(
                y=raw_waveform, sr=sample_rate
            )[0]
            spectral_bandwidth = librosa.feature.spectral_bandwidth(
                y=raw_waveform, sr=sample_rate
            )[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(
                y=raw_waveform, sr=sample_rate
            )
            spectral_contrast = librosa.feature.spectral_contrast(
                y=raw_waveform, sr=sample_rate
            )

            features.update(self.summarize_data(spectral_centroid, "spectral_centriod"))
            features.update(
                self.summarize_data(spectral_bandwidth, "spectral_bandwidth")
            )
            features.update(self.summarize_data(spectral_rolloff, "spectral_rolloff"))

            for i in range(spectral_contrast.shape[0]):
                features.update(
                    self.summarize_data(
                        spectral_contrast[i], f"spectral_contrast_{i+1}"
                    )
                )

            # -- harmonics and pitch --
            chroma = librosa.feature.chroma_stft(y=raw_waveform, sr=sample_rate)
            for i in range(chroma.shape[0]):
                features.update(self.summarize_data(chroma[i], f"chroma_{i+1}"))

            # -- energy and dynamics --
            root_mean_square_value = librosa.feature.rms(y=raw_waveform)[0]
            zero_crossing_rate = librosa.feature.zero_crossing_rate(y=raw_waveform)[0]

            features.update(self.summarize_data(root_mean_square_value, "rms"))
            features.update(self.summarize_data(zero_crossing_rate, "zcr"))

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
