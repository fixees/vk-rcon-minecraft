import json
import re
import sqlite3

from mcrcon import MCRcon


class DataBase:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        self.__instance = None

    def __init__(self):
        self.con = sqlite3.connect("database.sqlite")
        self.cur = self.con.cursor()


db = DataBase()


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


def w_server(name, ip, port, passw):
    db.cur.execute(
        "INSERT INTO servers (name, rcon_ip, rcon_password, rcon_port) VALUES (?, ?, ?, ?)",
        (
            name,
            ip,
            passw,
            port
        )
    )
    db.con.commit()


def easy_already_server(name_server):
    db.cur.execute("SELECT name FROM servers WHERE name = ?", (name_server,))

    if db.cur.fetchone() is not None:
        return True


def easy_create_user(new_id, name, perms, value):

    db.cur.execute("INSERT INTO users (id, name, permission_rcon, permission_bot) VALUES (?, ?, ?, ?)",
        (
            new_id,
            name,
            perms,
            value
        )
    )
    db.con.commit()


def easy_get_user(id):
    db.cur.execute("SELECT id FROM users WHERE id = ?", (id,))

    if db.cur.fetchone() is not None:
        return True


def easy_get_perm(perm, id):
    db.cur.execute("SELECT permission_rcon FROM users WHERE id = ?", (id,))
    permission_rcon = db.cur.fetchone()

    if permission_rcon is not None and str(permission_rcon[0]) == str(perm):
        return permission_rcon


def easy_update_perm(id, perm):
    db.cur.execute("UPDATE users SET permission_rcon = ? WHERE id = ?", (perm, id))
    db.con.commit()


def all_servers():
    db.cur.execute("SELECT * FROM servers")
    values = db.cur.fetchall()

    servers = ''

    for count, i in enumerate(values):
        count = count + 1
        servers += '{0}. {1} | {2}:{3} \n'.format(count, i[0], i[1], i[3])

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


def profile(id, ret: ('perm', 'status') = None):
    db.cur.execute("SELECT * FROM users WHERE id = ?", (id,))
    values = db.cur.fetchone()

    rcon_string = values[2]  # rcon
    status_string = values[3]  # bot

    match ret:
        case 'perm':
            return rcon_string
        case 'status':
            return status_string


def easy_check_status(id):
    db.cur.execute("SELECT permission_bot FROM users WHERE id = ?", (id,))
    value = db.cur.fetchone()[0]

    return value


def easy_check_user_in_base(id):
    db.cur.execute(
        "SELECT id FROM users WHERE id = ?", id
    )
    value = db.cur.fetchone()

    if value is not None:
        return True


def easy_rename_status(id, name):
    db.cur.execute("UPDATE users SET permission_bot = ? WHERE id = ?", (name, id))
    db.con.commit()


def easy_check_server(name_server, ret: ('bool', 'ip', 'passw', 'port') = None):
    db.cur.execute(f"SELECT * FROM servers WHERE name = '{name_server}'")
    values = db.cur.fetchone()

    if values is not None:

        match ret:
            case 'bool':
                return True
            case 'ip':
                return values[0]
            case 'passw':
                return values[2]
            case 'port':
                return values[1]


def easy_check_perm(id):
    db.cur.execute("SELECT permission_rcon FROM users WHERE id = ?", (id,))
    return db.cur.fetchone()[0]


def easy_check_perms_user(id):
    with open('servers.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

        db.cur.execute('SELECT permission_rcon FROM users WHERE id = ?', (id,))
        perms = db.cur.fetchone()[0]

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
