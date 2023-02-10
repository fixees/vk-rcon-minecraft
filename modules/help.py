from vkbottle.bot import BotLabeler, Message, rules
from functions import get_prefix

help_labeler = BotLabeler()
help_labeler.vbml_ignore_case = True

prefix = get_prefix()

@help_labeler.message(
    text=['{0}помощь'.format(prefix), '{0}help'.format(prefix), '{0}хелп'.format(prefix), '{0}911'.format(prefix)])
async def help_cmd(message: Message):
    try:
        await message.reply('📜 | Команды: \n'
                            '[id0|{0}профиль] -- Ваша статистика.\n'.format(prefix) +
                            '[id0|{0}сервера] -- Показывает все установленные rcon сервера.\n'.format(prefix) +
                            '[id0|{0}ркон <server> <cmd>] -- Запрос ркон команды.\n'.format(prefix) +
                            '[id0|{0}сервер ген <name> <ip> <port> <passw>] -- Создает ркон сервер.\n'.format(prefix) +
                            '[id0|{0}права] -- Показывает все установленные привилегии.\n'.format(prefix) +
                            '[id0|{0}права <perm> значения] -- Показывает все установленные значения привилегии.\n'.format(prefix) +
                            '[id0|{0}права сет <@nick> <perm>] -- Устанавливает право пользователю.'.format(prefix) +
                            '[id0|{0}права доп-доступ <@nick> <0/*/**>] -- Устанавливает доступ к боту пользователю \n* Только команда ркон\n** Все команды \n0 Запрещенный доступ'.format(prefix))

    except Exception as e:
        await message.reply("⚠ / Произошла ошибка, код ошибки: {0}".format(e))
