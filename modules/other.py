from vkbottle.bot import BotLabeler, Message
from sys import platform

import TtoS

other_labeler = BotLabeler()
other_labeler.vbml_ignore_case = True

"""
  НЕ трогать! Если команда/ответ будет изменён, можете не обращаться к разработчику за помощью, да, вот такой я злой!
"""

update = '0.5.0.2'
txt = TtoS.Image()

@other_labeler.message(text='update')
async def help_cmd(message: Message):
    try:
        await message.answer(
            message=f"Project: fixees.ru/projects/vk-rcon-minecraft/ \n* Update: {update} \n* Platform: {platform} \n\n {txt.output('fixees', 'made_by')}")

    except Exception as e:
        await message.reply('⚠ / Произошла ошибка, код ошибки: {0}'.format(e))
