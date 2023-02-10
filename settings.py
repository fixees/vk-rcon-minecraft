from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler
from functions import get_token

token = get_token()

api = API(token)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
