from datetime import date
import db
from keyboards import generate_calendar_days, \
    generate_calendar_months, EMTPY_FIELD, DAYS
from filters import calendar_factory, calendar_zoom, bind_filters
from telebot import types, TeleBot #Импортируем все необходимое с других файлов

month_name = ['-','Января','Февраля','Марта','Апреля','Мая','Июня','Июля','Августа','Сентября','Октября','Ноября','Декабря']
days_register = []
feedback = []
users = []
main_menu = ['1️⃣Главное','2️⃣Личный кабинет','3️⃣Вызов оператора','4️⃣Часто задаваемые вопросы','5️⃣Оставить отзыв', '6️⃣О создателях']
main_menu_buttons = ['Услуги и цены','Врачи','В начало']
lk_buttons = ['Записаться на прием','Текущие записи','В начало']
doctors = ['Бекреев Валерий Валентинович',
           'Журавлева Марина Александровна',
           'Клюкина Наталья Викторовна',
           'Целинская Анастасия Тимофеевна',
           'Белолипецкая Анастасия Алексеевна',
           'Лисицына Мария Денисовна',
           'Кузнецова Алия',
           'Денисова Екатерина Александровна',
           'Дубровин Константин Владимирович',
           'В начало']
doctors_description = {'Бекреев Валерий Валентинович':'Врач челюстно-лицевой хирургии, специалист по лечению ВНЧС\n\nОпыт работы - 43 года',
                       'Журавлева Марина Александровна':'Врач стоматолог-терапевт\n\nОпыт работы 14 лет',
                       'Клюкина Наталья Викторовна':'Врач стоматолог-терапевт\n\nОпыт работы 6 лет',
                       'Белолипецкая Анастасия Алексеевна':'Стоматолог общей практики, врач стоматолог-ортопед, детский стоматолог\n\nОпыт работы - 5 лет',
                       'Лисицына Мария Денисовна':'Врач стоматлог-ортопед\n\nОпыт работы 3 года',
                       'Кузнецова Алия':'Детский врач-стоматолог\n\nОпыт работы 12 лет',
                       'Денисова Екатерина Александровна':'Врач стоматолог-ортодонт\n\nОпыт работы 5 лет',
                       'Дубровин Константин Владимирович':'Врач стоматолог-хирург, имплантолог\n\nОпыт работы 7 лет'}
