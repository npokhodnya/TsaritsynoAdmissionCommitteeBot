from run import logger as logging

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import db.db as db

import app.admin_keyboards as akb
from app.user_handlers import cmd_start

from run import bot, parser, update_all

import app.user_handlers as us_h

admin_router = Router()


class Form(StatesGroup):
    start_broadcast = State()


@admin_router.callback_query(F.data == 'ucount')
async def page2(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await db.is_admin(user_id):
        await callback.message.edit_text(
            text=f'Пользователей бота, включая вас: {await db.count_of_users()}, из них {await db.count_of_closed_users()} заблокировали бота',
            reply_markup=akb.back)
        logging.warning(
            f"USER {callback.from_user.id} WITH ROLE: {await db.get_role_by_id(callback.from_user.id)} CHECK COUNT OF USERS")
    else:
        logging.warning(f"User {user_id} with role {await db.get_role_by_id(user_id)} try to check count of users")


@admin_router.message(Command("update_docs"))
async def update_docs(message: Message):
    user_id = message.from_user.id
    if await db.is_admin(user_id):
        msg = await message.answer("Обновление данных о документах...")
        try:
            us_h.doc_text = await parser.get_docs_list()
            logging.info(f"User {user_id} with role {await db.get_role_by_id(user_id)} update info about docs")
            await bot.edit_message_text("Данные о документах обновлены!", chat_id=message.chat.id,
                                        message_id=msg.message_id)
        except Exception as e:
            await bot.edit_message_text(f"Данные о документах не были обновлены!\nОшибка: {e}", chat_id=message.chat.id,
                                        message_id=msg.message_id)
            logging.error(f"User {user_id} with role {await db.get_role_by_id(user_id)} try update info about army, but error {e}")
    else:
        logging.warning(f"User {user_id} with role {await db.get_role_by_id(user_id)} try to update info about docs")


@admin_router.message(Command("update_army"))
async def update_army(message: Message):
    user_id = message.from_user.id
    if await db.is_admin(user_id):
        msg = await message.answer("Обновление данных об отсрочке...")
        try:
            us_h.army_text = await parser.get_postpoint_from_army()
            logging.info(f"User {user_id} with role {await db.get_role_by_id(user_id)} update info about army")
            await bot.edit_message_text("Данные о документах обновлены!", chat_id=message.chat.id,
                                        message_id=msg.message_id)
        except Exception as e:
            await bot.edit_message_text(f"Данные о документах не были обновлены!\nОшибка: {e}", chat_id=message.chat.id,
                                        message_id=msg.message_id)
            logging.error(
                f"User {user_id} with role {await db.get_role_by_id(user_id)} try update info about army, but error {e}")
    else:
        logging.warning(f"User {user_id} with role {await db.get_role_by_id(user_id)} try to update info about army")


@admin_router.message(Command("update_schedule"))
async def update_schedule(message: Message):
    user_id = message.from_user.id
    if await db.is_admin(user_id):
        msg = await message.answer("Обновление данных о времени работы приемной комиссии...")
        try:
            us_h.schedule_text = await parser.get_work_schedule()
            await bot.edit_message_text("Данные о времени работы приемной комиссии обновлены!", chat_id=message.chat.id,
                                        message_id=msg.message_id)
            logging.info(f"User {user_id} with role {await db.get_role_by_id(user_id)} update info about work schedule")

        except Exception as e:
            await bot.edit_message_text(f"Данные о документах не были обновлены!\nОшибка: {e}", chat_id=message.chat.id,
                                        message_id=msg.message_id)
            logging.error(
                f"User {user_id} with role {await db.get_role_by_id(user_id)} try update info about army, but error {e}")
    else:
        logging.warning(f"User {user_id} with role {await db.get_role_by_id(user_id)} try to update info about army")


@admin_router.callback_query(F.data == 'mailing')
async def admin_broadcast_handler(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if await db.is_admin(user_id):
        await call.answer()
        await call.message.answer(
            'Отправьте любое сообщение, а я его перехвачу и перешлю всем пользователям с базы данных',
            reply_markup=akb.cancel_kb
        )
        await state.set_state(Form.start_broadcast)
    else:
        logging.warning(f"User {user_id} with role {await db.get_role_by_id(user_id)} try to check count of users")


@admin_router.callback_query(F.data == 'admin_sttngs1')
async def admin_page2(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{callback.from_user.first_name}{", добро пожаловать"}',
                                     reply_markup=akb.admin_keyboard2)


@admin_router.callback_query(F.data == 'admin_sttngs2')
async def admin_page1(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{callback.from_user.first_name}{", добро пожаловать"}',
                                     reply_markup=akb.admin_keyboard1)


async def broadcast_message(message: Message, users_data: list, text: str = None, photo_id: int = None,
                            document_id: int = None,
                            video_id: int = None, audio_id: int = None, animation_id: int = None,
                            video_note_id: int = None, voice_id: int = None, caption: str = None,
                            content_type: str = None):
    global chat_id
    good_send = 0
    bad_send = 0
    total = len(users_data)

    msg = await bot.send_message(text='Отпрвка сообщений...\n'
                                      f'Удачно: {good_send}\nНе удачно: {bad_send}\nОсталось: {total - bad_send - good_send}',
                                 chat_id=message.chat.id)

    for user in users_data:
        try:
            chat_id = user.get('telegram_id')

            if chat_id == message.chat.id:
                good_send += 1
                msg = await bot.edit_message_text(text='Отправка сообщений...!\n'
                                                       f'Удачно: {good_send}\nНе удачно: {bad_send}\nОсталось: {total - bad_send - good_send}',
                                                  chat_id=msg.chat.id, message_id=msg.message_id)
                await db.change_bot_open_status(chat_id, True)
                continue

            elif content_type == ContentType.TEXT:
                await bot.send_message(chat_id=chat_id, text=text,
                                       reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif content_type == ContentType.PHOTO:
                await bot.send_photo(chat_id=chat_id, photo=photo_id, caption=caption,
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif content_type == ContentType.DOCUMENT:
                await bot.send_document(chat_id=chat_id, document=document_id, caption=caption,
                                        reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif content_type == ContentType.VIDEO:
                await bot.send_video(chat_id=chat_id, video=video_id, caption=caption,
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif content_type == ContentType.AUDIO:
                await bot.send_audio(chat_id=chat_id, audio=audio_id, caption=caption,
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif content_type == ContentType.ANIMATION:
                await bot.send_animation(chat_id=chat_id, animation=animation_id,
                                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif content_type == ContentType.VIDEO_NOTE:
                await bot.send_video_note(chat_id=chat_id, video_note=video_note_id,
                                          reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif content_type == ContentType.VOICE:
                await bot.send_voice(chat_id=chat_id, voice=voice_id,
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            good_send += 1

            if not user.get('bot_open'):
                await db.change_bot_open_status(chat_id, True)

            msg = await bot.edit_message_text(text='Отправка сообщений...!\n'
                                                   f'Удачно: {good_send}\nНе удачно: {bad_send}\nОсталось: {total - bad_send - good_send}',
                                              chat_id=msg.chat.id, message_id=msg.message_id)
        except Exception as e:
            logging.error(e)
            bad_send += 1

            if user.get('bot_open'):
                await db.change_bot_open_status(chat_id, False)

            msg = await bot.edit_message_text(text='Отправка сообщений...!\n'
                                                   f'Удачно: {good_send}\nНе удачно: {bad_send}\nОсталось: {total - bad_send - good_send}',
                                              chat_id=msg.chat.id, message_id=msg.message_id)

    await bot.edit_message_text(text='Сообщения отправлены!\n'
                                     f'Удачно: {good_send}\nНе удачно: {bad_send}\nОсталось: {total - bad_send - good_send}',
                                chat_id=msg.chat.id, message_id=msg.message_id)

    await bot.send_message(text='Рассылка завершена', chat_id=msg.chat.id,
                           reply_markup=ReplyKeyboardRemove(remove_keyboard=True))


@admin_router.message(
    F.content_type.in_({'text', 'photo', 'document', 'video', 'audio', 'animation', 'video_note', 'voice'}),
    Form.start_broadcast)
async def universe_broadcast(message: Message, state: FSMContext):
    content_type = message.content_type
    if content_type == ContentType.TEXT and message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Рассылка отменена!', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return

    users_data = await db.get_all_users()

    await broadcast_message(
        message=message,
        users_data=users_data,
        text=message.text if content_type == ContentType.TEXT else None,
        photo_id=message.photo[-1].file_id if content_type == ContentType.PHOTO else None,
        document_id=message.document.file_id if content_type == ContentType.DOCUMENT else None,
        video_id=message.video.file_id if content_type == ContentType.VIDEO else None,
        audio_id=message.audio.file_id if content_type == ContentType.AUDIO else None,
        animation_id=message.animation.file_id if content_type == ContentType.ANIMATION else None,
        video_note_id=message.video_note.file_id if content_type == ContentType.VIDEO_NOTE else None,
        voice_id=message.voice.file_id if content_type == ContentType.VOICE else None,
        caption=message.caption,
        content_type=content_type
    )
    await state.clear()
    await cmd_start(message)


@admin_router.message(Command('update_all'))
async def update_all_vars(message: Message):
    msg = await message.answer("Обновление всех данных...")
    await update_all()
    await msg.edit_text("Все данные обновлены!")
