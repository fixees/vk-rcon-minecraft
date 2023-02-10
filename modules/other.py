from vkbottle.bot import BotLabeler, Message
from functions import get_prefix

from sys import platform
import time

other_labeler = BotLabeler()
other_labeler.vbml_ignore_case = True

"""
  НЕ трогать! Если команда/ответ будет изменён, можете не обращаться к разработчику за помощью, да, вот такой я злой!
  Можно изменить только доступ к команде
"""

update = '0.0.5'


@other_labeler.message(text='{0}test'.format(get_prefix()))
async def help_cmd(message: Message):
    try:
        await message.reply(f"Проект -> https://fixees.ru/projects | Update {update} \nPlatform: {platform} \nTime: {time.time()}")

    except Exception as e:
        await message.reply('⚠ / Произошла ошибка, код ошибки: {0}'.format(e))
