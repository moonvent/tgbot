import requests
import telebot
import sys
from urllib import request
import pprint
import datetime
import time
import show
import os
from telebot import types
from pyaspeller import YandexSpeller


TOKEN = '889368628:AAHK1YT19iUnNjHKxQLk2brI7Azc3RDk-CU'
bot = telebot.TeleBot(TOKEN)
adminid = 704369002
lshelp = ['help',
          'command',
          'помощь',
          'команды',
          ]
lsabout = ['about',
           'о',
           'о разработчике',
           ]


@bot.message_handler(commands=lshelp)
def kek(message):
    if message.text.find('/help фильм') != -1:
        bot.send_message(message.from_user.id, 'Для удачного поиска нужного фильма\n'
                                               'вводите название фильма :\n'
                                               'а) с большой буквы;\n'
                                               'б) на английском;\n'
                                               'в) без нумерации серии / тайтла;\n')
        return
    elif message.text.find('/help игры') != -1:
        bot.send_message(message.from_user.id, 'Для удачного поиска нужной игры\n'
                                               'вводите название игры :\n'
                                               'а) с большой буквы;\n'
                                               'б) на английском;\n'
                                               'в) название части;\n'
                                               'г) название пака(deluxe edition);\n')
        return
    text = """ Доступные команды :>
    /about - о разработчике;
    /help фильм - помощь в поиске фильма;
    время - показывает время;
    курс евро / доллара / гривны - показывает курс евро / доллара / гривны  к рублю;
    где я - показывает ваше местоположение на карте;
    погода завтра / сегодня - погода на завтра / сегодня в Донецке;
    деньги - счета на вебкошелях;
    проверка текста - исправление ошибок в введенном тексте;
    скачать фильм / - скачать фильм /"""

    if message.from_user.id == adminid:
        text += """
        интернет - лиц. счет и тек. баланс;
        газ - проверка счета газа"""

    bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=lsabout)
def url(message):
    bot.send_photo(message.from_user.id, 'https://pp.userapi.com/c846219/v846219134/cba35/puXnXwYcw7Y.jpg')
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='ВК', url='https://vk.com/antipupsik')
    markup.add(btn_my_site)
    btn_my_site = types.InlineKeyboardButton(text='Телега', url='https://t.me/OnionBerserker')
    markup.add(btn_my_site)
    bot.send_message(message.from_user.id, ' ФИО - Куркурин Никита Леонидович;'
                                      '\nКонтактные данные - \n', reply_markup=markup)


#   МЕСТОПОЛОЖЕНИЕ
def buttonloc():    # фиксированная кнопка, появляющаяся внизу экрана
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text="Узнать свое местоположение",  request_location=True)
    markup.add(btn1)
    return markup


#   ПРОВЕРКА ТЕКСТА
def checkgraf(message):
    msg = bot.send_message(message.from_user.id, 'Введите текст :> ')
    bot.register_next_step_handler(msg, corrgraf)


def corrgraf(message):
    _text = message.text
    speller = YandexSpeller()
    try:
        changes = {change['word']: change['s'][0] for change in speller.spell(_text)}
        for word, suggestion in changes.items():
            _text = _text.replace(word, suggestion)
    except IndexError:
        bot.send_message(message.from_user.id, 'Определенного слова нет в словаре')
    else:
        bot.send_message(message.from_user.id, 'Проверенный текст :> \n' + _text)


# ДЛЯ ФИЛЬМОВ
def checkfilm(message):
    msg = bot.send_message(message.from_user.id, 'Введите название фильма > ')
    bot.register_next_step_handler(msg, mainfilm)


def mainfilm(message):
    markup = types.InlineKeyboardMarkup()
    _text = message.text
    print(_text)
    dict_of_films = show.kino(_text)
    if len(dict_of_films) < 1:
        bot.send_message(message.from_user.id, 'Введенного фильма не было найдено на сайте,\n'
                                               'читайте справку - /help фильм\n')
    else:
        for ls in dict_of_films.items():
            tempurl = str(ls[1])
            if sys.getsizeof(tempurl) > 100:
                tempurl = tempurl[:50]
            markup.add(types.InlineKeyboardButton(text=ls[0], callback_data=tempurl))
        bot.send_message(message.from_user.id, 'Выберите какой фильм вам угоден > ', reply_markup=markup)


def checkgame(message):
    msg = bot.send_message(message.from_user.id, 'Введите название игры > ')
    bot.register_next_step_handler(msg, maingame)


