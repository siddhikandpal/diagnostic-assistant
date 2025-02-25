import pandas as pd
import aiofiles
import asyncio
import logging

logger = logging.getLogger(__name__)

class PatientDataProcessor:
    """Processes patient data for triage and resource allocation."""

    def __init__(self, data_file):
        self.data_file = data_file

    async def load_data(self):
        """Asynchronously load patient data from a CSV file."""
        logger.info("Loading patient data.")
        async with aiofiles.open(self.data_file, mode='r') as f:
            content = await f.read()
        return pd.read_csv(pd.compat.StringIO(content))

    async def get_features_and_target(self):
        """Extract features and target variable from the dataset."""
        df = await self.load_data()
        X = df[['heart_rate', 'blood_pressure', 'oxygen_level', 'injury_severity']]
        y = df['triage_category']
        return X, y