import json
from io import StringIO

import pandas

from src import needs
from src import logger


URL = "https://zakupki.gov.ru/epz/order/extendedsearch/orderCsvSettings/download.html?" \
      "searchString={0}&morphology=on&search-filter=Дате+размещениѝ" \
      "&pageNumber=1&sortDirection=false&recordsPerPage=_10" \
      "&showLotsInfoHidden=false&sortBy=UPDATE_DATE&priceFromGeneral={1}" \
      "&fz44=on&fz223=on&af=on&currencyIdGeneral=-1&priceToGeneral={2}" \
      "&customerPlace=5277335&customerPlaceCodes=77000000000" \
      "&gws=Выберите+тип+закупки&OrderPlacementSmallBusinessSubject=on" \
      "&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on" \
      "&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0" \
      "&from=1&to=1&placementCsv=true&registryNumberCsv=true&stepOrderPlacementCsv=true" \
      "&methodOrderPurchaseCsv=true&nameOrderCsv=true&purchaseNumbersCsv=true" \
      "&numberLotCsv=true&nameLotCsv=true&maxContractPriceCsv=true&currencyCodeCsv=true" \
      "&maxPriceContractCurrencyCsv=true&currencyCodeContractCurrencyCsv=true&scopeOkdpCsv=true" \
      "&scopeOkpdCsv=true&scopeOkpd2Csv=true&scopeKtruCsv=true&ea615ItemCsv=true&customerNameCsv=true" \
      "&organizationOrderPlacementCsv=true&publishDateCsv=true&lastDateChangeCsv=true" \
      "&startDateRequestCsv=true&endDateRequestCsv=true&ea615DateCsv=true&featureOrderPlacementCsv=true"


def get_url(keyword: str, start_price: int, end_price: int):
    return URL.format(keyword, start_price, end_price)


class EIS:
    def __init__(self, search_rules: list):
        self.search_rules = search_rules
        self.start_price = 1000
        self.end_price = 300000

    @staticmethod
    def _formatter(tender: list, product_category: str, search_keyword: str):
        return {
            "product_category": product_category,
            "name": tender[3],
            "type": tender[0],
            "link": "https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=%s" % tender[1].replace("№", ''),
            "supplier_definition": tender[2],
            "start_price": int(tender[8]),
            "product_type": tender[14],
            "customer_name": tender[16],
            "start_date": tender[22],
            "end_date": tender[23],
            "preferential_supplier": tender[21],
            "search_keyword": search_keyword
        }


    def parse(self):
        formatted_results = []
        raw_results = []
        for search_rule in self.search_rules:
            for keyword in search_rule["keywords"]:
                logger.info("search by rule '%s' (keyword: '%s')" % (search_rule, keyword))
                response = needs.requester(
                    get_url(keyword, self.start_price, self.end_price)
                )
                csv_stringio = StringIO(response.text)
                df = pandas.read_csv(csv_stringio, sep=';')
                raw = df.to_dict('records')
                if raw not in raw_results:
                    raw_results.append(raw)
                for tender in df.values:
                    tender = list(tender)
                    if tender not in formatted_results:
                        formatted_results.append(self._formatter(tender, search_rule["product_category"], keyword))
        logger.info("got %s tenders" % len(formatted_results))
        return formatted_results, raw_results


if __name__ == '__main__':
    with open("../../data/search_rules.json", encoding="utf-8") as search_rules_file:
        search_rules = json.loads(search_rules_file.read())

    eis = EIS(search_rules)
    res = eis.search()
    print(json.dumps(res[0]))