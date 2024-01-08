from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import json
import datetime


def parse_onion_prices(text, metadata):
    result = {}
    pattern = r'(CEBOLA\sPERA|CEBOLA\sROXA):\sCaixa\s3\s–\sR\$\s([\d\.,]+)\se\sCaixa\s2\s–\sR\$\s([\d\.,]+)'

    matches = re.findall(pattern, text)
    for match in matches:
        onion_type = match[0]
        price_caixa_3 = match[1]
        price_caixa_2 = match[2]

        result[onion_type] = {
            "Caixa 3": f"R$ {price_caixa_3}",
            "Caixa 2": f"R$ {price_caixa_2}"
        }

    result.update(price_dt=metadata)
    result.update(
        ingestion_dt=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    return result


# Parse the examples using regex
if __name__ == "__main__":
    html = urlopen(
        # "https://www.didigalvao.com.br/cotacao-da-cebola-nesta-sexta-05-em-cabrobo/"
        "https://www.didigalvao.com.br/cotacao-da-cebola-nesta-sexta-20-no-mercado-do-produtor-em-juazeiro-ba-veja-tambem-outros-produtos/"
    )
    bs = BeautifulSoup(html, "html.parser")
    text = bs.find('div', {'class': 'td-post-content'}).get_text()
    metadata = bs.find(
        'span', {'class': 'td-post-date'}).get_text()

    parsed_example_1 = parse_onion_prices(text, metadata)
    print(parsed_example_1)
