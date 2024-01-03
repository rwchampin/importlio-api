# async_script.py

import asyncio
from posts.manager import Manager

async def run_manager():
    manager = Manager()
    await manager.main()

if __name__ == "__main__":
    asyncio.run(run_manager())
