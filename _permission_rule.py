from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message

from settings import owner_id


class Permission(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        return event.from_id == owner_id
