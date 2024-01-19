from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import json
import datetime

from pages_onion import OnionScraper


class SearchContent:

    def __init__(self, url):
        self.url = url
        self.onion_scraper = OnionScraper(url)

    def get_quotation_text(self):
        bs = self.onion_scraper.html_parser()
        try:
            content = bs.find('div', {'class': 'td-post-content'}).get_text()
            return content
        except Exception as e:
            print(e)
            return None

    def get_metadata(self):
        bs = self.onion_scraper.html_parser()
        try:
            metadata = bs.find(
                'span', {'class': 'td-post-date'}).get_text()
            return metadata
        except Exception as e:
            print(e)
            return None

    def parse_onion_prices(self):

        text = self.get_quotation_text()
        metadata = self.get_metadata()
        result = {}
        pattern1 = r'(CEBOLA\sPERA|CEBOLA\sROXA):\sCaixa\s3\s–\sR\$\s([\d\.,]+)\se\sCaixa\s2\s–\sR\$\s([\d\.,]+)'
        pattern3 = r'(\bCEBOLAS\b\s(?:PERA|ROXA)):\s(?:Caixa\s3|R\$70,00)\sR\$(\d+\,\d{2})\se\s(?:Caixa\s2|R\$50,00|R\$65,00)\sR\$(\d+\,\d{2})'
        pattern2 = r'\bCEBOLAS?\s+(PERA|ROXA)\b:\s*Caixa 3 R\$(\d+,\d+)\s*e\s*Caixa 2 R\$(\d+,\d+)'

        matches = re.findall(pattern1, text)

        if not matches:
            matches = re.findall(pattern2, text)
        if not matches:
            return None

        for match in matches:
            onion_type = match[0]
            price_caixa_3 = match[1]
            price_caixa_2 = match[2]

            if (match[0] == "PERA") or (match[0] == "ROXA"):
                onion_type = "CEBOLA " + match[0]

            else:
                onion_type = match[0]

            result[onion_type] = {
                "Caixa 3": f"R$ {price_caixa_3}",
                "Caixa 2": f"R$ {price_caixa_2}"
            }

        result.update(price_dt=metadata)
        result.update(
            ingestion_dt=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

        return result


if __name__ == "__main__":
    url = "https://www.didigalvao.com.br/cotacao-da-cebola-no-mercado-do-produtor-de-juazeiro-ba-nesta-quinta-feira-13/"
    url = "https://www.didigalvao.com.br/cotacao-da-cebola-nesta-sexta-05-em-cabrobo/"
    search_content = SearchContent(url)
    onion_price = search_content.get_quotation_text()
    onion_price = re.sub('\n', '', onion_price)
    print(len(onion_price))


# Parse the examples using regex
"""if __name__ == "__main__":
    html = urlopen(
        # "https://www.didigalvao.com.br/cotacao-da-cebola-nesta-sexta-05-em-cabrobo/"
        # "https://www.didigalvao.com.br/cotacao-da-cebola-nesta-quinta-30-no-ceasa-de-belem-do-sao-francisco/"
        "https://www.didigalvao.com.br/cotacao-da-cebola-no-mercado-do-produtor-de-juazeiro-ba-nesta-quinta-feira-13/"
        # "https://www.didigalvao.com.br/cotacao-da-cebola-nesta-sexta-feira-25-03-no-mercado-do-produtor-em-juazeiro-ba/"
        # "https://www.didigalvao.com.br/cotacao-da-cebola-nesta-sexta-20-no-mercado-do-produtor-em-juazeiro-ba-veja-tambem-outros-produtos/"
    )
    bs = BeautifulSoup(html, "html.parser")
    text = bs.find('div', {'class': 'td-post-content'}).get_text()
    metadata = bs.find(
        'span', {'class': 'td-post-date'}).get_text()

    # Define pattern for onion prices
    pattern = r'(CEBOLA\s+(?:PERA|AMARELA|ROXA)):\s+Caixa\s+3\s+R\$(\d+,\d+\.\d+|\d+)\s+e\s+Caixa\s+2\s+R\$(\d+,\d+\.\d+|\d+)'
    pattern = r'(CEBOLAS? (PERA|AMARELA|ROXA)):\s+Caixa\s+3\s+R\$(\d+,\d+\.\d+|\d+)\s+e\s+Caixa\s+2\s+R\$(\d+,\d+\.\d+|\d+)'
    pattern = r'\bCEBOLAS?\b (PERA|ROXA):\s*Caixa 3 R\$(\d+,\d+)\s*e\s*Caixa 2 R\$(\d+,\d+)'
    # Define pattern for CEBOLA or CEBOLAS
    pattern = r'\bCEBOLAS?\b'

    # Find all matches of the pattern in the text
    matches = re.findall(pattern, "I want one CEBOLA and two CEBOLAS.")

    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)
    print(matches)
    print(text)

    parsed_example_1 = parse_onion_prices(text, metadata)
    print(parsed_example_1)"""
