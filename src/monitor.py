import json
import sqlite3

from src.mos import mos
from src.eis import eis
from src import logger


class Monitor:
    with open("data/search_rules.json", encoding="utf-8") as rules_file:
        search_rules = json.loads(rules_file.read())

    def __init__(self):
        self.db_connect = sqlite3.connect("zakupki.db")
        self.db_cursor = self.db_connect.cursor()
        self.db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS zakupki (
            name TEXT,
            link TEXT
        );
        """
        )

    def _db_check(self, link: str):
        self.db_cursor.execute(
        """
        SELECT name FROM zakupki WHERE link=?;
        """, [link]
        )
        if self.db_cursor.fetchone():
            return True  # if exists
        return False

    def _db_write(self, name: str, link: str):
        self.db_cursor.execute(
        """
        INSERT INTO zakupki VALUES (?, ?)
        """, [name, link]
        )
        self.db_connect.commit()

    def _results(self, zakupki: list):
        checked_zakupki = []
        for zakupka in zakupki:
            if not self._db_check(zakupka["link"]):  # if not exists
                checked_zakupki.append(zakupka)
                self._db_write(zakupka["name"], zakupka["link"])
        return checked_zakupki

    def parse(self):
        logger.info("start: MOS")
        rsc_mos = mos.MOS(self.search_rules)
        logger.info("start: EIS")
        rsc_eis = eis.EIS(self.search_rules)
        results = {
            "eis": self._results(rsc_eis.parse()[0]),
            "mos": self._results(rsc_mos.parse()[0]),
        }
        return results
