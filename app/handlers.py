from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
VERSION = '0.1.2'
DEVELOPERS = ['dev1', 'dev2']
import app.keyboards as kb

router = Router()

start_text2 = 'Сейчас идут тех работы, функция недоступна :('
start_text = (', здаствуйте. Этот бот поможет вам с поступлением в один из лучших колледжей Москвы. Ниже вы можете '
              'выбрать интересующие вас детали.')
text3 = ('Специальности Колледжа "Царицыно"\nКолледж имеет 3 отделения:\n1)Генерала Белова 6 (Отделение управления и '
         'информационных технологий ОУИТ)\n2)Генерала Белова 4 (Политехническое отделение ОП)\n3)Шипиловский проезд '
         '37 (Отделение гостиничного и ресторанного бизнеса ОГРБ)')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'{message.from_user.first_name}{start_text}',
                         reply_markup=kb.settings1)


@router.message(Command('about'))
async def cmd_about(message: Message):
    await message.answer(f"-- version: {VERSION}\n-- developers: {', '.join(DEVELOPERS)}")


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
    await callback.message.edit_text(
        text='Чтобы поступить в колледж на бюджет, нужно подать документы в приемную комиссию. Делается это на '
             'портале мос.ру, на котором вы уже должны быть зарегистрированы (если же у вас там нет аккаунта, '
             'то сначала вам нужно зарегистрироваться). Заявления принимаются с 20 июня по 15 августа. Для '
             'поступления на платное обучение необходимо приходить в приёмную комиссию.',
        reply_markup=kb.How1)


@router.callback_query(F.data == 'back2')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Чтобы поступить в колледж на бюджет, нужно подать документы в приемную комиссию. Делается это на '
             'портале мос.ру, на котором вы уже должны быть зарегистрированы (если же у вас там нет аккаунта, '
             'то сначала вам нужно зарегистрироваться). Заявления принимаются с 20 июня по 15 августа. Для '
             'поступления на платное обучение необходимо приходить в приёмную комиссию.',
        reply_markup=kb.How1)


@router.callback_query(F.data == 'back3')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{text3}',
                                     reply_markup=kb.SpecialtyKeyboard)


@router.callback_query(F.data == 'doсs')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Какие же нужны документы для поступления ? \nВам нужно: \n1)Аттестат (оригинал + копия)\n2)Паспорт + '
             'копия паспорта. (На одном листе должен быть разворот с фото и разворот с регистрацией)\n3)4 штуки '
             'цветные фотографии 3х4 (Нужны для студенческого билета и зачетной книжки)\n4)Медицинская справка № '
             '086-у\n5)Копия страхового медицинского полиса\n6)СНИЛС + копия\n7)Справка об инвалидности (Если '
             'имеется)\n8)Грамоты за личные достижения в школе (World skills, abilympics и пр.)\n9) Льготы при наличии',
        reply_markup=kb.back2)


@router.callback_query(F.data == 'cook')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(
        text='По специальности 43.02.15 Поварское и кондитерское дело адреса обучения:\n- адрес обучения: ул. '
             'Шипиловский пр-д, дом 37, корп.1 бюджет и платное- 9 и 11 класс\n- адрес обучения: ул. Генерала Белова '
             'дом 4 бюджет- 9 класс',
        reply_markup=kb.back3)


@router.callback_query(F.data == 'tourism')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text='здесь нужны файлы',
                                     reply_markup=kb.back3)


@router.callback_query(F.data == 'transport')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text='здесь нужны файлы',
                                     reply_markup=kb.back3)


@router.callback_query(F.data == 'inf')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(
        text='По специальности 09.02.07 Информационные системы и программирование прием осуществляется по '
             'направлениям:\n-программист (бюджет и платное обучение) (адрес обучения: ул. Шипиловский пр-д, дом 37, '
             'корп.1; ул. Генерала Белова дом 6)\n-разработчик ВЭБ и мультимедийных приложений (бюджет и платное '
             'обучение) (адрес обучения: ул. Генерала Белова дом 6)\n-специалист по информационным системам ('
             'бюджетное обучение) (адрес обучения: ул. Генерала Белова дом 4)',
        reply_markup=kb.back3)


@router.callback_query(F.data == 'information_and_communication')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text='здесь нужны файлы',
                                     reply_markup=kb.back3)


@router.callback_query(F.data == 'sysadm')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text='здесь нужны файлы',
                                     reply_markup=kb.back3)


