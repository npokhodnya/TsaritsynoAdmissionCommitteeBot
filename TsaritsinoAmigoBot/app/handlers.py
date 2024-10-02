from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb

router = Router()

grp = ''
start_text2 = 'Сейчас идут тех работы, функция недоступна :('
start_text = ', здаствуйте. Этот бот поможет вам с поступлением в один из лучших колледжей Москвы. Ниже вы можете выбрать интересующие вас детали.'

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'{message.from_user.first_name}{start_text}',
                         reply_markup=kb.settings1)

@router.callback_query(F.data == 'sttngs1')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{callback.from_user.first_name}{start_text}',
                         reply_markup=kb.settings1)

@router.callback_query(F.data == 'sttngs2')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{callback.from_user.first_name}{start_text}',
                         reply_markup=kb.settings2)

@router.callback_query(F.data == 'sttngs3')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{callback.from_user.first_name}{start_text}',
                         reply_markup=kb.settings3)

@router.callback_query(F.data == 'How')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text='Чтобы поступить в колледж на бюджет, нужно подать документы в приемную комиссию. Делается это на портале мос.ру, на котором вы уже должны быть зарегистрированы (если же у вас там нет аккаунта, то сначала вам нужно зарегистрироваться). Заявления принимаются с 20 июня по 15 августа. Для поступления на платное обучение необходимо приходить в приёмную комиссию.',
                         reply_markup=kb.How1)

@router.callback_query(F.data == 'back2')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text='Чтобы поступить в колледж на бюджет, нужно подать документы в приемную комиссию. Делается это на портале мос.ру, на котором вы уже должны быть зарегистрированы (если же у вас там нет аккаунта, то сначала вам нужно зарегистрироваться). Заявления принимаются с 20 июня по 15 августа. Для поступления на платное обучение необходимо приходить в приёмную комиссию.',
                         reply_markup=kb.How1)

@router.callback_query(F.data == 'doсs')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text='Какие же нужны документы для поступления ? \nВам нужно: \n1)Аттестат (оригинал + копия)\n2)Паспорт + копия паспорта. (На одном листе должен быть разворот с фото и разворот с регистрацией)\n3)4 штуки цветные фотографии 3х4 (Нужны для студенческого билета и зачетной книжки)\n4)Медицинская справка № 086-у\n5)Копия страхового медицинского полиса\n6)СНИЛС + копия\n7)Справка об инвалидности (Если имеется)\n8)Грамоты за личные достижения в школе (World skills, abilympics и пр.)\n9) Льготы при наличии',
                         reply_markup=kb.back2)

@router.message(F.text == 'пон')
async def get_help(message: Message):
    await message.reply('¯\_(ツ)_/¯')

@router.callback_query(F.data == 'more')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{start_text2}',
                                  reply_markup=kb.back1)

@router.callback_query(F.data == 'back1')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{callback.from_user.first_name}{start_text}',
                         reply_markup=kb.settings1)

@router.callback_query(F.data == 'Specialty')
async def more(callback: CallbackQuery):
    await callback.message.edit_text('Специальности Колледжа "Царицыно"\nКолледж имеет 3 отделения:\n1)Генерала Белова 6 (Отделение управления и информационных технологий ОУИТ)\n2)Генерала Белова 4 (Политехническое отделение ОП)\n3)Шипиловский проезд 37 (Отделение гостиничного и ресторанного бизнеса ОГРБ)',
                                  reply_markup=kb.SpecialtyKeyboard)

@router.callback_query(F.data == 'schedule2')
async def more(callback: CallbackQuery):
    await callback.message.edit_text('Здесь будут данные о расписании пар (на неделю или день)',reply_markup=kb.back1)

@router.callback_query(F.data == 'class_call')
async def more(callback: CallbackQuery):
    await callback.message.edit_text('Первая пара: 9:00-10:30\nВторая пара: 10:50-12:20\nТретья пара: 12:40-14:10\nЧетвёртая пара: 14:30-16:00\nПятая пара: 16:10-17:40\n\nУдачного обучения!',
                                  reply_markup=kb.back1)

@router.callback_query(F.data == 'feedback')
async def more(callback: CallbackQuery):
    await callback.message.edit_text('Здесь будут данные для обратной связи со всей администрации с которой студент говорить может (психолог, фридман, Максимова итд)',
                                  reply_markup=kb.back1)