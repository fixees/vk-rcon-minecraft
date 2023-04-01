from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message
from functions import get_owner
from functions import DataBase

import json

id_owner = get_owner()
db = DataBase()

class PermissionOwners(ABCRule[Message]):
    async def check(self, event: Message) -> bool:

        db.cur.execute(f'SELECT permission_bot FROM users WHERE id = {event.from_id}')
        perm = db.cur.fetchone()

        if perm is not None:
            if perm[0] == '**':
                return True


class Permission(ABCRule[Message]):
    async def check(self, event: Message) -> bool:

        db.cur.execute(f'SELECT permission_bot FROM users WHERE id = {event.from_id}')
        perm = db.cur.fetchone()

        if perm is not None:
            return True

        elif event.from_id == id_owner:
            return True
