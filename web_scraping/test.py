from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.newegg.com/p/pl?Submit=StoreIM&Depa=3&PageSize=96'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()


page_soup = soup(page_html, 'html.parser')
page_results = page_soup.findAll(
    'div', {'class': 'item-cell'})

# print(len(page_results))
containers = page_results
# print(page_results)
# print(containers)


if containers:
    for container in containers:
        item_brand = container.find('a', {'class': 'item-brand'})
        if item_brand:
            item = item_brand.img['title']
            print('item: ' + item)
        else:
            print('Brand not found')
        item_title = container.find('div', {'class': 'item-title'})
        title = item_title.text if item_title else "Khong co ten san pham"
        print('title: ' + title)
        price_ship = container.find('div', {'class': 'price-ship'})
        ship = price_ship.text if price_ship else "Khong free ship"
        print()
        price_current = container.find('div', {'class': 'price-current'})
        price = price_current.strong


else:
    print('No containers found.')
