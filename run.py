import asyncio
import logging
from multiprocessing import Process
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import os
import db.db
from utils.parser.parser import Parser
import app.user_handlers as us_h
import aioschedule
from logging.handlers import RotatingFileHandler

load_dotenv("config.env")
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
parser = Parser(browser="chrome")
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
file_handler_info_warning = logging.handlers.RotatingFileHandler("info_warning.log", maxBytes=1073741824, backupCount=1)
file_handler_info_warning.setLevel(logging.INFO)
file_handler_critical = logging.handlers.RotatingFileHandler("critical.log", maxBytes=1073741824, backupCount=1)
file_handler_critical.setLevel(logging.CRITICAL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler_info_warning.setFormatter(formatter)
file_handler_critical.setFormatter(formatter)
logger.addHandler(file_handler_info_warning)
logger.addHandler(file_handler_critical)


async def main():
    from app.user_handlers import user_router
    from app.sadmin_handels import sadmin_router
    from app.admin_handlers import admin_router
    await update_all()
    logger.critical("START BOT")
    process = Process(target=on_startup)
    process.start()
    dp.include_routers(user_router, sadmin_router, admin_router)
    await dp.start_polling(bot, on_startup=await init_all())
    process.join()


async def init_all():
    await db.db.initialize_database()


async def update_all():
    logger.warning("Starting update all variables with parser...")
    logger.warning("Starting update docs list...")
    us_h.doc_text = await parser.get_docs_list()
    logger.warning("Complete updating docs list!")
    logger.warning("Starting update work schedule...")
    us_h.schedule_text = await parser.get_work_schedule()
    logger.warning("Complete updating work schedule!")
    logger.warning("Starting update postpoint from army...")
    us_h.army_text = await parser.get_postpoint_from_army()
    logger.warning("Complete updating postpoint from army!")
    logger.warning("Complete updating all variables with parser!")


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
