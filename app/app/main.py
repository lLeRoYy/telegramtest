import asyncio

from loguru import logger

from app.handlers.routing import get_all_routers
from app.middlewares.throttling import rate_limit_middleware
from app.core.container import Container
from app.scripts import create_super_user
from app import handlers

from loader import dp, bot


async def main():
    """Запуск бота."""
    try:
        all_routers = get_all_routers()
        dp.include_routers(all_routers)
        dp.message.middleware(rate_limit_middleware)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    container = Container()
    container.wire(modules=[create_super_user, handlers])
    logger.info("Bot is starting")
    asyncio.run(main())
