from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters

from tginviter.bot.base_bot import BaseBot


class PythonTelegramBot(BaseBot):
    def __init__(self, *, token, deeplink_handler, job_handler, interval=5):
        """Wrapper for Updater and Dispatcher with deeplink and job handlers"""

        self.updater = Updater(token, use_context=True)
        self.dp = self.updater.dispatcher

        self.dp.add_handler(
            CommandHandler(
                "start",
                deeplink_handler,
                pass_args=True,
                filters=Filters.regex("/start \S+")
            )
        )

        self.updater.job_queue.run_repeating(
            job_handler,
            interval=interval,
            first=0
        )

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def get_name(self):
        return self.updater.bot.getMe()["username"]
