import json

from src import needs
from src import logger


def get_api_url(keyword: str, start_price: str, end_price: str):
    return (
        'https://old.zakupki.mos.ru/api/Cssp/Purchase/Query?queryDto={"filter":{"nameLike":"'
        + keyword
        + '",'
        '"regionPaths":[".1.504."],"startPriceGreatEqual":'
        + start_price
        + ',"startPriceLessEqual":'
        + end_price
        + ","
        '"auctionSpecificFilter":{"stateIdIn":[19000002]},"needSpecificFilter":{"stateIdIn":[20000002]},'
        '"tenderSpecificFilter":{"stateIdIn":[5]},"ptkrSpecificFilter":{}},"order":[{"field":"relevance",'
        '"desc":true}],"withCount":true,"take":100,"skip":0}'
    )


class MOS:
    def __init__(self, search_rules: list):
        self.search_rules = search_rules
        self.start_price = "1000"
        self.end_price = "300000"

    @staticmethod
    def _formatter(auction: dict, product_category: str, search_keyword: str):
        link = auction["auctionId"]
        if link:
            link = "https://zakupki.mos.ru/auction/" + str(auction["auctionId"])
        else:
            link = "https://old.zakupki.mos.ru/#/tenders/" + str(auction["tenderId"])

        return {
            "product_category": product_category,
            "link": link,
            "name": auction["name"],
            "status": auction["stateName"],
            "federal_law_name": auction["federalLawName"],
            "customer_name": auction["customers"][0]["name"],
            "customer_region": auction["regionName"],
            "start_price": auction["startPrice"],
            "begin_date": auction["beginDate"],
            "end_date": auction["endDate"],
            "search_keyword": search_keyword,
        }

    def search(self, search_rule: dict):
        formatted_auctions = []
        raw_auctions = []
        for keyword in search_rule["keywords"]:
            logger.info("search by rule: %s" % search_rule)
            response = needs.requester(
                get_api_url(
                    keyword=keyword,
                    start_price=self.start_price,
                    end_price=self.end_price,
                )
            ).json()
            for auction in response["items"]:
                if auction not in formatted_auctions:
                    formatted_auctions.append(
                        self._formatter(
                            auction, search_rule["product_category"], keyword
                        )
                    )
                    raw_auctions.append(auction)
        logger.info("got %s tenders" % len(formatted_auctions))
        return formatted_auctions, raw_auctions

    def parse(self):
        formatted_results = []
        raw_results = []
        for search_rule in self.search_rules:
            results = self.search(search_rule)
            formatted_results += results[0]
            raw_results += results[1]
        return formatted_results, raw_results


if __name__ == "__main__":
    with open("../../data/search_rules.json", encoding="utf-8") as search_rules_file:
        search_rules = json.loads(search_rules_file.read())
    mos = MOS(search_rules)
    results = mos.run()
    print(results)
