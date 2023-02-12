from vkbottle.bot import BotLabeler, Message
from sys import platform

import time
import TtoS

other_labeler = BotLabeler()
other_labeler.vbml_ignore_case = True

"""
  НЕ трогать! Если команда/ответ будет изменён, можете не обращаться к разработчику за помощью, да, вот такой я злой!
  Можно изменить только доступ к команде
"""

update = '0.5.1.2'
txt = TtoS.Image()


@other_labeler.message(text='test')
async def help_cmd(message: Message):
    try:
        await message.answer(
            message=f"-> fixees.ru/projects \n* Update: {update} \n* Platform: {platform} \n\n {txt.output('fixees', 'made_by')}"

        )

    except Exception as e:
        await message.reply('⚠ / Произошла ошибка, код ошибки: {0}'.format(e))
