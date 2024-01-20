from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re

html = urlopen(
    "https://www.didigalvao.com.br/cotacao-da-cebola-nesta-sexta-05-em-cabrobo/"
    # "https://www.didigalvao.com.br/cotacao-da-cebola-nesta-sexta-20-no-mercado-do-produtor-em-juazeiro-ba-veja-tambem-outros-produtos/"
)
bs = BeautifulSoup(html, "html.parser")

text = bs.find('div', {'class': 'td-post-content'}).get_text()

print(text)

print("-"*50)

patterns = {"yell_box2": r"(AMARELA CAIXA 2 .{8})",
            "yell_box3": r"(AMARELA CAIXA 3 .{8})",
            "red_box2": r"(ROXA CAIXA 2 .{8})",
            "red_box3": r"(ROXA CAIXA 3 .{8})"}

collection = {"yell_box2": None,
              "yell_box3": None,
              "red_box2": None,
              "red_box3": None}

for key, value in patterns.items():
    data = re.findall(value, text.upper())
    collection[key] = data

collection.update(date=bs.find('span', {'class': 'td-post-date'}).get_text())
print(collection)


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
