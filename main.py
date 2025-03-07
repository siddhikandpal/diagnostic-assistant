import asyncio
from containers import Container
import logging

container = Container()
container.config.from_yaml("config/config.yaml")

# logging.basicConfig(
#     level=container.config.logging.level,
#     format=container.config.logging.format,
#     filename=container.config.logging.file
# )
# logger = logging.getLogger(__name__)

async def main():
    try:
        data_processor = container.data_processor()
        X, y = await data_processor.get_features_and_target()

        triage_model = container.triage_model()
        triage_model.train(X, y)
        evaluation_report = triage_model.evaluate(X, y)
        print("Triage Model Evaluation:")
        print(evaluation_report)

        allocator = container.resource_allocator()
        await allocator.allocate_resources()

    except Exception as e:
        print(f"An error occurred: {e}")
        pass


if __name__ == "__main__":
    asyncio.run(main())