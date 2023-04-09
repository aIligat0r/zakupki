import time

import config
from tg import tg_send_message
from monitor import Monitor

from src.logger import logger


def monitor():
    mon = Monitor()
    results = mon.parse()
    for zakupka in results["eis"]:
        tg_message = f"""
<b>rule:</b> <code>{zakupka["product_category"]}</code>
<b>keyword:</b> <code>{zakupka["search_keyword"]}</code>

<b>название:</b> <code>{zakupka["name"]}</code>

<b>начальная цена:</b> <i>{"{:,.2f}".format(zakupka["start_price"])}</i>

<b>заказчик:</b> <code>{zakupka["customer_name"]}</code>

<b>до:</b> {zakupka["end_date"]}
<b>тендер:</b> {zakupka["link"]}
"""
        logger.info("tender from EIS sent tg: %s" % zakupka)
        tg_send_message(text=tg_message, mode="HTML")

    for zakupka in results["mos"]:
        tg_message = f"""
<b>rule:</b> <code>{zakupka["product_category"]}</code>
<b>keyword:</b> <code>{zakupka["search_keyword"]}</code>

<b>статус:</b> <code>{zakupka["status"]}</code>

<b>название:</b> <code>{zakupka["name"]}</code>

<b>начальная цена:</b> <i>{zakupka["start_price"]}</i>

<b>заказчик:</b> <code>{zakupka["customer_name"]}</code>

<b>до:</b> {zakupka["end_date"]}

<b>тендер:</b> {zakupka["link"]}
"""
        logger.info("tender from MOS sent tg: %s" % zakupka)
        tg_send_message(text=tg_message, mode="HTML")


if __name__ == "__main__":
    while True:
        logger.info("start monitoring")
        monitor()
        logger.info("sleeping: %s minutes" % config.SLEEP_TIME)
        time.sleep(config.SLEEP_TIME * 60)
