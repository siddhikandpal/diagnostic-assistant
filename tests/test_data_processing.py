import pytest
from modules.data_processing import PatientDataProcessor
import pandas as pd
import asyncio

@pytest.mark.asyncio
async def test_load_data():
    """Test loading patient data from a CSV file."""
    processor = PatientDataProcessor("data/mock_patient_data.csv")
    df = await processor.load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

@pytest.mark.asyncio
async def test_get_features_and_target():
    """Test extracting features and target variable."""
    processor = PatientDataProcessor("data/mock_patient_data.csv")
    X, y = await processor.get_features_and_target()
    assert isinstance(X, pd.DataFrame)
    assert isinstance(y, pd.Series)
    assert len(X) == len(y)