import logging

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import db.db as db

import app.admin_keyboards as akb
from app.user_handlers import cmd_start

from run import bot

admin_router = Router()


class Form(StatesGroup):
    start_broadcast = State()

@admin_router.callback_query(F.data == 'ucount')
async def page2(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await db.is_admin(user_id):
        cu = await db.count_of_users()
        await callback.message.edit_text(text=f'Пользователей бота: {cu}',
                                         reply_markup=akb.back)
    else:
        logging.warning(f"User {user_id} with role {await db.get_role_by_id(user_id)} try to check count of users")


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
        logging.warning(f"User {user_id} with role {await db.get_role_by_id(user_id)} try to start broadcast")


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