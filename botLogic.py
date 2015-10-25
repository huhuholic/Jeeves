import telegram
import time
import goslate


class BotLogic:

    def __init__(self, bot: telegram.Bot, message: str, chat_id: str):
        self.bot = bot
        self.message = message
        self.chat_id = chat_id
        self.translator = goslate.Goslate()

    def reply_text(self, text: str):
        self.bot.sendMessage(chat_id=self.chat_id, text=text)

    def start_help(self,):
        text = 'Hello! I am Jeeves, there is nothing I can help you with unfortunately.'
        self.reply_text(text)

    def get_time(self):
        text = time.ctime()
        self.reply_text(text)

    def translate_to_en(self, text_to_translate: str):
        #text = self.translator.translate(text_to_translate, 'en')
        text = "Not yet working, bro :("
        self.reply_text(text)

    def what_time(self):
        urtime = "ADVENTURE TIME!"
        self.reply_text(urtime)
        stick = "BQADAgADeAcAAlOx9wOjY2jpAAHq9DUC"
        self.bot.sendSticker(self.chat_id, stick)









