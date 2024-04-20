import asyncio

from dotenv import load_dotenv

from presentation.core.dependencies.Dependencies import Dependencies
from presentation.util.Constants import QUALITY_MODEL_LIST_SCREEN


async def main():
    load_dotenv()
    dependencies = Dependencies()

    asyncio.create_task(dependencies.shared_view_model.fetch_quality_models())
    await dependencies.navigator.navigate_to(QUALITY_MODEL_LIST_SCREEN)

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    await asyncio.gather(*tasks)
    dependencies.dispose()


if __name__ == "__main__":
    asyncio.run(main())
