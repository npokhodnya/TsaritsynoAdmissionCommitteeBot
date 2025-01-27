from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


keyboard_page1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Как поступить в колледж?', callback_data='How')],
                                                       [InlineKeyboardButton(text='Цифры приёма по специальностям', callback_data='more')],
                                                       [InlineKeyboardButton(text='Специалитет', callback_data='Specialty')],
                                                       [InlineKeyboardButton(text='Этапы зачисления', callback_data='Stages_of_enrollment')],
                                                       [InlineKeyboardButton(text='Страница 2 ->', callback_data='sttngs2')]
                                                       ])

How1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Какие нужны документы?', callback_data='doсs')],
                                            [InlineKeyboardButton(text='В главное меню', callback_data='back1')]
                                                 ])


back2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back2')]
                                                 ])
back3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back3')]
                                                 ])
back_del = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back_del')]
                                                 ])

keyboard_page2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Льготы', callback_data='benefits')],
                                                       [InlineKeyboardButton(text='Проходные баллы', callback_data='Passing_points')],
                                                       [InlineKeyboardButton(text='Время работы приёмной комиссии',callback_data='Opening_hours')],
                                                       [InlineKeyboardButton(text='<- Страница 1', callback_data='sttngs1'),
                                                       InlineKeyboardButton(text='Страница 3 ->', callback_data='sttngs3')]
                                                       ])

keyboard_page3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Дни открытых дверей', callback_data='Doors')],
                                                       [InlineKeyboardButton(text='Отсрочка от армии', callback_data='Seven_nation_army')],
                                                       [InlineKeyboardButton(text='Часто задаваемые вопросы', callback_data='Questions')],
                                                       [InlineKeyboardButton(text='<- Страница 2', callback_data='sttngs2')]
                                                       ])

SpecialtyKeyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Поварское и кондитерское дело', callback_data='cook')],
                                                 [InlineKeyboardButton(text='Туризм и гостеприимство', callback_data='tourism')],
                                                 [InlineKeyboardButton(text='Сервис на транспорте',callback_data='transport')],
                                                 [InlineKeyboardButton(text='Информационные системы и программирование', callback_data='inf')],
                                                 [InlineKeyboardButton(text='Компьютерные системы и комплексы', callback_data='comp_comp')],
                                                 [InlineKeyboardButton(text='В главное меню',callback_data='back1')]
                                                 ])

benefits_Keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Лица с ОВЗ', callback_data='ovz')],
                                                 [InlineKeyboardButton(text='Дети-сироты оставшиеся без попечния родителей', callback_data='orphans')],
                                                 [InlineKeyboardButton(text='Нуждающиеся в социальной поддержке', callback_data='social_support')],
                                                 [InlineKeyboardButton(text='В главное меню', callback_data='back1')]
                                                 ])
back_to_benefits = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back_to_benefits')]
                                                 ])


Doors_Keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Перейти на сайт', url = 'https://collegetsaritsyno.mskobr.ru/postuplenie-v-kolledzh/dni-otkrytyh-dverej')],
                                                 [InlineKeyboardButton(text='В главное меню', callback_data='back1')]
                                                 ])

Chanel_Keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Подписаться на канал', url = 'https://t.me/+GOhYfBSGvXc1ZGIy')]])

back1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В главное меню', callback_data='back1')]
                                                 ])
