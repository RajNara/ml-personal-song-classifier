import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib


class ModelTrainer:
    def __init__(self):
        self.models_dir = "../models"
        self.model_path = os.path.join(self.models_dir, "music_classifier.pkl")
        self.scaler_path = os.path.join(self.models_dir, "scaler.pkl")

        os.makedirs(self.models_dir, exist_ok=True)

    def load_and_clean_data(self, filepath):
        """
        Loads CSV and cleans the data
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file {filepath} does not exist.")

        df = pd.read_csv(filepath)
        print(f"Loaded len{df} songs ")

        drop_columns = ["track_name", "artist", "track_id", "preview_url", "filename"]
        existing_drop_columns = [col for col in drop_columns if col in df.columns]
        clean_df = df.drop(columns=existing_drop_columns)

        return clean_df

    def train_model(self, data_path):
        """
        Trains a RandomForestClassifier on the provided data
        """
        df = self.load_and_clean_data(data_path)

        # label is the target variable
        X = df.drop(columns=["label"])
        y = df["label"]

        # split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        print("Training Random Forest Model...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)

        # evaluate model
        y_pred = model.predict(X_test_scaled)
        accuracy_score_val = accuracy_score(y_test, y_pred)

        print("Training complete.")
        print(f"Accuracy: {accuracy_score_val:.4f}")

        print(classification_report(y_test, y_pred))

        # save model and scaler
        joblib.dump(model, self.model_path)
        joblib.dump(scaler, self.scaler_path)


if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train_model("../data/raw/training_data.csv")
