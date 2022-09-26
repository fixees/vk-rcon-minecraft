from vkbottle.bot import Bot, Message, BotLabeler
from vkbottle import API, BaseStateGroup, VKAPIError, VKAPIError, BaseMiddleware
from mcrcon import MCRcon
import asyncio
import json
import re

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
            await message.reply(
                '♻ | Сервер {0}, со значениями: \n- Пароль {1}\n- Айпи {2}\n\nБыл добавлен!'.format(name, passw, ip))
    except Exception as e:
        await message.reply(e)


# --------------------------------------------------------


def easy_create_user(new_data):
    with open('servers.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        for i in file_data['users']:
            file_data["users"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4, ensure_ascii=False)
            break


def easy_get_user(id):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['users']:
            if i['id'] == str(id):
                return True


def easy_get_perm(perm, id):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['users']:
            if i['id'] == str(id):
                if i['perms'] == str(perm):
                    perms = i['perms']
                    return perms


def easy_update_perm(id, perm):
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)

    for i in data['users']:
        if i["id"] == str(id):
            i["perms"] = perm
            with open("servers.json", "w", encoding='utf-8') as jsonFile:
                json.dump(data, jsonFile, indent=4, ensure_ascii=False)
            return True


@bot.on.private_message(Permission(), text='{0}права сет <user> <perms>'.format(prefix_cmd))
async def cmd_set_perms(message: Message, user, perms):
    id_ = re.findall(r'.права сет \[id(\d*)\|.*]', message.text)
    new_id = id_[0]
    try:
        if easy_get_user(id=new_id) == True:
            if easy_get_perm(perm=perms, id=new_id) == perms:
                await message.reply('⚠ | Юзер уже имеет такие права')
                return
        if perms not in all_perms(ret='massive'):
            await message.reply('⚠ | Права {0} не найдены!'.format(perms))


        elif easy_get_user(id=new_id) == True:
            if perms in all_perms(ret='massive'):
                easy_update_perm(id=new_id, perm=perms)
                await message.reply('♻ | Пользователь {0}, с правами {1}, был обновлен!'.format(new_id, perms))

        elif perms in all_perms(ret='massive'):
            y = {
                "id": "{0}".format(new_id),
                "perms": perms
            }
            easy_create_user(y)
            await message.reply('♻ | Пользователь {0}, с правами {1}, был создан!'.format(new_id, perms))
    except Exception as e:
        await message.reply(e)


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


# ------------------------.права-<name>-значения-------------------------------

def check_perms(name_perms, ret: ('all_perms', 'perms') = None):
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    for a in data["perms"]:
        for x in a['{0}'.format(name_perms)]:
            all_perms = x['all']
            perms_list = ''
            for perms in x['perm']:
                perms_list += ' {0} |'.format(perms)
            match ret:
                case 'all_perms':
                    return all_perms
                case 'perms':
                    return perms_list


@bot.on.private_message(Permission(), text='{0}права <name> значения'.format(prefix_cmd))
async def cmd_perms_list(message: Message, name):
    try:
        if name in all_perms(ret='massive'):
            await message.reply("♻ | Данные привилегии {0}: \n\n".format(name) +
                                "Имеет все права: {0} \n".format(check_perms(name_perms=name, ret='all_perms')) +
                                "Разрешенные пермишнс: {0}".format(check_perms(name_perms=name, ret='perms')))
        else:
            await message.reply('❗ | Привилегии с названием {0}, не найдено!'.format(name))
    except Exception as e:
        await message.reply(e)


# --------------------------------------------------------


# ------------------------.права--------------------------------

def all_perms(ret: ('massive', 'string') = None):
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    servers_massive = ''
    servers_string = ''
    for a in data["perms"]:
        servers_string += '{0}'.format(", ".join(list(a.keys())))
        servers_massive += '{0}'.format(list(a.keys()))
        match ret:
            case 'massive':
                return servers_massive
            case 'string':
                return servers_string


