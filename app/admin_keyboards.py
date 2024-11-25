from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


admin_keyboard1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Массовая рассылка', callback_data='mailing')],
                                                        [InlineKeyboardButton(text='Посмотреть кол-во пользователей', callback_data='ucount')],
                                                        [InlineKeyboardButton(text='Страница 1 ->', callback_data='admin_sttngs1')]
                                                        ])

admin_keyboard2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Как поступить в колледж?', callback_data='How')],
                                                        [InlineKeyboardButton(text='Цифры приёма по специальностям', callback_data='more')],
                                                        [InlineKeyboardButton(text='Специалитет', callback_data='Specialty')],
                                                        [InlineKeyboardButton(text='Этапы зачисления', callback_data='Stages_of_enrollment')],
                                                        [InlineKeyboardButton(text='<- Страница Администратора', callback_data='admin_sttngs2'),
                                                         InlineKeyboardButton(text='Страница 2 ->', callback_data='sttngs2')]
                                                        ])

cancel_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )

back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В главное меню', callback_data='back1')]
                                                 ])
