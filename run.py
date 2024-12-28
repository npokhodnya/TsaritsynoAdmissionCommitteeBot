import asyncio
import logging
from multiprocessing import Process

from aiogram import Bot, Dispatcher
import os
import db.db
from utils.parser.parser import Parser
import app.user_handlers as us_h
import aioschedule

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
parser = Parser()


async def main():
    from app.user_handlers import user_router
    from app.sadmin_handels import sadmin_router
    from app.admin_handlers import admin_router
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    await update_all()
    logging.critical("START BOT")
    process = Process(target=on_startup)
    process.start()
    dp.include_routers(user_router, sadmin_router, admin_router)
    await dp.start_polling(bot, on_startup=await init_all())
    process.join()


async def init_all():
    await db.db.initialize_database()


async def update_all():
    logging.warning("Starting update all variables with parser...")
    logging.warning("Starting update docs list...")
    us_h.doc_text = await parser.get_docs_list()
    logging.warning("Complete updating docs list!")
    logging.warning("Starting update work schedule...")
    us_h.schedule_text = await parser.get_work_schedule()
    logging.warning("Complete updating work schedule!")
    logging.warning("Starting update postpoint from army...")
    us_h.army_text = await parser.get_postpoint_from_army()
    logging.warning("Complete updating postpoint from army!")
    logging.warning("Complete updating all variables with parser!")


async def scheduler():
    aioschedule.every().day.at("00:00").do(update_all)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


def on_startup():
    asyncio.run(scheduler())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('LOL')
