"""
Isolation Forest training script.

Usage:
    python ml/anomaly_detection/train.py --agent-id <id> --output ml/models/isolation_forest.joblib

Reads activity logs from the database (or a CSV export) and trains a
scikit-learn IsolationForest model for agent behavioural anomaly detection.
"""
from __future__ import annotations
import argparse
import joblib
import numpy as np
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


FEATURE_NAMES = [
    "total_tool_calls",
    "auth_failure_count",
    "unique_operations",
    "avg_execution_time_ms",
    "calls_per_minute",
]

MODEL_OUTPUT = Path("ml/models/isolation_forest.joblib")


def load_features(source: str) -> np.ndarray:
    """
    Load feature matrix from a CSV file or database query.
    CSV columns must match FEATURE_NAMES.

    TODO: replace CSV path with live DB query using SQLAlchemy.
    """
    import pandas as pd
    df = pd.read_csv(source)
    return df[FEATURE_NAMES].values


def build_pipeline(contamination: float = 0.05) -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("iso_forest", IsolationForest(
            n_estimators=200,
            contamination=contamination,
            random_state=42,
            n_jobs=-1,
        )),
    ])


def train(features: np.ndarray, contamination: float = 0.05) -> Pipeline:
    pipeline = build_pipeline(contamination)
    pipeline.fit(features)
    return pipeline


def main():
    parser = argparse.ArgumentParser(description="Train Praxion anomaly detection model")
    parser.add_argument("--source", required=True, help="Path to feature CSV or 'db'")
    parser.add_argument("--contamination", type=float, default=0.05)
    parser.add_argument("--output", default=str(MODEL_OUTPUT))
    args = parser.parse_args()

    print(f"Loading features from {args.source} ...")
    X = load_features(args.source)

    print(f"Training IsolationForest on {X.shape[0]} samples ...")
    model = train(X, args.contamination)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    print(f"Model saved to {output_path}")


if __name__ == "__main__":
    main()
