from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.newegg.com/p/pl?d=graphics+card'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, 'html.parser')
page_soup__h1 = page_soup.h1
page_soup__p = page_soup.p
containers = page_soup.findAll("div", {"class": "item-container"})

product_length = len(containers)

# Lu file duoi dang csv
filename = "products.csv"
f = open(filename, "w")

headers = "Product_name,Price\n"

f.write(headers)

# print(product_length)
for container in containers:
    title_a = container.find("a", {"class": "item-title"})
    product_name = title_a.text if title_a else "Khong co ten san pham"
    #print("Product: " + product_name)

    price_current = container.find("li", {"class": "price-current"})
    price = price_current.text
    #print("Price: " + price)

    f.write(f"{product_name},{price}\n")

f.close()