@router.callback_query(F.data == 'Stages_of_enrollment')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Этап 1 (20 июня - 15 августа)\nШаги:\n1) Подача заявления на бюджет через мос.ру и/или в пиёмную '
             'комиссию колледжа. Подача заявления на платное обучение производится толко в приёмной комиссии '
             'колледжа.\n2) Подготовка документов необходимых для поступления в колледж.\n3) Для граждан льготной '
             'категории предосталение в приёмную комиссию документов подтверждающих льготу.\n4) Отслеживание на '
             'офицальном сайте колледжа изменения по проходному баллу выбранной специальности.\n5) Предоставление '
             'оригиналов документов в приёмную комиссию колледжа.\nЭтап 2 (15 - 22 августа)\nПроведение конкурса '
             'аттестатов для поступления на бюджетные места.\nЭтап 3 (22 - 30 августа)\nПри получении на портале '
             'мос.ру информации о рекомендации к зачислению, прикрепление скана справки 086у\nЭтап 4 (22 августа - 30 '
             'октября)\nИздание приказов на зачисление в колледж и приём абитуриентов на платное обучение.',
        reply_markup=kb.back1)


@router.callback_query(F.data == 'bonus')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text=start_text2,
                                     reply_markup=kb.back1)


@router.callback_query(F.data == 'Passing_points')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text=start_text2,
                                     reply_markup=kb.back1)


@router.callback_query(F.data == 'Opening_hours')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text='Часы работы приемной комиссии адрес: метро Орехово ул. Шипиловский пр-д дом 37, корп.1\n'
                                          'Часы работы: понедельник-пятница с 09.00 до 20.00, суббота с 10.00 до 18.00\n'
                                          'Общие телефоны приемной комиссии:\n'
                                          '84953900190\n'
                                          'Секретарь приемной комиссии: Железнова Светлана Николаевна тел. 8-916-511-11-03\n'
                                          'В приемной комиссии Вам помогут подать заявление через портал mos.ru на бюджет. Окажут помощь в выборе'
                                          ' специальности. Одновременно подадите заявление на платное обучение.',
                                     reply_markup=kb.back1)


@router.callback_query(F.data == 'Doors')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{start_text2}',
                                     reply_markup=kb.back1)


@router.callback_query(F.data == 'Seven_nation_army')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text='Колледж "Царицыно" предоставляет отсрочку от армии студентам очной формы обучения\n\n'
                                          'C 1 января 2017 года вступает в силу Федеральный закон от 14.10.2014 N 302-ФЗ "О внесении изменений в статью 24 Федерального закона'
                                          ' "О воинской обязанности и военной службе", согласно которому отсрочка от призыва на военную службу для студентов будет предоставляться независимо'
                                          ' от достижения ими определенного возраста при условии, что это первое его образование.\n'
                                          'Абитуриентам, поступающим после 11 класса, которые уже воспользовались правом отсрочки от призыва на военную службу учась в школе,'
                                          ' при поступлении в колледж повторная отсрочка не предоставляется.',
                                     reply_markup=kb.back1)


@router.callback_query(F.data == 'Questions')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(text='Вопрос: \nПрименяются ли льготы при приеме на обучение по ОП СПО на основе результатов освоения поступающими программы основного общего или среднего общего образования?\n'
                                            'Ответ: \nЛьготы вне конкурса: \nквота для детей-инвалидов и лиц ОВЗ, установленные образовательной организацией по согласованию с Советом колледжа,'
                                            ' одно бюджетное место на специальность, отдельно на базе 9 и 11 классов.\n'
                                            '-дети лиц, участвующих в СВО\n'
                                            '- участники СВО\n'
                                            'Льготы-преимущественное право:-сироты, инвалиды 1 и 2 группы, личные достижения (см. перечень на сайте колледжа)\n\n'
                                            'Вопрос: \nСколько стоит платное обучение и какой проходной балл?\n'
                                            'Ответ: \nОчное платное обучение в колледже стоит в год 180 тыс. рублей, оплата осуществляется по двум семестрам (август, январь),'
                                            ' можно использовать материнский капитал. Проходной балл зависит от количества поданных заявлений и выделенных мест.\n\n'
                                            'Вопрос: \nМогу ли я поступить в колледж на бюджетной основе, если я являюсь Гражданином СНГ, Киргизии?\n'
                                            'Ответ: \nПрием иностранных граждан на обучение в образовательные организации осуществляется за счет бюджетных ассигнований федерального бюджета, бюджетов субъектов '
                                            'Российской Федерации или местных бюджетов в соответствии с международными договорами Российской Федерации, федеральными законами или установленной Правительством Российской '
                                            'Федерации квотой на образование иностранных граждан в Российской Федерации, а также по договорам об оказании платных образовательных услуг. '
                                            'К сожалению, квоты на образование за счет бюджетных средств иностранных граждан, в том числе соотечественников,  в учебном году не предусмотрено. '
                                            'Прием в колледж для всех абитуриентов осуществляется на общих основаниях.  В соответствии с Правилами приема в ГБПОУ Колледж «Царицыно» подача и регистрация заявлений на '
                                            'обучение по профессиональным образовательным программам CПО, реализуемым за счет средств бюджета города Москвы может быть произведена при условии обязательной регистрации '
                                            'заявления через Официальный сайт Мэра Москвы mos.ru в период с 20 июня по 15 августа.',
                                     reply_markup=kb.back1)


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
    await callback.message.edit_text(f'{text3}',
                                     reply_markup=kb.SpecialtyKeyboard)
