import telegram

from core.conf import Settings


class PharmZakazTelegramBot:
    msg = None

    def __init__(self):
        self.conf = Settings()
        self.chat_id = self.conf.CHAT_ID
        self.bot = telegram.Bot(token=self.conf.TELEGRAM_BOT_TOKEN)

    def send_msg(self, chat_id=None, msg=None):
        if not msg:
            msg = self.msg
        if not chat_id:
            chat_id = self.chat_id
        self.bot.send_message(chat_id=chat_id, text=str(msg))
