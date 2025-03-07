from run import logger as logging
from run import bot
from run import database as db

from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InputMediaDocument, FSInputFile

import app.keyboards as kb

import app.admin_keyboards as akb

import app.sadmin_keyboards as sakb

user_router = Router()

VERSION = '0.1.2b'
DEVELOPERS = ['@npokhodnya', '@Volosatiyyy']


class Form(StatesGroup):
    start_broadcast = State()


start_text2 = 'Сейчас идут тех работы, функция недоступна :('
start_text = (', здаствуйте. Этот бот поможет вам с поступлением в один из лучших колледжей Москвы. Ниже вы можете '
              'выбрать интересующие вас детали.')
text3 = ('Специальности Колледжа "Царицыно"\nКолледж имеет 3 отделения:\n1)Генерала Белова 6 (Отделение управления и '
         'информационных технологий ОУИТ)\n2)Генерала Белова 4 (Политехническое отделение ОП)\n3)Шипиловский проезд '
         '37 (Отделение гостиничного и ресторанного бизнеса ОГРБ)')
doc_text = "Сейчас идут тех работы, функция недоступна :("
army_text = "Сейчас идут тех работы, функция недоступна :("
schedule_text = "Сейчас идут тех работы, функция недоступна :("
points_text = 'На данный момент данные о проходных баллах не доступны. Информация о проходных баллах будет обновляться.'


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    us_id = message.from_user.id
    await db.add_user(us_id, message.from_user.username)
    if await db.is_super_admin(us_id):
        await message.answer(f'{message.from_user.first_name}{start_text}',
                             reply_markup=sakb.sadmin_keyboard1)
    elif await db.is_admin(message.from_user.id):
        await message.answer(f'{message.from_user.first_name}{start_text}',
                             reply_markup=akb.admin_keyboard1)
    else:
        await message.answer(f'{message.from_user.first_name}{start_text}',
                             reply_markup=kb.keyboard_page1)


@user_router.message(Command('about'))
async def cmd_about(message: Message):
    await message.answer(f"-- version: {VERSION}\n-- developers: {', '.join(DEVELOPERS)}")


@user_router.callback_query(F.data == 'sttngs1')
async def page2(callback: CallbackQuery):
    if await db.is_super_admin(callback.from_user.id):
        await callback.message.edit_text(f'{callback.from_user.first_name}{start_text}',
                                         reply_markup=sakb.sadmin_keyboard2)

    elif await db.is_admin(callback.from_user.id):
        await callback.message.edit_text(text=f'{callback.from_user.first_name}{start_text}',
                                         reply_markup=akb.admin_keyboard2)
    else:
        await callback.message.edit_text(text=f'{callback.from_user.first_name}{start_text}',
                                         reply_markup=kb.keyboard_page1)


@user_router.callback_query(F.data == 'sttngs2')
async def page2(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{callback.from_user.first_name}{start_text}',
                                     reply_markup=kb.keyboard_page2)


@user_router.callback_query(F.data == 'sttngs3')
async def page3(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{callback.from_user.first_name}{start_text}',
                                     reply_markup=kb.keyboard_page3)


@user_router.callback_query(F.data == 'How')
async def how_to_enroll(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Чтобы поступить в колледж на бюджет, нужно подать документы в приемную комиссию. Делается это на '
             'портале мос.ру, на котором вы уже должны быть зарегистрированы (если же у вас там нет аккаунта, '
             'то сначала вам нужно зарегистрироваться). Заявления принимаются с 20 июня по 15 августа. Для '
             'поступления на платное обучение необходимо приходить в приёмную комиссию.',
        reply_markup=kb.How1)


@user_router.callback_query(F.data == 'back2')
async def how_to_enroll(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Чтобы поступить в колледж на бюджет, нужно подать документы в приемную комиссию. Делается это на '
             'портале мос.ру, на котором вы уже должны быть зарегистрированы (если же у вас там нет аккаунта, '
             'то сначала вам нужно зарегистрироваться). Заявления принимаются с 20 июня по 15 августа. Для '
             'поступления на платное обучение необходимо приходить в приёмную комиссию.',
        reply_markup=kb.How1)


@user_router.callback_query(F.data == 'back3')
async def back_to_specialty(callback: CallbackQuery):
    sent_message = await callback.message.answer(text=f'{text3}',
                                                 reply_markup=kb.SpecialtyKeyboard)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=str(sent_message.message_id - 1))


