#!/usr/bin/python
# -*- coding: utf-8 -*-

from functions import DataBase
from vkbottle import Bot
from functions import get_owner
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

db = DataBase()


def create_owner():
    db.cur.execute('SELECT id FROM users WHERE id = ?', (get_owner(),))
    value = db.cur.fetchone()

    if value is None:
        db.cur.execute(
            "INSERT INTO users (id, name, permission_rcon, permission_bot) VALUES (?, ?, ?, ?)",
            (
                get_owner(),
                'Владелец',
                'ADMIN',
                '**'
            )
        )
        db.con.commit()


create_owner()

# Start
bot.run_forever()
