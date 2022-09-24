from vkbottle.bot import Bot, Message, BotLabeler
from vkbottle import API, BaseStateGroup, VKAPIError, VKAPIError, BaseMiddleware
from mcrcon import MCRcon
import asyncio
import json

from _permission_rule import Permission
from settings import token, rcon_pass, rcon_address, owner_id, prefix_cmd

# Токен находится в settings.py
bot = Bot(token)


# Бот не будет отвечать, если напишет группа
class NoBotMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        if self.event.from_id < 0:
            self.stop("Группам не разрешено использовать функционал.")


# ------------------------.сервер добавить--------------------------------

def w_server(new_data):
    with open('servers.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        for i in file_data['servers']:
            file_data["servers"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4, ensure_ascii=False)
            break

def easy_already_server(name_server):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['servers']:
            if i['name'] == str(name_server):
                return True

@bot.on.private_message(Permission(), text='{0}сервер ген <name> <ip> <passw>'.format(prefix_cmd))
async def cmd_add_server(message: Message, name, ip, passw):

    try:
        # если name существует == True:

        if easy_already_server(name_server=name) == True:
             await message.reply('⚠ | Такое имя уже существует')
        else:
            y = {
                "name": name,
                "rcon_ip": ip,
                "rcon_pass": passw
            }
            w_server(y)
            await message.reply('♻ | Сервер {0}, со значениями: \n- Пароль {1}\n- Айпи {2}\n\nБыл добавлен!'.format(name, passw, ip))
    except Exception as e:
        await message.reply(e)


# --------------------------------------------------------





# ------------------------.сервера--------------------------------

def all_servers():
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    servers = ''
    for i in data['servers']:
        servers += '| {0} / {1},\n'.format(i['name'], i['rcon_ip'])
    return servers


@bot.on.private_message(Permission(), text='{0}сервера'.format(prefix_cmd))
async def cmd_all_servers(message: Message):
    await message.reply("♻ | Все существующие сервера: \n" +
                        all_servers())


# --------------------------------------------------------

def easy_check_server(name_server, ret: ('bool', 'ip', 'passw') = None):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['servers']:
            # Если name_server есть в i['name']
            if i['name'] == name_server:
                ip = i['rcon_ip']
                passw = i['rcon_pass']
                match ret:
                    case 'bool':
                        return True
                    case 'ip':
                        return ip
                    case 'passw':
                        return passw

@bot.on.private_message(Permission(), text='{0}<server> <cmd>'.format(prefix_cmd))
async def cmd_send(message: Message, server, cmd):
    try:
        if easy_check_server(name_server=server, ret='bool') == True:
            r_a = easy_check_server(name_server=server, ret='ip')
            r_p = easy_check_server(name_server=server, ret='passw')
            with MCRcon(r_a, r_p) as mcr:
                resp = mcr.command(cmd)
                await message.reply('🗂 | Отправлена команда: /{0}\n'.format(cmd) +
                                        'Ответ: \n{0}'.format(resp))
        elif easy_check_server(name_server=server) != True:
                await message.reply('❗ | Сервера {0}, не существует!'.format(server))
    except OSError:
        await message.reply('❗ | Сервер {0}, не отвечает запросу'.format(server))
    except Exception as e:
        await message.reply(e)

@bot.on.private_message(Permission(), text='{0}помощь'.format(prefix_cmd))
async def cmd_send(message: Message):
    await message.reply('📜 | Команды: \n'
                        '{0}сервера - Показывает все установленные rcon сервера.\n'.format(prefix_cmd) +
                        '{0}<server> <cmd> - Запрос ркон команды.\n'.format(prefix_cmd) +
                        '{0}сервер ген <name> <ip> <passw> - Создает ркон сервер.'.format(prefix_cmd))
                        #'{0}сервер ип <name> <ip> <new_ip> - Переименовывает значени ip на ркон сервере.'.format(prefix_cmd) +
                        #'{0}сервер пасс <name> <pass> <new_pass> - Переименовывает значени pass на ркон сервере.'.format(prefix_cmd))

# Регистрируем класс NoBotMiddleware
bot.labeler.message_view.register_middleware(NoBotMiddleware)
# Start
bot.run_forever()