@user_router.callback_query(F.data == 'back_del')
async def back_to_page1(callback: CallbackQuery):
    us_id = callback.from_user.id
    if await db.is_super_admin(us_id):
        sent_message = await callback.message.answer(f'{callback.from_user.first_name}{start_text}',
                             reply_markup=sakb.sadmin_keyboard1)
    elif await db.is_admin(us_id):
        sent_message = await callback.answer(f'{callback.from_user.first_name}{start_text}',
                             reply_markup=akb.admin_keyboard1)
    else:
        sent_message = await callback.answer(f'{callback.from_user.first_name}{start_text}',
                             reply_markup=kb.keyboard_page1)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=str(sent_message.message_id - 1))


@user_router.callback_query(F.data == 'doсs')
async def documents(callback: CallbackQuery):
    await callback.message.edit_text(
        text=doc_text,
        reply_markup=kb.back2)


@user_router.callback_query(F.data == 'cook')
async def cook_info(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaDocument(media='https://collegetsaritsyno.mskobr.ru/attach_files/i-konditerskoe-delo.pdf'),
        reply_markup=kb.back3)
    await callback.message.edit_caption(
        caption='Данные о направлении "Поварское и кондитерское дело"',
        reply_markup=kb.back3)


@user_router.callback_query(F.data == 'tourism')
async def tourism_info(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaDocument(media='https://collegetsaritsyno.mskobr.ru/attach_files/delo.pdf'),
        reply_markup=kb.back3)
    await callback.message.edit_caption(
        caption='Данные о направлении "Туризм и гостеприимство"',
        reply_markup=kb.back3)


@user_router.callback_query(F.data == 'transport')
async def transport_info(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaDocument(
            media='https://collegetsaritsyno.mskobr.ru/attach_files/22-servis-na-transporte-po-vidam-transporta.pdf'),
        reply_markup=kb.back3)
    await callback.message.edit_caption(
        caption='Данные о направлении "Сервис на транспорте"',
        reply_markup=kb.back3)


@user_router.callback_query(F.data == 'inf')
async def inf_info(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaDocument(
            media='https://tk21.mskobr.ru/files/2022-2023/informaczionnye-sistemy-i-programmirovanie-1.pdf'),
        reply_markup=kb.back3)
    await callback.message.edit_caption(
        caption='По специальности 09.02.07 Информационные системы и программирование прием осуществляется по '
                'направлениям:\n   -программист (бюджет и платное обучение) (адрес обучения: ул. Шипиловский пр-д, дом 37, '
                'корп.1; ул. Генерала Белова дом 6)\n   -разработчик ВЭБ и мультимедийных приложений (бюджет и платное '
                'обучение) (адрес обучения: ул. Генерала Белова дом 6)\n   -специалист по информационным системам ('
                'бюджетное обучение) (адрес обучения: ул. Генерала Белова дом 4)',
        reply_markup=kb.back3)



@user_router.callback_query(F.data == 'comp_comp')
async def sysadm_info(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaDocument(
            media='https://collegetsaritsyno.mskobr.ru/attach_files/sistemyi-i-kompleksyi.pdf'),
        reply_markup=kb.back3)
    await callback.message.edit_caption(
        caption='Данные о направлении "Компьютерные системы и комплексы"',
        reply_markup=kb.back3)


@user_router.callback_query(F.data == 'Stages_of_enrollment')
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



@user_router.callback_query(F.data == 'benefits')
async def invalids(callback: CallbackQuery):
    await callback.message.edit_text(text='Колледж предоставляет квоты абитуриентам с ограниченными возможностями на '
                                          'бесплатное очное обучение.\n Для того, чтобы поступить по данной квоте, вы '
                                          'должны предоставить в приемную комиссию соответствующий документ (заключение '
                                          'учреждения медико-социальной экспертизы и (или) справку об установлении инвалидности) '
                                          'с заключением от врача об отсутствии противопоказаний для обучения в ГБПОУ '
                                          'Колледж «Царицыно» по выбранной специальности.\nЕсли численность абитуриентов '
                                          'превышает количество квот, то прем в колледж осуществляется по баллам аттестата.',
                                     reply_markup=kb.benefits_Keyboard)


