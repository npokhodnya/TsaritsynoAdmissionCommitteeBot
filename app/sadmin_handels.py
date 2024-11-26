import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import db.db as db

sadmin_router = Router()


@sadmin_router.message(Command("set_role"))
async def add_admin(message: Message):
    global id
    if await db.is_super_admin(message.from_user.id):
        args = message.text.split(" ")
        if len(args) == 3:
            try:
                id = int(args[1])
                new_role = args[2]
                old_role = await db.get_role_by_id(id)
                if old_role in ["sadmin", 'developer']:
                    await message.reply("ОШИБКА! Невозможно сменить роль для суперадмина!")
                    return
                await db.set_role(id, new_role)
                await message.reply("Роль изменена!\n"
                                    f"ID: {id}\n"
                                    f"Новая роль: {new_role}\n"
                                    f"Старая роль: {old_role}\n")
                logging.critical(
                    f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} CHANGE ROLE FOR USER {id} FROM {old_role} TO {new_role}")
            except Exception as e:
                await message.reply(str(e))
                logging.warning(
                    f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} TRY TO CHANGE ROLE FOR USER {id} BUT ERROR: {e}")
        else:
            await message.reply(f"ОШИБКА! Введено {len(args) - 1} аргументов, когда ожидается 2")
            logging.warning(
                f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} TRY TO CHANGE ROLE FOR {id} BUT NOT ENOUGH ARGS")
    else:
        logging.critical(
            f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} WANT TO CHANGE ROLE FOR {id} WITHOUT RIGHTS")

@sadmin_router.message(Command("drop_id"))
async def drop_id(message: Message):
    global id
    if await db.is_super_admin(message.from_user.id):
        args = message.text.split(" ")
        if len(args) == 2:
            try:
                id = int(args[1])
                old_role = await db.get_role_by_id(id)
                if not await db.is_developer(message.from_user.id):
                    if old_role in ["sadmin", 'developer']:
                        await message.reply("ОШИБКА! Невозможно сменить роль для суперадмина!")
                        return
                await db.drop_user_by_id(id)
                await message.reply(f"Пользователь с ID: {id} и ROLE: {old_role} успешно удален из базы данных!")
                logging.critical(
                    f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} DROP USER {id} WITH ROLE {old_role}")
            except Exception as e:
                await message.reply(str(e))
                logging.warning(
                    f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} TRY TO DROP USER {id} BUT ERROR: {e}")
        else:
            await message.reply(f"ОШИБКА! Введено {len(args) - 1} аргументов, когда ожидается 1")
            logging.warning(
                f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} TRY TO DROP USER {id} BUT NOT ENOUGH ARGS")
    else:
        logging.critical(
            f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} WANT TO DROP USER {id} WITHOUT RIGHTS")


@sadmin_router.message(Command("drop_blocked"))
async def drop_blocked(message: Message):
    if await db.is_super_admin(message.from_user.id):
        await db.drop_all_closed()
        logging.critical(
                f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} DROP ALL INACTIVE USERS!")
    else:
        logging.critical(
            f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} WANT TO DROP ALL INACTIVE USERS!")