import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import TOKEN
import db.db
bot = Bot(token=TOKEN)
dp = Dispatcher()

kb_list = [{'label': 'Руд болото', 'url': 'https://t.me/+GOhYfBSGvXc1ZGIy'}]


async def main():
    from app.user_handlers import user_router
    from app.sadmin_handels import sadmin_router
    from app.admin_handlers import admin_router
    dp.include_routers(user_router, sadmin_router, admin_router)
    await dp.start_polling(bot)
    await db.db.initialize_database()


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.critical("START BOT")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
