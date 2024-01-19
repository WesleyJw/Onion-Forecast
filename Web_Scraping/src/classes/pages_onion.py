# This get the link pages that store cotation onion links

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup


class OnionScraper():
    def __init__(self, url):
        self.url = url

    def html_parser(self):
        try:
            html = urlopen(self.url)
        except (HTTPError, URLError) as e:
            print(e)
        else:
            if html is None:
                print("Page empty!")
                return None
            else:
                return BeautifulSoup(html, "html.parser")

    def get_page_url(self):
        # Get the pages links
        bs = self.html_parser()
        current = bs.find('span', {'class': 'current'}).get_text()
        title = str(int(current) + 1)
        try:
            next_page = bs.find('a', {'title': title}).attrs['href']
        except AttributeError:
            next_page = ""
        return next_page

    def get_urls_quotation(self):
        # Get the cotations links
        try:
            bs = self.html_parser()
            content = bs.find_all(
                'h3', {'class': 'entry-title td-module-title'})
            url_quotations = [url.find('a', href=True)['href']
                              for url in content]
            return url_quotations
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    url = "https://www.didigalvao.com.br/page/1/?s=cota%C3%A7%C3%A3o+cebola"
    onion_scraper = OnionScraper(url)
    while url:
        print(url)
        cotations_links = onion_scraper.get_urls_quotation()
        print(cotations_links)
        # for link in cotations_links:
        #    text, metadata = onion_scraper.get_cotation_text()
        #    print(metadata)
        #    break
        url = onion_scraper.get_page_url()
        break
