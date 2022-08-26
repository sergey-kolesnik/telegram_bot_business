from telebot.types import BotCommand
from loguru import logger

@logger.catch()
def set_default_commands(bot):
    """Функция для генерации команд бота
    :param bot: telebot
    :return: None"""

    command = [BotCommand('start', "Запустить бота")]
    bot.set_my_commands(command)