#Создаем массив имен кнопок
bot = TeleBot('5303187878:AAF0YYm-d9IhzR6snAeJudIxM2TX33NW1DY') #Добавляем токен бота
@bot.message_handler(commands=['start']) #сообщения от бота в виде приветствия
def begin(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(types.KeyboardButton("Регистрация", request_contact = True))
    send_message = f'Привет, <i><b>{message.from_user.first_name}</b></i>!\n'\
                   f'Мы рады тебя приветствовать в нашем боте <i><b>DentaKlad</b></i>. \n'\
                   f'Для начала работы мы должны внести тебя в нашу базу, этому просто нажми на кнопку <b>Регистрация</b>, после чего у тебя появятся кнопки!\n'\
                   f'Если вдруг панель из кнопок исчезнет, просто нажми на квадратик с 4 точками и оно откроется\n\n'\
                   f'P.S. кнопку <b>Запись</b> не трогай, она в разработке, хотя ради прикола поклацать можешь)'
    bot.send_message(message.chat.id, send_message, parse_mode = 'html', reply_markup = markup)

@bot.message_handler(content_types=['contact'])
def number(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for context in main_menu:
        markup.add(types.KeyboardButton(context))
    send_message = f'Отлично, вы были зарегистрированы! Перед вами открылось главное меню, которым вы можете пользоваться!'
    bot.send_message(message.from_user.id, send_message, parse_mode='html', reply_markup=markup)
    users.append([message.contact.user_id, message.contact.phone_number, message.contact.first_name, message.contact.last_name])
    name = str(message.contact.first_name) + str(message.contact.last_name)
    db.add_row(name, message.contact.phone_number)
    for i in range(len(users)):
        print(f"Пользователь {i + 1}:\n id:{users[i][0]}\n Телефон:{users[i][1]}\n Имя:{users[i][2]}\n Фамилия:{users[i][3]}\n")
    db.all_rows()

@bot.callback_query_handler(func=lambda c: c.data in ['Контакты','Реквизиты компании','Гарантии']) #Выполнение команд на кнопки, прикрепленные к сообщению
def start_programm(callback):
    name = callback.data
    if name == 'Контакты':
        bot.send_location(callback.from_user.id, 55.660327, 37.515121)
        mess = f'📩Наш адрес:\n      г.Москва, м.Калужская,\n      ул.Обручева, дом 11\n' \
               f'❎Работаем без выходных\n      С 8:00 до 22:00\n' \
               f'📱Телефон: \n       +74951201091'
        bot.send_message(callback.from_user.id, mess, parse_mode='html')
    elif name == 'Гарантии':
        send_message = f'Гарантия и прогнозы предстоящего лечения обговариваются лечащим врачом отдельно для каждого случая ' \
                       f'конкретно и указываются в медицинской карте пациента. Все гарантийные обязательства клиники указаны в «Положении о гарантийных обязательствах», ' \
                       f'которые являются обязательным приложением к договору с пациентом, и предоставляются только в случае выполнения пациентом следующих обязательств:' \
                       f'- пациент обязан строго соблюдать назначения и рекомендации врача до начала лечения, во время и после лечения;' \
                       f'- в случае возникновения боли, дискомфорта или других жалоб пациенту в течение 1-3 дней надо обратиться в клинику к любому врачу для диагностики и устранению причин этих расстройств;' \
                       f'- пациент обязан поддерживать на соответствующем уровне гигиену полости рта, уход за ортопедическими, ортодонтическими конструкциями;' \
                       f'- один раз в 6 месяцев (или чаще по назначению врача) пациенту надо посещать своего лечащего врача или любого другого доктора нашей клиники.'
        bot.send_message(callback.from_user.id, f'<i>{send_message}</i>', parse_mode='html')
    elif name == 'Реквизиты компании':
        bot.send_photo(callback.from_user.id, photo='https://sun9-56.userapi.com/s/v1/if2/J2NaeW_sI3fpr9kYZ5HYkkpjyGDpmeTtavK_1r8n7j9NgGHRBCKupqRYxks-w-bOovrePiAHOJWC63eLja6k32-3.jpg?size=1274x818&quality=96&type=album',caption='Прикрепляем реквизиты:')

@bot.message_handler(content_types=['text']) #Блок, отвечающий за действия всех кнопок на панели
def all_message(message):
    if message.text == main_menu_buttons[2]:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for context in main_menu:
            markup.add(types.KeyboardButton(context))
        send_message = f'Вы открыли начальное меню'
        bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

    elif message.text == main_menu[0]:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for context in main_menu_buttons:
            markup.add(types.KeyboardButton(context))
        markup1 = types.InlineKeyboardMarkup()
        markup1.add(types.InlineKeyboardButton("Контакты", callback_data='Контакты'))
        markup1.add(types.InlineKeyboardButton("Реквизиты компании", callback_data='Реквизиты компании'))
        markup1.add(types.InlineKeyboardButton("Гарантии", callback_data='Гарантии'))
        mess = f'<b>Вы зашли в главное🌐</b>\n\n'\
               f'<i>Вы можете выбрать интересующие вас кнопки на панели\nЕсли вы хотите получить </i>'\
               f'<i>информацию о нашей клинике, нажмите кнопки ниже и перед вами высветится окошко с описанием</i>'
        bot.send_message(message.chat.id, '...Загрузка...', parse_mode='html', reply_markup = markup)
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup = markup1)

    elif message.text == main_menu[1]:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for context in lk_buttons:
            markup.add(types.KeyboardButton(context))
        bot.send_message(message.chat.id, 'Вы открыли свой личный кабинет🏠', parse_mode='html', reply_markup = markup)

    elif message.text == main_menu[3]:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Смотреть", url="https://dentaklad.ru/paczientam/"))
        mess = f'Нажав кнопку <b><i>Смотреть</i></b>, вы сможете перейти на наш сайт и посмотреть часто задаваемые вопросы'
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    elif message.text == main_menu[4]:
        mess = bot.send_message(message.chat.id, '<b>Пожалуйста, напишите ваш отзыв о нашей клинике!</b>', parse_mode='html')
        bot.register_next_step_handler(mess, answer)

    elif message.text == main_menu[5]:
        send_message = f'Данный бот был разработан командой из ВШЭ как проект по программированию'
        bot.send_message(message.chat.id, send_message, parse_mode='html')

    elif message.text == main_menu_buttons[0]:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Смотреть", url="https://dentaklad.ru/czeny/"))
        mess = f'Нажав кнопку <b><i>Смотреть</i></b>, вы сможете перейти на наш сайт и увидеть цены'
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

    elif message.text == main_menu_buttons[1]:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for context in doctors:
            markup.add(types.KeyboardButton(context))
        mess = f'<b>👩🏼‍⚕️‍Только опытные врачи</b>\n<i>Стаж работы от 4 до 45 лет</i>\n\n'\
               f'<b>🖥На пике технологий</b>\n<i>Регулярно повышают квалификацию</i>\n\n' \
               f'<b>👍🏻98% клиентов рекомендуют нас знакомым</b>\n<i>Регулярно повышают квалификацию</i>\n\n' \
               f'Выберите работника из списка для просмотра информации'
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

    elif message.text in doctors and message.text != doctors[-1]:
        send_message = f'<b>{message.text}</b>\n\n<i>{doctors_description[message.text]}</i>'
        bot.send_message(message.chat.id, send_message, parse_mode='html')

    elif message.text == lk_buttons[0]:
        now = date.today()
        bot.send_message(message.chat.id, '<b>Выберите день, в который вы бы хотели записаться к нам📅</b>', parse_mode='html', reply_markup=generate_calendar_days(year=now.year, month=now.month))

    elif message.text == lk_buttons[1]:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        register = f'{days_register[0][2]} {month_name[int(days_register[0][1])]} {days_register[0][0]}'
        markup.add(types.KeyboardButton(register))
        markup.add(types.KeyboardButton(lk_buttons[2]))
        send_message = f'Ваши записи доступны на панеле кнопок'
        bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

    else:
        send_message = f'К сожалению, я не отвечаю на сообщения, я не умею разговаривать('
        bot.send_message(message.chat.id, send_message, parse_mode='html')

def answer(message): #Ответ на отзыв
    feedback.append(message.text)
    phone_number = 0
    try:
        for i in users:
            if i[0] == message.from_user.id:
                phone_number = i[1]
    except Exception as ex:
        print(ex)
    db.add_comment(message.text, phone_number)
    bot.send_message(message.chat.id, 'Спасибо за ваш отзыв!')

@bot.callback_query_handler(func=None, calendar_config=calendar_factory.filter()) #Генерация клавиатуры из кнопок при перемотке нового месяца
def calendar_action_handler(call: types.CallbackQuery):
    callback_data: dict = calendar_factory.parse(callback_data=call.data)
    year, month = int(callback_data['year']), int(callback_data['month'])
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
                                  reply_markup=generate_calendar_days(year=year, month=month))

