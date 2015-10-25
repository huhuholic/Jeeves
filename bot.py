#!/usr/bin/python3

'''Using Webhook and self-signed certificate'''

# This file is an annotated example of a webhook based bot for
# telegram. It does not do anything useful, other than provide a quick
# template for whipping up a testbot. Basically, fill in the CONFIG
# section and run it.
# Dependencies (use pip to install them):
# - python-telegram-bot: https://github.com/leandrotoledo/python-telegram-bot
# - Flask              : http://flask.pocoo.org/
# Self-signed SSL certificate (make sure 'Common Name' matches your FQDN):
# $ openssl req -new -x509 -nodes -newkey rsa:1024 -keyout server.key -out server.crt -days 3650
# You can test SSL handshake running this script and trying to connect using wget:
# $ wget -O /dev/null https://$HOST:$PORT/

# TODO: Implement logger

from flask import Flask, request
from botLogic import BotLogic
from db import DatabaseWorker
import telegram
import sqlite3

# CONFIG
TOKEN    = '156292358:AAEPeTrjulpt5IrNwUi5kKQ-bhsVkOTcMmo'
HOST     = 'huhuholic.info' # Same FQDN used when generating SSL Cert
PORT     = 8443
CERT     = '/etc/ssl/crt/server.crt'
CERT_KEY = '/etc/ssl/crt/server.key'

bot = telegram.Bot(TOKEN)
app = Flask(__name__)
context = (CERT, CERT_KEY)
conn = sqlite3.connect("jeeves.db")
with conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users"
                "(id TEXT, first_name TEXT, last_name TEXT, username TEXT, is_friend TEXT)")

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True))
    chat_id = update.message.chat.id
    message = update.message.text
    user = update.message.from_user
    conn_hook = sqlite3.connect("jeeves.db")
    with conn_hook:
        cur_hook = conn_hook.cursor()
        cur_hook.execute("SELECT * FROM users WHERE id = ?", (user.id, ))
        if cur_hook.rowcount > 0:
            pass  # The user is already in the database
        else:
            cur_hook.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)",
                             (user.id, user.first_name, user.last_name, user.username, "False"))

    logic = BotLogic(bot, message, chat_id)

    if '/start' == message or '/help' == message:
        logic.start_help()

    if '/time' == message:
        logic.get_time()

    if '/trtoen' in message:
        text_to_translate = message[8:]
        logic.translate_to_en(text_to_translate)

    if '/whattime' == message:
        logic.what_time()

    return 'OK'


def setWebhook():
    bot.setWebhook(webhook_url='https://%s:%s/%s' % (HOST, PORT, TOKEN),
                   certificate=open(CERT, 'rb'))

if __name__ == '__main__':
    setWebhook()

    app.run(host='0.0.0.0',
            port=PORT,
            ssl_context=context,
            debug=True)
