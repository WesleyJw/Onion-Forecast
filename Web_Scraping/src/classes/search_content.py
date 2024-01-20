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

    def get_quotation_img(self):
        bs = self.onion_scraper.html_parser()
        try:
            content = bs.find(
                'div', class_='td-post-content').find('a').get('href')
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


if __name__ == "__main__":
    url = "https://www.didigalvao.com.br/cotacao-da-cebola-no-mercado-do-produtor-de-juazeiro-ba-nesta-quinta-feira-13/"
    url = "https://www.didigalvao.com.br/cotacao-da-cebola-nesta-sexta-05-em-cabrobo/"
    search_content = SearchContent(url)
    onion_price = search_content.get_quotation_img()
    # onion_price = re.sub('\n', '', onion_price)
    print(onion_price)