@user_router.callback_query(F.data == 'back_to_benefits')
async def invalids(callback: CallbackQuery):
    await callback.message.edit_text(text='Колледж предоставляет квоты абитуриентам с ограниченными возможностями на '
                                          'бесплатное очное обучение.\n Для того, чтобы поступить по данной квоте, вы '
                                          'должны предоставить в приемную комиссию соответствующий документ (заключение '
                                          'учреждения медико-социальной экспертизы и (или) справку об установлении инвалидности) '
                                          'с заключением от врача об отсутствии противопоказаний для обучения в ГБПОУ '
                                          'Колледж «Царицыно» по выбранной специальности.\nЕсли численность абитуриентов '
                                          'превышает количество квот, то прем в колледж осуществляется по баллам аттестата.',
                                     reply_markup=kb.benefits_Keyboard)


@user_router.callback_query(F.data == 'ovz')
async def invalids(callback: CallbackQuery):
    await callback.message.edit_text(text='Имеют право на получение:\n'
                                          '   - социальной стипендии (928 руб)\n'
                                          '   - дополнительного горячего питания\n'
                                          '   - приоритетное право на получение бесплатных билетов для посещения театров и музеев города Москвы '
                                          '(в рамках реализации Постановления Правительства города Москвы № 516-ПП от 30.06.1998 года.'
                                          '«Об организации бесплатного посещения учреждений культуры Москвы учащимися образовательных учреждений, приютов,'
                                          ' реабилитационных центров, центов социальной помощи семьи и детям»).\n\n'
                                          'Для получения социальной стипендии необходимо:\n'
                                          '   - предоставить социальному педагогу справку, подтверждающую инвалидность из медико-социальной экспертизы '
                                          '(категории: «ребенок-инвалид», инвалид I и II группы, инвалид III группы – инвалидность с детства)\n'
                                          '   - обратиться к социальному педагогу отделения для написания Заявления.',
                                     reply_markup=kb.back_to_benefits)


@user_router.callback_query(F.data == 'orphans')
async def invalids(callback: CallbackQuery):
    await callback.message.edit_text(text='Имеют право на получение:'
                                          '\n   - социальной стипендии (928 руб.)'
                                          '\n   - ежегодное пособие на приобретение учебной литературы и письменных принадлежностей  (1704 руб.)'
                                          '\n   - дополнительного горячего питания'
                                          '\n   - выплата денежных средств на содержание (с 18 лет) (12 000 руб.)'
                                          '\n   - приоритетное право на получение бесплатных билетов для посещения театров и музеев города Москвы '
                                          '(в рамках реализации Постановления Правительства города Москвы № 516-ПП от 30.06.1998 года. «Об организации бесплатного посещения '
                                          'учреждений культуры Москвы учащимися образовательных учреждений, приютов, реабилитационных центров, центов социальной помощи семьи и детям».).'
                                          '\n   - единовременной компенсационной выплаты по окончанию ГБПОУ Колледж «Царицыно»: *При дальнейшем трудоустройстве (при предоставлении справки с места работы 79,416 рублей. )'
                                          '\n   *При дальнейшем поступлении на очное дневное отделение (при предоставлении справки с места учёбы 20,639 рублей)'
                                          '\n   Для получения социальной стипендии необходимо:'
                                          '\n   - предоставить документы, подтверждающие статус ребенка-сироты, ребенка оставшегося без попечения родителей или лиц из категории вышеперечисленных. '
                                          '(справка из органов опеки или органов социальной защиты, постановление суда о лишении родительских прав и установлении опеки, свидетельство о смерти и пр.)'
                                          '\n   - обратиться к социальному педагогу отделения для написания Заявления.',
                                     reply_markup=kb.back_to_benefits)


@user_router.callback_query(F.data == 'social_support')
async def invalids(callback: CallbackQuery):
    await callback.message.edit_text(text='Имеют право на получение:'
                                          '\n   - социальной стипендии (928 руб)'
                                          '\n   - дополнительного горячего питания'
                                          '\n   - приоритетное право на получение бесплатных билетов для посещения театров и музеев города Москвы (в рамках реализации Постановления Правительства города Москвы'
                                          ' № 516-ПП от 30.06.1998 года. «Об организации бесплатного посещения учреждений культуры Москвы учащимися образовательных учреждений, приютов, реабилитационных центров,'
                                          ' центров социальной помощи семьи и детям».).'
                                          '\n\nДля получения социальной стипендии необходимо:'
                                          '\nПодать онлайн-заявление на получение справки о назначении государственной социальной помощи в городе Москве на портале mos.ru (Ссылка для заказа справок о назначении государственной социальной помощи)'
                                          '\nСрок рассмотрения электронного заявления составляет не более 7 рабочих дней. Услуга предоставляется зарегистрированным пользователям с указанным СНИЛС в личном кабинете.'
                                          '\nПосле получения онлайн уведомления о ПОЛОЖИТЕЛЬНОМ решении о предоставлении государственной функции обратиться к социальному педагогу отделения для написания Заявления.'
                                          ' (Не ранее 2-х календарных дней с момента получения уведомления).',
                                     reply_markup=kb.back_to_benefits)


