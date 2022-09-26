from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message

import json
from settings import owner_id

from settings import owner_id


class Permission(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        with open("servers.json", "r+", encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
        for a in data["users"]:
            if str(event.from_id) in a['id']:
                return True

        if event.from_id == owner_id:
            return True
