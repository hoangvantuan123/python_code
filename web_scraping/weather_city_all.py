import urllib.request
import urllib.parse
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup as soup
import csv 

with open('uscities.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # skip header

    for row in reader:
        city, state_id = row[0] , row[1]
        # Tìm toạ độ của thành phố
        try:
            # khởi tạo một đối tượng Nominatim 
            geolocator = Nominatim(user_agent="weather_app")
            location = geolocator.geocode(f"{city}, {state_id}") # Tìm kiếm toạ độ theo địa chỉ nhập
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

        # Solution #2
        page_soup = soup(content, 'html.parser')
        try:
            
            div_page_city = page_soup.find('div' , {'id': 'seven-day-forecast'})
            div_page_city_div = div_page_city.find('div',{'class': 'panel-heading'}) 
            h2_page = div_page_city_div.find('h2', {'class': 'panel-title'}).text.strip()
            print(h2_page)
        except:
            h2_page ='N/A'
        # dùng find_next_sibling() đây là một phương thức được sử dụng để tìm phần tử kế tiếp trong danh sách
        try:
            humidity = page_soup.find('td', text='Humidity').find_next_sibling('td').text
        except AttributeError:
            humidity = 'N/A'

        try:
            wind_speed = page_soup.find('td', text='Wind Speed').find_next_sibling('td').text
        except AttributeError:
            wind_speed = 'N/A'

        try:
            barometer = page_soup.find('td', text='Barometer').find_next_sibling('td').text
        except AttributeError:
            barometer = 'N/A'

        try:
            dewpoint = page_soup.find('td', text='Dewpoint').find_next_sibling('td').text
        except AttributeError:
            dewpoint = 'N/A'

        try:
            visibility = page_soup.find('td', text='Visibility').find_next_sibling('td').text
        except AttributeError:
            visibility = 'N/A'

        try:
            last_update = page_soup.find('td', text='Last update').find_next_sibling('td').text.strip()
        except AttributeError:
            last_update = 'N/A'


        print('Humidity:', humidity)
        print('Wind Speed:', wind_speed)
        print('Barometer:', barometer)
        print('Dewpoint:', dewpoint)
        print('Visibility:', visibility)
        print('Last update:', last_update)