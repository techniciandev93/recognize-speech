import logging


telegram_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = telegram_formatter.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)