@bot.on.private_message(Permission(), text='{0}права'.format(prefix_cmd))
async def cmd_all_perms(message: Message):
    await message.reply("♻ | Все существующие привилегии: \n" +
                        all_perms(ret='string'))
# --------------------------------------------------------

def profile(ids, ret: ('perm') = None):
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)

    perm_string = ''
    for x in data['users']:
        if x['id'] == str(ids):
            perm_string += x['perms']
    match ret:
        case 'perm':
            return perm_string

@bot.on.private_message(text='{0}профиль'.format(prefix_cmd))
async def cmd_profile(message: Message):
    await message.reply("♻ | Ваш Профиль: \n\n" +
                        'Статус: {0}'.format(profile(ids=message.from_id, ret='perm')))

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


def easy_check_perm(id):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['users']:
            if i['id'] == str(id):
                perms = i['perms']
                return perms


def easy_check_perms_user(id):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['users']:
            if i['id'] == str(id):
                perms = i['perms']

        for x in data['perms']:
            for y in x['{0}'.format(perms)]:
                perms = y['perm']
                return perms


async def send_message_rcon(msg, cmd, server):
    r_a = easy_check_server(name_server=server, ret='ip')
    r_p = easy_check_server(name_server=server, ret='passw')
    with MCRcon(r_a, r_p) as mcr:
        resp = mcr.command(cmd)
        await msg.reply('🗂 | Отправлена команда: /{0}\n'.format(cmd) +
                        'Ответ: \n{0}'.format(resp))


@bot.on.private_message(Permission(), text='{0}<server> <cmd>'.format(prefix_cmd))
async def cmd_send(message: Message, server, cmd):
    try:
        # если сервер существует
        if easy_check_server(name_server=server, ret='bool') == True:
            # если у from_id сущесвуют права
            with open('servers.json', encoding='utf-8') as json_file:
                data = json.load(json_file)

            if cmd in easy_check_perms_user(id=message.from_id):
                await send_message_rcon(message, cmd, server)
            elif cmd not in easy_check_perms_user(id=message.from_id):
                await message.reply('❗ | Вам не разрешено использовать команду {0}'.format(cmd))
            elif message.from_id == owner_id:
                await send_message_rcon(message, cmd, server)
        elif easy_check_server(name_server=server) != True:
            await message.reply('❗ | Сервера {0}, не существует!'.format(server))
    except OSError:
        await message.reply('❗ | Сервер {0}, не отвечает запросу'.format(server))
    except Exception as e:
        await message.reply(e)


@bot.on.private_message(Permission(), text='{0}помощь'.format(prefix_cmd))
async def cmd_send(message: Message):
    await message.reply('📜 | Команды: \n'
                        '{0}профиль - Ваша статистика.\n'.format(prefix_cmd) +
                        '{0}сервера - Показывает все установленные rcon сервера.\n'.format(prefix_cmd) +
                        '{0}<server> <cmd> - Запрос ркон команды.\n'.format(prefix_cmd) +
                        '{0}сервер ген <name> <ip> <passw> - Создает ркон сервер.\n'.format(prefix_cmd) +
                        '{0}права - Показывает все установленные привилегии.\n'.format(prefix_cmd) +
                        '{0}права <perm> значения - Показывает все установленные значения привилегии.\n'.format(prefix_cmd) +
                        '{0}права сет <@nick> <perm>- Устанавливает право пользователю.'.format(prefix_cmd))
                        # '{0}сервер ип <name> <ip> <new_ip> - Переименовывает значени ip на ркон сервере.'.format(prefix_cmd) +
                        # '{0}сервер пасс <name> <pass> <new_pass> - Переименовывает значени pass на ркон сервере.'.format(prefix_cmd))


# Регистрируем класс NoBotMiddleware
bot.labeler.message_view.register_middleware(NoBotMiddleware)
# Start
bot.run_forever()
