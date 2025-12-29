import os
import requests
import warnings

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
        if os.path.exists(self.temp_directory):
            return filename

        try:
            response = requests.get(preview_url)
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        except Exception as e:
            print(f"Error downloading preview: {e}")
            return None
