import locale
locale.setlocale(locale.LC_ALL, ('RU','UTF8')) #Специальная штука, чтобы можно было переводить с помошью Datetime месяцы на русском

import calendar
from datetime import date, timedelta

from filters import calendar_factory, calendar_zoom
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

EMTPY_FIELD = '1'
DAYS = [str(i) for i in range(1,32)] #создаем дни в месяце
WEEK_DAYS = ['Пн','Вт','Ср','Чт','Пт','Сб','Вс'] #создаем дни недели
MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)] #создаем номера месяцев


def generate_calendar_days(year: int, month: int): #генерим сам календарь в текущем месяце
    keyboard = InlineKeyboardMarkup(row_width=7)
    today = date.today()

    keyboard.add(
        InlineKeyboardButton(
            text=date(year=year, month=month, day=1).strftime('%b %Y'),
            callback_data=EMTPY_FIELD
        )
    )
    keyboard.add(*[
        InlineKeyboardButton(
            text=day,
            callback_data=EMTPY_FIELD
        )
        for day in WEEK_DAYS
    ])

    for week in calendar.Calendar().monthdayscalendar(year=year, month=month):
        week_buttons = []
        for day in week:
            day_name = ' '
            if day == today.day and today.year == year and today.month == month:
                day_name = '⚪️'
            elif day != 0:
                day_name = str(day)
            if day == 0:
                week_buttons.append(InlineKeyboardButton(text=day_name, callback_data=EMTPY_FIELD))
            else:
                week_buttons.append(
                    InlineKeyboardButton(
                        text=day_name, callback_data=str(date(year=year, month=month, day=day))
                    )
                )
        keyboard.add(*week_buttons)

    previous_date = date(year=year, month=month, day=1) - timedelta(days=1)
    next_date = date(year=year, month=month, day=1) + timedelta(days=31)

    keyboard.add(
        InlineKeyboardButton(
            text='<',
            callback_data=calendar_factory.new(year=previous_date.year, month=previous_date.month)
        ),
        InlineKeyboardButton(
            text='Записаться',
            callback_data=calendar_zoom.new(year=year)
        ),
        InlineKeyboardButton(
            text='>',
            callback_data=calendar_factory.new(year=next_date.year, month=next_date.month)
        ),
    )

    return keyboard


def generate_calendar_months(year: int):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton(
            text=date(year=year, month=1, day=1).strftime('Year %Y'),
            callback_data=EMTPY_FIELD
        )
    )
    keyboard.add(*[
        InlineKeyboardButton(
            text=month,
            callback_data=calendar_factory.new(year=year, month=month_number)
        )
        for month_number, month in MONTHS
    ])
    keyboard.add(
        InlineKeyboardButton(
            text='<',
            callback_data=calendar_zoom.new(year=year - 1)
        ),
        InlineKeyboardButton(
            text='>',
            callback_data=calendar_zoom.new(year=year + 1)
        )
    )
    return