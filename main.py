import asyncio
from containers import Container
from modules.data_processing import PatientDataProcessor
from modules.models import RandomForestTriageModel
from modules.allocation import HospitalResourceAllocator
from modules.forecasting import ResourceDemandForecaster
import logging

# Load configuration
container = Container()
container.config.from_yaml("config/config.yaml")

# Configure logging
logging.basicConfig(level=container.config.logging.level, format=container.config.logging.format, filename=container.config.logging.file)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Step 1: Data Processing
        data_processor = container.data_processor()
        X, y = await data_processor.get_features_and_target()

        # Step 2: Triage Model
        triage_model = container.triage_model()
        triage_model.train(X, y)
        evaluation_report = triage_model.evaluate(X, y)
        print("Triage Model Evaluation:")
        print(evaluation_report)

        # Step 3: Resource Allocation
        allocator = container.resource_allocator()
        await allocator.allocate_resources()

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())