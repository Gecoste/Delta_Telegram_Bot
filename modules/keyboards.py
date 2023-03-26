from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#[Главное меню] =================================================================
def start_button_class():
    start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    search = types.KeyboardButton(text='Поиск информации', callback_data='search')
    support = types.KeyboardButton(text='🎧 Техническая поддержка')
    profile = types.KeyboardButton(text='📰 Профиль')
    faq = types.KeyboardButton(text='📔 F.A.Q проекта')
    helps = types.KeyboardButton(text='🔗 Помощь')
    start.add(search, profile,faq, helps, support)
    return start
    
#[Калькулятор] =================================================================
def calc_button_class():
    calculator = types.InlineKeyboardMarkup(row_width=4)
    null_button = types.InlineKeyboardButton(' ', callback_data='no')
    percent_button = types.InlineKeyboardButton('%', callback_data='%')
    clear_button = types.InlineKeyboardButton('C', callback_data='clear')
    return_button = types.InlineKeyboardButton('<=', callback_data='cancel') 
    tg_button = types.InlineKeyboardButton('tg(x)', callback_data='tgs')
    sn_button = types.InlineKeyboardButton('sin(x)', callback_data='sns')
    cos_button = types.InlineKeyboardButton('cos(x)', callback_data='coss')
    del_button = types.InlineKeyboardButton('/', callback_data='/')
    mn_button = types.InlineKeyboardButton('*', callback_data='*')
    min_button = types.InlineKeyboardButton('-', callback_data='-')
    plus_button = types.InlineKeyboardButton('+', callback_data='+')
    step_button = types.InlineKeyboardButton('х²', callback_data='step')
    korn_button = types.InlineKeyboardButton('√x', callback_data='korn')
    seven_button = types.InlineKeyboardButton('7', callback_data='7')
    eight_button = types.InlineKeyboardButton('8', callback_data='8')
    nine_button = types.InlineKeyboardButton('9', callback_data='9')
    four_button = types.InlineKeyboardButton('4', callback_data='4')
    five_button = types.InlineKeyboardButton('5', callback_data='5')
    six_button = types.InlineKeyboardButton('6', callback_data='6')
    one_button = types.InlineKeyboardButton('1', callback_data='1')
    two_button = types.InlineKeyboardButton('2', callback_data='2')
    three_button = types.InlineKeyboardButton('3', callback_data='3')
    zero_button = types.InlineKeyboardButton('0', callback_data='0')
    result_button = types.InlineKeyboardButton('=', callback_data='=')
    calculator.add(null_button, percent_button, clear_button, return_button)
    calculator.add(sn_button,cos_button, tg_button, step_button)
    calculator.add(plus_button, min_button, mn_button, del_button)
    calculator.add(korn_button)
    calculator.add(six_button, seven_button, eight_button, nine_button)
    calculator.add(two_button, three_button, four_button, five_button)
    calculator.add(null_button, zero_button, one_button, result_button)
    return calculator

#[Техническая поддержка] =================================================================

def support():
    support = types.InlineKeyboardMarkup(row_width=2)
    cancel = types.InlineKeyboardButton('Отмена', callback_data='techcancel')
    sugidea = types.InlineKeyboardButton('Предложить идею', callback_data='sugidea')
    wrerror = types.InlineKeyboardButton('Написать об ошибке', callback_data='wrerror')
    support.add(sugidea, wrerror, cancel)
    return support

#[Переводы, языки для переводов текста] =================================================================

def button_languages():
    lang = types.InlineKeyboardMarkup(row_width=2)
    russian_lang = types.InlineKeyboardButton('Русский', callback_data='ru')
    english_lang = types.InlineKeyboardButton('Английский', callback_data='en')
    lang.add(russian_lang, english_lang)
    return lang