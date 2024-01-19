from classes import OnionScraper

url = "https://www.didigalvao.com.br/page/1/?s=cota%C3%A7%C3%A3o+cebola"
onion_scraper = OnionScraper(url)

while url:
    print(url)
    # Get list of onion price by week to url page.
    quotations_links = onion_scraper.get_urls_cotation()
    for link in quotations_links:
        print(">>>>>> Cotation-link:", link)
        """text, metadata = po.get_cotation_text(link)
        print(len(text))
        if text:
            result = sp.parse_onion_prices(text, metadata)
            if result is None:
                break
            else:
                sj.price_to_json(result)
            print(result)"""

    # Get next page of onion cotations
    url = onion_scraper.get_page_url()
    break
