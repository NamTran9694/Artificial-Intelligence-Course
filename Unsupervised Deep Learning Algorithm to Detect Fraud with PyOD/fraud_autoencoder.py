"""
fraud_autoencoder_pyod.py

Builds and evaluates a fraud detection model using PyOD's AutoEncoder
on the Kaggle anonymized credit card transactions dataset.

- Uses an unsupervised AutoEncoder to detect anomalies (fraud).
- Evaluates model using ROC-AUC, confusion matrix, and classification report.
- Prints metrics so we can capture a screenshot for the report.
"""

import argparse
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pyod.models.auto_encoder import AutoEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)


def load_data(csv_path: str):
    """
    Load the credit card dataset from the given CSV path.

    The Kaggle dataset typically has:
    - Feature columns: V1, V2, ..., V28 + 'Amount'
    - Target column: 'Class' (0 = normal, 1 = fraud)
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    # Basic sanity checks
    if "Class" not in df.columns:
        raise ValueError("Expected a 'Class' column in the dataset.")

    # Separate features and labels
    X = df.drop(columns=["Class"])
    y = df["Class"]

    return X, y


def preprocess_data(X: pd.DataFrame, y: pd.Series, test_size: float = 0.3):
    """
    Split the data into train and test sets, and scale the features.

    We use Stratified split to preserve fraud/normal ratio.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42,
        stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train.values, y_test.values, scaler


def train_autoencoder(X_train: np.ndarray, contamination: float = 0.001):
    """
    Train a PyOD AutoEncoder model on the training data.

    contamination: expected fraction of outliers (fraud) in the data.
    """
    # Minimal call so it works with older/newer PyOD versions
    try:
        # Most PyOD versions support contamination as a keyword
        model = AutoEncoder(contamination=contamination)
    except TypeError:
        # Fallback if contamination is not accepted in __init__
        model = AutoEncoder()
        # If contamination attribute exists, set it (optional, best-effort)
        if hasattr(model, "contamination"):
            model.contamination = contamination

    model.fit(X_train)
    return model


def evaluate_model(model: AutoEncoder, X_test: np.ndarray, y_test: np.ndarray):
    """
    Evaluate the trained AutoEncoder model on the test data.

    Prints:
    - Confusion matrix
    - Classification report
    - ROC-AUC score

    Also returns the anomaly scores and predicted labels.
    """
    # Predicted labels: 0 = inlier (normal), 1 = outlier (fraud)
    y_pred = model.predict(X_test)

    # Outlier scores (higher = more likely fraud)
    y_scores = model.decision_function(X_test)

    # Compute confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("=== Confusion Matrix (rows=true, cols=pred) ===")
    print(cm)
    print()

    # Classification report
    print("=== Classification Report ===")
    print(classification_report(y_test, y_pred, digits=4))
    print()

    # ROC-AUC using anomaly scores
    try:
        roc_auc = roc_auc_score(y_test, y_scores)
        print(f"ROC-AUC (using anomaly scores): {roc_auc:.4f}")
    except ValueError:
        print("ROC-AUC could not be computed (check label distribution).")

    return y_pred, y_scores


def plot_anomaly_scores(y_test: np.ndarray, y_scores: np.ndarray, output_path: str = None):
    """
    Plot histogram of anomaly scores for normal vs fraud transactions.

    This plot is useful to visualize how well the model separates classes.
    You can also screenshot this plot for your assignment.
    """
    fraud_scores = y_scores[y_test == 1]
    normal_scores = y_scores[y_test == 0]

    plt.figure(figsize=(8, 5))
    plt.hist(normal_scores, bins=50, alpha=0.6, label="Normal (Class=0)")
    plt.hist(fraud_scores, bins=50, alpha=0.6, label="Fraud (Class=1)")
    plt.xlabel("Anomaly Score")
    plt.ylabel("Count")
    plt.title("AutoEncoder Anomaly Score Distribution")
    plt.legend()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"Anomaly score histogram saved to: {output_path}")
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Fraud Detection using PyOD AutoEncoder on Kaggle Credit Card dataset."
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default="data/creditcard.csv",
        help="Path to creditcard.csv dataset."
    )
    parser.add_argument(
        "--contamination",
        type=float,
        default=0.001,
        help="Estimated fraction of fraud cases in the data."
    )
    parser.add_argument(
        "--save_plot",
        action="store_true",
        help="If set, save anomaly score histogram instead of just showing it."
    )

    args = parser.parse_args()

    print("Loading data...")
    X, y = load_data(args.data_path)
    print(f"Dataset shape: {X.shape}, Fraud ratio: {y.mean():.6f}")

    print("Preprocessing data (train/test split + scaling)...")
    X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)

    print("Training AutoEncoder model...")
    model = train_autoencoder(X_train, contamination=args.contamination)

    print("Evaluating model on test set...")
    y_pred, y_scores = evaluate_model(model, X_test, y_test)

    print("Plotting anomaly scores...")
    if args.save_plot:
        plot_anomaly_scores(y_test, y_scores, output_path="anomaly_scores_hist.png")
    else:
        plot_anomaly_scores(y_test, y_scores)

    print("Experiment complete.")


if __name__ == "__main__":
    main()
