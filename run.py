import asyncio
import logging
from aiogram import Bot, Dispatcher
import os
import db.db
from utils.parser.parser import Parser

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
parser = Parser()

async def main():
    from app.user_handlers import user_router
    from app.sadmin_handels import sadmin_router
    from app.admin_handlers import admin_router
    dp.include_routers(user_router, sadmin_router, admin_router)
    await db.db.initialize_database()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.critical("START BOT")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
