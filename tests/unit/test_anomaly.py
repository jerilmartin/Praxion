"""
Unit tests – Anomaly Detection feature extraction
"""
import pytest
import numpy as np

# Placeholder – actual import once AnomalyDetectionAgent is implemented
# from backend.agents.anomaly.anomaly_agent import AnomalyDetectionAgent


def test_isolation_forest_scores_shape():
    """Smoke test: IsolationForest accepts the expected feature shape."""
    from sklearn.ensemble import IsolationForest
    X = np.array([
        [100, 0,  5, 200, 10],
        [200, 5, 10, 500, 20],
        [5000, 50, 50, 5000, 200],   # simulated anomaly
    ])
    model = IsolationForest(n_estimators=100, random_state=42)
    model.fit(X)
    scores = model.score_samples(X)
    assert scores.shape == (3,)
    # Anomaly should have the lowest score
    assert scores.argmin() == 2