@user_router.callback_query(F.data == 'Passing_points')
async def passing_points(callback: CallbackQuery):
    await callback.message.edit_text(
        text=points_text,
        reply_markup=kb.back1)



@user_router.callback_query(F.data == 'Opening_hours')
async def opening_hours(callback: CallbackQuery):
    await callback.message.edit_text(
        text=schedule_text,
        reply_markup=kb.back1)


@user_router.callback_query(F.data == 'Doors')
async def open_doors_info(callback: CallbackQuery):
    await callback.message.edit_text(
        text='На данный момент для того чтобы узнать информацию о ближайших днях открытых дверей требуется перейти на сайт Колледжа Царицыно.',
        reply_markup=kb.Doors_Keyboard)


@user_router.callback_query(F.data == 'Seven_nation_army')
async def army(callback: CallbackQuery):
    await callback.message.edit_text(
        text=army_text,
        reply_markup=kb.back1)


@user_router.callback_query(F.data == 'Questions')
async def questions(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaDocument(
            media=FSInputFile("Files_for_amigo/Часто задаваемые вопросы.pdf", "Часто задаваемые вопросы.pdf"),
            reply_markup=kb.keyboard_page1))
    await callback.message.edit_caption(caption=f"Часто задаваемые вопросы", reply_markup=kb.back_del)


@user_router.message(F.text == 'пон')
async def get_help(message: Message):
    await message.reply('¯\_(ツ)_/¯')


@user_router.callback_query(F.data == 'more')
async def more(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaDocument(media="https://collegetsaritsyno.mskobr.ru/files/2023/испр.4.5.6.Специальности.pdf",
                                 reply_markup=kb.keyboard_page1))
    await callback.message.edit_caption(caption=f"Цифры приема по специальностям", reply_markup=kb.back_del)


@user_router.callback_query(F.data == 'back1')
async def back_to_page1(callback: CallbackQuery):
    if await db.is_super_admin(callback.from_user.id):
        await callback.message.edit_text(f'{callback.from_user.first_name}{start_text}',
                                         reply_markup=sakb.sadmin_keyboard1)

    elif await db.is_admin(callback.from_user.id):
        await callback.message.edit_text(f'{callback.from_user.first_name}{start_text}',
                                         reply_markup=akb.admin_keyboard1)

    else:
        await callback.message.edit_text(f'{callback.from_user.first_name}{start_text}',
                                         reply_markup=kb.keyboard_page1)


@user_router.callback_query(F.data == 'Specialty')
async def more(callback: CallbackQuery):
    await callback.message.edit_text(f'{text3}',
                                     reply_markup=kb.SpecialtyKeyboard)


@user_router.message(Command('id'))
async def get_id(msg: Message):
    await msg.answer(str(msg.from_user.id))


@user_router.message(Command('role'))
async def get_role(msg: Message):
    if msg.text.strip() == '/role':
        await msg.answer(str(await db.get_role_by_id(msg.from_user.id)))
    elif len(msg.text.split()) == 2:
        if await db.is_admin(msg.from_user.id):
            try:
                tg_id = int(msg.text.split()[1])
                role = await db.get_role_by_id(msg.from_user.id)
                if role is not None:
                    await msg.answer(str(await db.get_role_by_id(msg.from_user.id)))
                    logging.info(f"User {msg.from_user.id} with role {await db.get_role_by_id(msg.from_user.id)} check role of user {tg_id}")
                else:
                    await msg.answer("There is no user with that id")
                    logging.info(
                        f"User {msg.from_user.id} with role {await db.get_role_by_id(msg.from_user.id)} try check role of user {tg_id}, but there is no user with that id in database")
            except ValueError:
                await msg.answer("Invalid value for tg_id")
                logging.info(
                    f"User {msg.from_user.id} with role {await db.get_role_by_id(msg.from_user.id)} try check role of user, but there is invalid argument id")
        else:
            await msg.answer("Invalid usage of /role command")
            logging.warning(f"User {msg.from_user.id} with role {await db.get_role_by_id(msg.from_user.id)} try check role of another user, whithout admin rights")
    else:
        await msg.answer("Invalid usage of /role command")




