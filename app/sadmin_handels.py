from run import logger as logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from  run import bot

import db.db as db


sadmin_router = Router()


@sadmin_router.message(Command("set_role"))
async def add_admin(message: Message):
    global id
    users_data = await db.get_all_sadmins()
    await broadcast_sadm_message(message=message, attention='set_role', users_data=users_data)
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
                if new_role == 'admin':
                    await db.set_role(id, 1)
                    await message.reply("Роль изменена!\n"
                                        f"ID: {id}\n"
                                        f"Новая роль: {new_role}\n"
                                        f"Старая роль: {old_role}\n")
                    return
                if new_role == 'sadmin' or new_role == 'super-admin' or new_role == 'superadmin':
                    await db.set_role(id, 2)
                    await message.reply("Роль изменена!\n"
                                        f"ID: {id}\n"
                                        f"Новая роль: {new_role}\n"
                                        f"Старая роль: {old_role}\n")
                    return
                if new_role == 'user':
                    await db.set_role(id, 0)
                    await message.reply("Роль изменена!\n"
                                        f"ID: {id}\n"
                                        f"Новая роль: {new_role}\n"
                                        f"Старая роль: {old_role}\n")
                    return
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
    users_data = await db.get_all_sadmins()
    await broadcast_sadm_message(message=message, attention='drop_id', users_data=users_data)
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
    users_data = await db.get_all_sadmins()
    await broadcast_sadm_message(message=message, attention='drop_blocked', users_data=users_data)
    if await db.is_super_admin(message.from_user.id):
        await db.drop_all_closed()
        logging.critical(
                f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} DROP ALL INACTIVE USERS!")
    else:
        logging.critical(
            f"USER {message.from_user.id} WITH ROLE: {await db.get_role_by_id(message.from_user.id)} WANT TO DROP ALL INACTIVE USERS!")


async def broadcast_sadm_message(message: Message, attention: str, users_data: list):
    global chat_id
    chat_id = message.from_user.id
    await bot.send_message(text=f'Пользователь {message.from_user.username} использвал функцию: {attention}',
                                 chat_id=chat_id)
    for user in users_data:
        try:
            chat_id = user.get('telegram_id')
            if chat_id == message.chat.id:
                await db.change_bot_open_status(chat_id, True)
                continue
            await bot.send_message(
                text=f'Пользователь {message.from_user.username} использвал функцию: {attention}',
                chat_id=chat_id)
            await db.change_bot_open_status(chat_id, True)

            if not user.get('bot_open'):
                await db.change_bot_open_status(chat_id, True)

        except Exception as e:
            logging.error(e)

            if user.get('bot_open'):
                await db.change_bot_open_status(chat_id, False)
