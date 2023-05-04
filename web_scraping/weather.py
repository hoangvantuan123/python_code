#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 10 - weather.py
# Fetch the weather forecast from the National Weather Service.

import sys
import urllib
import urllib.request
import urllib.error
import urllib.parse
import lxml.etree
from lxml.cssselect import CSSSelector
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup as soup

""" 
#Đang bị lõi vì không gửi đc yêu cầu đến trang cần gửi thiếu toạ đoạ vị trí
#thành phố.
if len(sys.argv) < 2:
    print('usage: weather.py CITY, STATE', file=sys.stderr)
    exit(2)

data = urllib.parse.urlencode({'inputstring': ' '.join(sys.argv[1:])})
data = data.encode('ascii')
info = urllib.request.urlopen('http://forecast.weather.gov/zipcity.php', data)
content = info.read() """

# Tên thành phố và tiểu bang
city_name = input("Nhập tên thành phố: ")
state_code = input("Nhập mã bang: ")

# Tìm toạ độ của thành phố
try:
    # khởi tạo một đối tượng Nominatim 
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(f"{city_name}, {state_code}") # Tìm kiếm toạ độ theo địa chỉ nhập
    # print ra toạ độ kinh độ , vĩ đỗ của địa chỉ vừa mới nhập.
    latitude, longitude = location.latitude, location.longitude
except AttributeError:
    print('Không tìm thấy địa điểm thành phố. Vui lòng kiểm tra lại tên thành phố và mã bang đã nhập!')

# Tạo URL mới với toạ độ của thành phố
#.4f được sử dụng để định dạng các giá trị số thập phân của latitude và longitude với độ chính xác đến 4 chữ số sau dấu phẩy.
url = f"https://forecast.weather.gov/MapClick.php?lat={latitude:.4f}&lon={longitude:.4f}"
response = urllib.request.urlopen(url)
content = response.read()

# Ghi sang 1 file
#open('weather_file_page.html', 'wb').write(content)
#print(content)


""" # Solution #1

# Hiênj tại thì không có class nào tên là big trong tệp HTML này 
# Cùng với hiện giờ là phần tử đầu tiên trong td không phải là phần tử chứa độ ẩm mà là chứa thông tin độ âme
parser = lxml.etree.HTMLParser(encoding='utf-8')
tree = lxml.etree.fromstring(content, parser)
big = CSSSelector('td.big')(tree)[0]
if big.find('font') is not None:
    big = big.find('font')
print('Condition:', big.text.strip())
print('Temperature:', big.findall('br')[1].tail)
tr = tree.xpath('.//td[b="Humidity"]')[0].getparent()
print('Humidity:', tr.findall('td')[1].text)
print() """

# Solution #1
parser = lxml.etree.HTMLParser(encoding='utf-8')
tree = lxml.etree.fromstring(content, parser)
big = CSSSelector('td.text-right')(tree)[0]
# lấy thẻ b
b_big_text = big.find('b')
#print(b_big_text.text)

humid_td = tree.xpath('//td[b="Humidity"]')[0]  # Tìm đến phần tử td có chứa văn bản "Humidity"
humid = humid_td.getnext().text  # Lấy phần tử td tiếp theo

# Lấy phần tử td chứa thông tin tốc độ gió
wind_speed_element = tree.xpath("//td[b='Wind Speed']")[0]
# c1 
wind_speed_value = wind_speed_element.getnext().text 
#C2
#wind_speed_value = wind_speed_element.xpath("./following-sibling::td")[0].text

# Lấy phần tử td chứa thông tin áp suất khí quyển
barometer_element = tree.xpath("//td[b='Barometer']")[0]
barometer_value = barometer_element.xpath("./following-sibling::td")[0].text

print('Humidity:', humid)
print('Wind Speed:', wind_speed_value)
print('Barometer:' , barometer_value)

print('_________________')



# Solution #2
page_soup = soup(content, 'html.parser')

# dùng find_next_sibling() đây là một phương thức được sử dụng để tìm phần tử kế tiếp trong danh sách
humidity = page_soup.find('td', text='Humidity').find_next_sibling('td').text
wind_speed = page_soup.find('td', text='Wind Speed').find_next_sibling('td').text
barometer = page_soup.find('td', text='Barometer').find_next_sibling('td').text
dewpoint = page_soup.find('td', text='Dewpoint').find_next_sibling('td').text
visibility = page_soup.find('td', text='Visibility').find_next_sibling('td').text
last_update = page_soup.find('td', text='Last update').find_next_sibling('td').text.strip()

print('Humidity:', humidity)
print('Wind Speed:', wind_speed)
print('Barometer:', barometer)
print('Dewpoint:', dewpoint)
print('Visibility:', visibility)
print('Last update:', last_update)