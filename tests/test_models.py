import pytest
from modules.models import RandomForestTriageModel
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

def test_triage_model_training():
    """Test training the triage model."""
    X, y = make_classification(n_samples=100, n_features=4, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestTriageModel()
    model.train(X_train, y_train)

    predictions = model.predict(X_test)
    assert len(predictions) == len(y_test)

def test_triage_model_evaluation():
    """Test evaluating the triage model."""
    X, y = make_classification(n_samples=100, n_features=4, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestTriageModel()
    model.train(X_train, y_train)

    report = model.evaluate(X_test, y_test)
    assert isinstance(report, str)