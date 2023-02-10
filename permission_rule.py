from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message

from functions import get_owner
import json

id_owner = get_owner()

"""
 Я тут ничего не переделывал
"""


class PermissionOwners(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        with open("servers.json", "r+", encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)

        for a in data["users"]:
            if str(event.from_id) in a['id']:
                if a['perms'] == '**':
                    return True


class Permission(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        with open("servers.json", "r+", encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
        for a in data["users"]:
            if str(event.from_id) in a['id']:
                return True

        if event.from_id == id_owner:
            return True
