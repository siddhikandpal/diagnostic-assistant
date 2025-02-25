import pytest
from modules.forecasting import ResourceDemandForecaster
import pandas as pd
import numpy as np

def test_forecaster_training():
    """Test training the resource demand forecaster."""
    dates = pd.date_range(start='2023-10-01', periods=30, freq='D')
    resource_demand = np.random.randint(10, 50, size=30)

    forecaster = ResourceDemandForecaster()
    forecaster.train(dates, resource_demand)

    # Add assertions to verify the training process
    # For example, check if the model is trained successfully

def test_forecaster_forecasting():
    """Test generating a resource demand forecast."""
    dates = pd.date_range(start='2023-10-01', periods=30, freq='D')
    resource_demand = np.random.randint(10, 50, size=30)

    forecaster = ResourceDemandForecaster()
    forecaster.train(dates, resource_demand)

    forecast = forecaster.forecast(periods=7)
    assert isinstance(forecast, pd.DataFrame)
    assert not forecast.empty