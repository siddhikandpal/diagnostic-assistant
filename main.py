import asyncio
from containers import Container
import logging
from modules.allocation import HospitalResourceAllocator  # Import manually

container = Container()

# ✅ Debugging: Check if YAML is loading correctly
try:
    container.config.from_yaml("config/config.yaml")
    print("✅ Config Loaded Successfully:")
    print(container.config())  # Should be a dictionary
    print("✅ Type of config:", type(container.config()))  # Should be <class 'dict'>
except Exception as e:
    print(f"❌ Error loading config: {e}")

async def main():
    try:
        data_processor = container.data_processor()
        print("✅ Data Processor Loaded Successfully")

        X, y = await data_processor.get_features_and_target()
        print("✅ Features and Target Loaded")
        print("🔹 X (features):", X)
        print("🔹 y (target):", y)

        triage_model = container.triage_model()
        print("✅ Triage Model Loaded Successfully")

        triage_model.train(X, y)
        evaluation_report = triage_model.evaluate(X, y)
        print("✅ Triage Model Evaluation:")
        print(evaluation_report)

        # ✅ Fix: Remove 'await' when calling allocate_resources()
        allocator = HospitalResourceAllocator(
            hospitals=container.config.hospitals(),
            data_file=container.config.data.file()
        )
        print("✅ Resource Allocator Loaded Successfully")

        allocator.allocate_resources()  # ✅ Fixed: No 'await' since it's no longer async

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
