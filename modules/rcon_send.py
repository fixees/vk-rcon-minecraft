from vkbottle.bot import BotLabeler, Message
from functions import *
from permission_rule import Permission, PermissionOwners

import difflib
import re

rcon_labeler = BotLabeler()
rcon_labeler.vbml_ignore_case = True

prefix = get_prefix()
owner_id = get_owner()


@rcon_labeler.private_message(PermissionOwners(), text='{0}сервер ген <name> <ip> <port> <passw>'.format(prefix))
async def cmd_add_server(message: Message, name, ip, port, passw):
    try:

        if easy_already_server(name_server=name):
            await message.reply('⚠ | Такое имя уже существует')
        else:
            w_server(name, ip, port, passw)

            await message.reply(
                '♻ | Сервер {0}, со значениями: \n- Пароль: {1}\n- Айпи: {2} : {3}\n\nДобавлен!'.format(name,
                                                                                                        passw,
                                                                                                        ip,
                                                                                                        port))
    except Exception as e:
        await message.reply(f'⚠ | Произошла ошибка: \n {e=}, \n {type(e)=} ')


@rcon_labeler.private_message(PermissionOwners(), text='{0}права сет <user> <perms>'.format(prefix))
async def cmd_set_perms(message: Message, user, perms):
    new_id = re.findall(r"[0-9]+", user)[0]

    user = await message.ctx_api.users.get(new_id)
    name_user = str(user[0].first_name + ' ' + user[0].last_name)

    if easy_get_user(id=new_id):
        if easy_get_perm(perm=perms, id=new_id) == perms:
            await message.reply('⚠ | [id{0}|Пользователь] уже имеет такие права'.format(new_id))

    if perms not in all_perms(ret='massive'):
        await message.reply('⚠ | Права {0} не найдены!'.format(perms))

    elif easy_get_user(id=new_id):
        if perms in all_perms(ret='massive'):
            easy_update_perm(id=new_id, perm=perms)
            await message.reply('♻ | [id{0}|Пользователь], с правами {1}, был обновлен!'.format(new_id, perms))

    elif perms in all_perms(ret='massive'):
        easy_create_user(str(new_id), name_user, perms, 0)

        await message.reply('♻ | [id{0}|Пользователь], с правами {1}, был создан!'.format(new_id, perms))


@rcon_labeler.private_message(PermissionOwners(), text='{0}сервера'.format(prefix))
async def cmd_all_servers(message: Message):
    await message.reply("♻ | Все существующие сервера: \n\n" +
                        all_servers())


@rcon_labeler.private_message(PermissionOwners(), text='{0}права <name> значения'.format(prefix))
async def cmd_perms_list(message: Message, name):
    try:
        if name in all_perms(ret='massive'):
            await message.reply("♻ | Данные привилегии {0}: \n\n".format(name) +
                                "Разрешенные права: {0}".format(check_perms(name_perms=name, ret='perms')))
        else:
            await message.reply('❗ | Привилегии с названием {0}, не найдено!'.format(name))
    except Exception as e:
        await message.reply(f'⚠ | Произошла ошибка: \n {e=}, \n {type(e)=} ')


@rcon_labeler.private_message(PermissionOwners(), text='{0}права'.format(prefix))
async def cmd_all_perms(message: Message):
    await message.reply("♻ | Все существующие привилегии: \n" +
                        all_perms(ret='string'))


@rcon_labeler.private_message(Permission(), text='{0}профиль'.format(prefix))
async def cmd_profile(message: Message):
    if profile(id=message.from_id, ret='status') not in ['*', '**']:
        cmd_open = check_perms(name_perms=profile(id=message.from_id, ret='perm'), ret='perms')
    else:
        cmd_open = 'все команды.'

    if profile(id=message.from_id, ret='status') == '**':
        cmd_add = 'Владелец'
    elif profile(id=message.from_id, ret='status') == '*':
        cmd_add = 'Админ'
    else:
        cmd_add = 'Нету'

    await message.reply("♻ | Ваш Профиль: \n\n" +
                        'Права: {0} / Доп.Права: {1} ({2}) \n'.format(profile(id=message.from_id, ret='perm'),
                                                                      profile(id=message.from_id, ret='status'),
                                                                      cmd_add) +
                        'Доступные тебе команды из ркона: {0}'.format(cmd_open))


@rcon_labeler.private_message(PermissionOwners(), text='{0}права доп-доступ <nick> <name>'.format(prefix))
async def cmd_set_status(message: Message, nick, name):
        new_id = re.findall(r"[0-9]+", nick)[0]

        if name in ['**', '*']:

            if not easy_check_user_in_base(new_id):
                await message.reply('⚠ | Пользователь не найден в базе!')

            elif easy_check_status(new_id) == name:
                await message.reply('⚠ | Пользователь уже имеет такой доступ!')

            elif str(new_id) == str(nick):
                await message.reply('⚠ | Нельзя изменять доступ самому себе!')

            elif easy_check_user_in_base(new_id):
                easy_rename_status(new_id, name)
                await message.reply('♻ | Пользователь теперь имеет доступ {0}'.format(name))
        else:
            await message.reply('⚠ | Доступ {0} не существует!'.format(name))



@rcon_labeler.private_message(Permission(), text='{0}ркон <server> <cmd>'.format(prefix))
async def cmd_send(message: Message, server, cmd):
    try:
        if easy_check_server(name_server=server, ret='bool'):

            # easy_check_perms_user(id=message.from_id) = ['list', 'ban {0}']
            # cmd = ban fix

            end = cmd  # ban fixees
            end_list = end.split()  # ['ban', 'fixees']

            print(end_list)  # ['ban', 'fixees']
            print(easy_check_perms_user(id=message.from_id))

            command = difflib.get_close_matches(end_list[0],
                                                easy_check_perms_user(id=message.from_id))

            if 0 < len(command):
                command = command[0]

            if command in easy_check_perms_user(id=message.from_id):

                if '{0}' in end:
                    command_list = command.split()
                    number = 0

                    for count, i in enumerate(command_list):
                        if i == '{0}':
                            number += count

                    def replace_text(n, text):
                        command_list[n] = text
                        return command_list

                    replace_text(number, end_list[number])

                await message.reply('🗂 | Отправлена команда: /{0}\n'.format(cmd) +
                                    'Ответ: \n{0}'.format(send_message_rcon(end, server)))

            elif profile(id=message.from_id, ret='status') in ['*', '**']:

                if '{0}' in end:
                    command_list = command.split()
                    number = 0

                    for count, i in enumerate(command_list):
                        if i == '{0}':
                            number += count

                    def replace_text(n, text):
                        command_list[n] = text
                        return command_list

                    replace_text(number, end_list[number])

                await message.reply('🗂 | Отправлена команда: /{0}\n'.format(cmd) +
                                    'Ответ: \n{0}'.format(send_message_rcon(cmd, server)))

            elif command not in easy_check_perms_user(id=message.from_id):

                await message.reply('❗ | Вам не разрешено использовать команду {0}'.format(cmd))

        elif not easy_check_server(name_server=server):
            await message.reply('❗ | Сервера {0}, не существует!'.format(server))

    except OSError:
        await message.reply('❗ | Сервер {0}, не отвечает запросу'.format(server))
    except Exception as e:
        await message.reply(f'⚠ | Произошла ошибка: \n {e=}, \n {type(e)=} ')