def maingame(message):
    markup = types.InlineKeyboardMarkup()
    _text = message.text
    print(_text)
    dict_of_games = show.game(_text)
    if len(dict_of_games) < 1:
        bot.send_message(message.from_user.id, 'Введенной игры не было найдено на сайте,\n'
                                               'читайте справку - /help игры\n')
    else:
        for ls in dict_of_games.items():
            tempurl = str(ls[1])
            if sys.getsizeof(tempurl) > 100:
                tempurl = tempurl[:50]
            markup.add(types.InlineKeyboardButton(text=ls[0], callback_data=tempurl))
        bot.send_message(message.from_user.id, 'Выберите какая игра вам угодна > ', reply_markup=markup)


@bot.callback_query_handler(func=lambda message: True)
def callback_for_buttons(object_):
    namefile = 'Нажми_на_меня.torrent'
    chat_id = object_.from_user.id
    print(object_.data)
    if object_.data.find('/torrents/') != -1:  # скачивание фильмов
        # request.urlretrieve(object_.data, namefile)
        with open(namefile, 'wb') as f:
            f.write(requests.get(object_.data).content)
        with open(namefile, 'rb') as f:
            bot.send_document(chat_id, f)
        os.remove(namefile)
    elif object_.data.find('/kinoframe.') != -1:
        markup = types.InlineKeyboardMarkup()
        dict_of_quality = show.choice_quality(object_.data)
        for i in dict_of_quality.items():
            markup.add(types.InlineKeyboardButton(text=i[0], callback_data=i[1]))
        print('Качество фильма:')
        bot.send_message(chat_id, 'Выберите качество фильма :', reply_markup=markup)
    elif object_.data.find('gmt-max.net') != -1:
        msg = bot.forward_message(chat_id, chat_id, object_.message.message_id - 1)
        title = msg.text
        bot.delete_message(chat_id, msg.message_id)
        dict_of_games = show.game(title)
        for i in dict_of_games.values():
            if i.find(object_.data) != -1:
                request.urlretrieve(show.download_game(i), namefile)
                with open(namefile, 'rb') as f:
                    bot.send_document(chat_id, f)
                os.remove(namefile)
                break


@bot.message_handler(content_types=["text"])
def test(message):
    text = message.text.lower()
    userid = message.from_user.id
    if text.find('курс') != -1:
        if text.find('доллара') != -1:
            bot.send_message(userid, '$$$ Курс доллара к рублю - 1 : ' + show.kurs('Доллар'))
        elif text.find('евро') != -1:
            bot.send_message(userid, '€€€ Курс евро к рублю - 1 : ' + show.kurs('Евро'))
        elif text.find('гривны') != -1:
            bot.send_message(userid, '₴₴₴ Курс гривны к рублю - 1 : ' + show.kursgrn())
    if text.find('погода') != -1:
        if text.find('сегодня') != -1:
            bot.send_message(userid, show.gismeteo('<div class="tab  tooltip" data-text="'))
            bot.send_message(userid, show.mailru('day1'))
        if text.find('завтра') != -1:
            bot.send_message(userid, show.gismeteo('r-donetsk-5080/tomorrow/" data-text="'))
            bot.send_message(userid,  show.mailru('day2'))
    elif text.find('время') != -1:
        bot.send_message(userid, show.timeotime())
    elif text.find('где я') != -1:
        bot.send_message(userid, 'Ваши координаты :> ', reply_markup=buttonloc())
    elif text.find('интернет') != -1:
        if userid == adminid:
            bot.send_message(userid, show.inet())
    elif text.find('деньги') != -1:
        if userid == adminid:
            bot.send_message(userid, show.oniksmoney())
    elif text.find('газ') != -1:
        if userid == adminid:
            bot.send_message(userid, show.checkgaz())
    elif text.find('проверка текста') != -1:
        checkgraf(message)  # нельзя в другом файле, так как отправка сообщения только через сенд месс, иначе краш
    # elif text.find('дота') != -1:
    #     bot.send_message(userid, 'Новости Доты :', reply_markup=buttondota())
    elif text.find('скачать') != -1:
        if text.find('фильм') != -1:
            checkfilm(message)
        elif text.find('игру') != -1:
            checkgame(message)
    elif text.find('свет') != -1:
        if userid == adminid:
            bot.send_message(userid, show.check_light())


print("I'm Work!")
bot.infinity_polling(True)
