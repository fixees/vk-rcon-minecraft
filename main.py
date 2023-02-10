from vkbottle import Bot
from settings import api, state_dispenser, labeler
from modules import rcon_labeler, other_labeler, help_labeler

labeler.load(rcon_labeler)
labeler.load(other_labeler)
labeler.load(help_labeler)

bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)

# Start
bot.run_forever()
