from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


sadmin_keyboard1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Массовая рассылка', callback_data='mailing'), InlineKeyboardButton(text='Посмотреть кол-во пользователей', callback_data='ucount')],
                                                         [InlineKeyboardButton(text="Получить логи", callback_data='send_logs'), InlineKeyboardButton(text="Получить базу данных пользователей", callback_data='send_db')],
                                                        [InlineKeyboardButton(text='Страница 1 ->', callback_data='sadmin_sttngs1')]
                                                        ])

sadmin_keyboard3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='EXCEL таблица', callback_data='mode_xls'),
                                                          InlineKeyboardButton(text='DB файл', callback_data='mode_db')],
                                                         [InlineKeyboardButton(text='CSV таблица', callback_data='mode_csv')],
                                                         [InlineKeyboardButton(text='Назад', callback_data='back1')]])


sadmin_keyboard2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Как поступить в колледж?', callback_data='How')],
                                                        [InlineKeyboardButton(text='Цифры приёма по специальностям', callback_data='more')],
                                                        [InlineKeyboardButton(text='Специалитет', callback_data='Specialty')],
                                                        [InlineKeyboardButton(text='Этапы зачисления', callback_data='Stages_of_enrollment')],
                                                        [InlineKeyboardButton(text='<- Страница Супер-Администратора', callback_data='sadmin_sttngs2'),
                                                         InlineKeyboardButton(text='Страница 2 ->', callback_data='sttngs2')]
                                                        ])

cancel_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )

back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В главное меню', callback_data='back1')]])
