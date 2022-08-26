import telebot.apihelper
from set_bot_command import set_default_commands
from loguru import logger
from loader import bot
from keyboard import keyboards_button
from data_base import recording_user_id, path_mysql_database, record_message_id
from config import ADMIN
from telebot.types import Message
import os
from class_user import User, User_time
import time
from re import match

#ERROR - TeleBot:


logger.add('debug_telegram.log',
           format='{time} {level} {message}',
           level='DEBUG',
           rotation='2000 KB')





@bot.message_handler(commands=['start'])
@logger.catch()
def start_bot(message: Message) -> None:
    """Функция главной страницы
    :type message: Message
    :return: None"""
    path_text = os.path.abspath('head_text.txt')
    name = message.from_user.full_name
    with open(path_text, 'r', encoding='utf-8') as file:
        result_text = file.read()

        bot.send_message(message.from_user.id, f'{name},  {result_text}')

    recording_user_id(message.from_user.id)



@bot.message_handler(commands=['secret'], content_types=['text'])
def mailing_message(message: Message) -> None:
    """Функция массовой рассылки
    :type message: Message
    :return: None"""
    if message.from_user.id == int(ADMIN):
        count = 0
        data = []
        conn = path_mysql_database()
        cur = conn.cursor()
        query = 'SELECT * FROM user_id'
        cur.execute(query)

        for users in cur:
            data.append(users)

        total = message.text
        print(message.text)
        for total_user in data:
            try:
                bot.send_message(total_user[0], f'{total[7::]}')

                logger.info(message.message_id)
                count += 1
                if count == 25:
                    count = 0
                    time.sleep(1)
            except telebot.apihelper.ApiException:
                logger.error(telebot.apihelper.ApiException)




@bot.message_handler(commands=['cons'])
def consultation_answer(message: Message) -> None:
    """Функция запрашивает кому ответить на вопрос
    :type message: Message
    :return: None"""
    logger.info(message.from_user.id)
    if message.from_user.id == int(ADMIN):
        bot.send_message(ADMIN, 'Кому ты хочешь ответить? ')

        bot.register_next_step_handler(message, total_consultation)




def total_consultation(message: Message) -> None:
    """Функция запроса ответа
    :type message: Message
    :return: None"""
    text = message.text
    pattern = r'\d+'
    number = match(pattern, text)
    User.get_user(int(number.group()))

    bot.send_message(message.from_user.id, 'Марина, введи текст ответа:')
    bot.register_next_step_handler(message, result)



def result(message: Message) -> None:
    """Функция подтверждения отправки ответа на вопрос
    :type message: Message
    :return: None"""
    logger.info(User.set_user())
    bot.send_message(message.from_user.id, 'Отправил сообщение')
    if message.content_type == 'text':
        bot.send_message(User.set_user(), message.text)
    elif message.content_type == 'document':
        bot.send_document(User.set_user(), message.document.file_id, caption=message.caption)
    elif message.content_type == 'video':
        bot.send_video(User.set_user(), message.video.file_id, caption=message.caption)
    elif message.content_type == 'photo':
        bot.send_photo(User.set_user(), message.photo[3].file_id, caption=message.caption)


@logger.catch()
@bot.message_handler(func=lambda message: True, content_types=['text', 'document', 'video', 'photo'])
def consultation(message: Message) -> None:
    """функция которая отправлят вопросы АДМИНУ, в виде текста, фото, видео или документа
    :type message: Message
    :return: None"""
    user_name = message.from_user.username
    user_id = message.from_user.id
    user = User_time.get_user(user_id)
    print(message)
    if user == 'yes':
        if message.content_type == 'text':
            bot.send_message(ADMIN, f'{user_id} пользователь {message.from_user.full_name} @{user_name}, спрашивает:\n'
                                    f'{message.text}\n'
                                    f'---------------------')
        elif message.content_type == 'document':
            bot.send_message(ADMIN, f'{user_id} пользователь {message.from_user.full_name} @{user_name}, прислал документ:\n')
            bot.send_document(ADMIN, message.document.file_id, caption=message.caption)
        elif message.content_type == 'video':
            bot.send_message(ADMIN, f'{user_id} пользователь {message.from_user.full_name} @{user_name}, прислал видео:\n')
            bot.send_video(ADMIN, message.video.file_id, caption=message.caption)
        elif message.content_type == 'photo':
            bot.send_message(ADMIN, f'{user_id} пользователь {message.from_user.full_name} @{user_name}, прислал фото:\n')
            bot.send_photo(ADMIN, message.photo[3].file_id, caption=message.caption)

    elif user is None:
        bot.send_message(user_id, 'Извините, но вы слишком часто отправляете сообщения, напишите через 10 секунд')





@logger.catch()
def main():
    """Функция работы бота"""
    try:
        if __name__ == '__main__':
            set_default_commands(bot)
            bot.infinity_polling()
    except Exception as error:
        logger.error(error)


main()
