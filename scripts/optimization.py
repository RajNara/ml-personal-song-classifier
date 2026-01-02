import pandas as pd
import numpy as np
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, "..")
sys.path.append(root_dir)

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

DATA_PATH = os.path.join(root_dir, "data", "raw", "training_data.csv")


def load_data():
    if not os.path.exists(DATA_PATH):
        print("data file not found")
        return None, None

    df = pd.read_csv(DATA_PATH)

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
    return X, y


def optimize():
    X, y = load_data()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    print("Tuning Random Forest...")
    random_forest_parameters = {
        "n_estimators": [100, 200, 250, 300],
        "max_depth": [None, 3, 6, 10],
        "min_samples_split": [5, 10, 15, 20],
    }

    random_forest_grid = GridSearchCV(
        RandomForestClassifier(random_state=42),
        random_forest_parameters,
        cv=5,
        scoring="accuracy",
        n_jobs=-1,
    )
    random_forest_grid.fit(X_train, y_train)

    print(f"Best Random Forest Accuracy: {random_forest_grid.best_score_:.2%}")
    print(f"Best Random Forest Parameters: {random_forest_grid.best_params_}")

    print("Tuning Gradient Boosting...")
    gradient_boosting_parameters = {
        "n_estimators": [25, 50, 100, 200],
        "learning_rate": [0.01, 0.1, 0.2, 0.5],
        "max_depth": [None, 3, 6, 10],
    }

    gradient_boosting_grid = GridSearchCV(
        GradientBoostingClassifier(random_state=42),
        gradient_boosting_parameters,
        cv=5,
        scoring="accuracy",
        n_jobs=-1,
    )
    gradient_boosting_grid.fit(X_train, y_train)

    print(f"Best Gradient Boosting Accuracy: {gradient_boosting_grid.best_score_:.2%}")
    print(f"Best Gradient Boosting Parameters: {gradient_boosting_grid.best_params_}")

    print("done evaluating")

    best_rf_model = random_forest_grid.best_estimator_
    random_forest_test_acc = best_rf_model.score(X_test, y_test)

    best_gb_model = gradient_boosting_grid.best_estimator_
    gradient_boosting_test_acc = best_gb_model.score(X_test, y_test)

    print(f"random forest test acc : {random_forest_test_acc:.2%}")
    print(f"gradient boosting test acc : {gradient_boosting_test_acc:.2%}")

    if random_forest_test_acc > gradient_boosting_test_acc:
        print("random forest wins")
    else:
        print("gradient boosting wins")


if __name__ == "__main__":
    optimize()
