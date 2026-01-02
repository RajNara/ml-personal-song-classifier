import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib


def train_model_in_memory(self, df):
    """
    Trains a model in-memory
    Args:
        df (pd.DataFrame): The training data
    Returns:
        model, scaler: The trained objects
    """
    if df is None or len(df) < 2:
        print("Not enough data to train")
        return None, None

    try:
        # remove metadata info
        # TODO: maybe use artist to inform model later?
        metadata_cols = [
            "track_name",
            "artist",
            "track_id",
            "preview_url",
            "filename",
            "label",
        ]
        existing_cols = [col for col in metadata_cols if col in df.columns]

        # features
        X = df.drop(columns=existing_cols)
        # target var
        y = df["label"]

        # scale data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # hyperparameters from optimization.py
        model = RandomForestClassifier(
            n_estimators=250, max_depth=6, min_samples_split=10, random_state=42
        )
        model.fit(X_scaled, y)

        return model, scaler
    except Exception as e:
        print(f"Error in training model : {e}")
        return None, None