@bot.callback_query_handler(func=None, calendar_zoom_config=calendar_zoom.filter()) #Выдача сообщений при нажатии кнопок на календаре, а также запись на дату
def calendar_zoom_out_handler(call: types.CallbackQuery):
    callback_data: dict = calendar_zoom.parse(callback_data=call.data)
    year = int(callback_data.get('year'))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=generate_calendar_months(year=year))
    yr, mth, dy = days_register[0][0], days_register[0][1], days_register[0][2]
    chosen_date = f'{yr}/{mth}/{dy}'
    if date(int(yr),int(mth),int(dy)) >= date.today():
        bot.answer_callback_query(call.id, f'Вы записались на {chosen_date}🕐', show_alert=True)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if date(int(yr),int(mth),int(dy)) < date.today():
        mess = f'<b>Извините, но выбранная дата уже прошла по календарю. Запишитесь еще раз</b>'
    else:
        mess = f'<b>{call.from_user.first_name}</b>, вы записались на прием на\n\n <i><b>{days_register[0][2]} {month_name[int(days_register[0][1])]} {days_register[0][0]} года</b></i>🕐\n\n'\
           f'<i>Запись отобразится у вас в личном кабинете. Если вы хотите поменять дату записи, просто еще раз запишитесь и она автоматически сменится на другую</i>'
    bot.send_message(call.message.chat.id, mess, parse_mode='html')


@bot.callback_query_handler(func=lambda call: (call.data.split('-'))[2] in DAYS) #Выбор даты записи
def callback_empty_field_handler(call: types.CallbackQuery):
    chosen_data = (call.data.split('-'))[2]
    bot.answer_callback_query(call.id, f' Вы выбрали {chosen_data} число. Нажмите кнопку Записаться')
    days_register.clear()
    days_register.append(call.data.split('-'))

if __name__ == '__main__':
    bind_filters(bot)
    bot.infinity_polling()
