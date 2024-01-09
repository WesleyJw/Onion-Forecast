import pages_onion as po
import search_price as sp
import save_json as sj

url = "https://www.didigalvao.com.br/page/1/?s=cota%C3%A7%C3%A3o+cebola"
while url:
    print(url)
    cotations_links = po.get_url_cotation(url)
    for link in cotations_links:
        print(">>>>>> Cotation-link:", link)
        text, metadata = po.get_cotation_text(link)
        print(len(text))
        if text:
            result = sp.parse_onion_prices(text, metadata)
            if result is None:
                break
            else:
                sj.price_to_json(result)
            print(result)
    url = po.get_page_url(url)
    print(url)