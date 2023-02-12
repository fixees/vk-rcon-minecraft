import json
import re

from mcrcon import MCRcon


def get_replace():
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data['replacement']


def get_prefix():
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data['prefix']


def get_token():
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data['token']


def get_owner():
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data['owner_id']


def set_prefix(prefix):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        data['prefix'] = prefix

        with open("servers.json", "w", encoding='utf-8') as jsonFile:
            json.dump(data, jsonFile, indent=4, ensure_ascii=False)


def set_token(token):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        data['token'] = token

        with open("servers.json", "w", encoding='utf-8') as jsonFile:
            json.dump(data, jsonFile, indent=4, ensure_ascii=False)


def set_owner(owner):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        data['owner_id'] = owner
        with open("servers.json", "w", encoding='utf-8') as jsonFile:
            json.dump(data, jsonFile, indent=4, ensure_ascii=False)


def set_replace(boolean):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        data['replacement'] = boolean
        with open("servers.json", "w", encoding='utf-8') as jsonFile:
            json.dump(data, jsonFile, indent=4, ensure_ascii=False)


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
                if i['rcon'] == str(perm):
                    perms = i['rcon']
                    return perms


def easy_update_perm(id, perm):
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)

    for i in data['users']:
        if i["id"] == str(id):
            i["rcon"] = perm
            with open("servers.json", "w", encoding='utf-8') as jsonFile:
                json.dump(data, jsonFile, indent=4, ensure_ascii=False)
            return True


def all_servers():
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    servers = ''
    for i in data['servers']:
        servers += '| {0} / {1}:{2},\n'.format(i['name'], i['rcon_ip'], i['rcon_port'])
    return servers


def check_perms(name_perms, ret: ('perms') = None):
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    for a in data["perms"]:
        for x in a['{0}'.format(name_perms)]:
            perms_list = ''
            for perms in x['perm']:
                perms_list += ' {0} |'.format(perms)
            match ret:
                case 'perms':
                    return perms_list


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


def profile(ids, ret: ('perm', 'status') = None):
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)

    perm_string = ''
    status_string = ''
    for x in data['users']:
        if x['id'] == str(ids):
            perm_string += x['rcon']
            status_string += x['perms']
    match ret:
        case 'perm':
            return perm_string
        case 'status':
            return status_string


def easy_check_status(id):
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    for a in data["users"]:
        if a['id'] == str(id):
            status = a['perms']
            return status


def easy_check_user_in_base(id):
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)

    user = ''
    for a in data["users"]:
        if a['id'] == str(id):
            user += '+'
            return True
    if user == '':
        return False


def easy_rename_status(id, name):
    with open("servers.json", "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)

        for x in data['users']:
            if x['id'] == str(id):
                x['perms'] = name
                with open("servers.json", "w", encoding='utf-8') as jsonFile:
                    json.dump(data, jsonFile, indent=4, ensure_ascii=False)
                break


def easy_check_server(name_server, ret: ('bool', 'ip', 'passw', 'port') = None):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['servers']:
            # Если name_server есть в i['name']
            if i['name'] == name_server:
                ip = i['rcon_ip']
                passw = i['rcon_pass']
                port = i['rcon_port']
                match ret:
                    case 'bool':
                        return True
                    case 'ip':
                        return ip
                    case 'passw':
                        return passw
                    case 'port':
                        return port


def easy_check_perm(id):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['users']:
            if i['id'] == str(id):
                perms = i['rcon']
                return perms


def easy_check_perms_user(id):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['users']:
            if i['id'] == str(id):
                perms = i['rcon']

        for x in data['perms']:
            for y in x['{0}'.format(perms)]:
                perms = y['perm']
                return perms


def send_message_rcon(cmd, server):
    r_a = str(easy_check_server(name_server=server, ret='ip'))
    r_pass = str(easy_check_server(name_server=server, ret='passw'))
    r_pt = int(easy_check_server(name_server=server, ret='port'))

    with MCRcon(host=r_a, password=r_pass, port=r_pt, timeout=5, tlsmode=0) as mcr:
        resp = re.sub('§e|§a|§c|§l|§b|§d|§f|§k|§m|§n|§o|§r|§0|§1|§2|§3|§4|§5|§6|§7|§8|§9', '',
                      mcr.command(cmd))
        return resp
