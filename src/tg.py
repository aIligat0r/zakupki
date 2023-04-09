import time

import telebot

import config
from src import logger


bot = telebot.TeleBot(config.TG_BOT_TOKEN)


def tg_send_message(text: str, mode="MarkdownV2"):
    while True:
        try:
            bot.send_message(
                chat_id=config.TG_CHAT_ID,
                text=str(text),
                parse_mode=mode,
                disable_web_page_preview=True,
            )
            return
        except telebot.apihelper.ApiTelegramException:
            logger.error("telebot sleep (flood message)")
            time.sleep(15)
