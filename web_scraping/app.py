import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

# Tên thành phố và tiểu bang
city_name = input("Nhập tên thành phố: ")
state_code = input("Nhập mã bang: ")

# Tìm toạ độ của thành phố
geolocator = Nominatim(user_agent="weather_app")
location = geolocator.geocode(f"{city_name}, {state_code}")
latitude, longitude = location.latitude, location.longitude

# Tạo URL mới với toạ độ của thành phố
url = f"https://forecast.weather.gov/MapClick.php?lat={latitude:.4f}&lon={longitude:.4f}"

# Gửi yêu cầu HTTP để lấy thông tin thời tiết
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
""" 
Tham số utf-8 được truyền vào prettufy để đảm bảo rằng đoạn mã HTml được mã hoá bằng UTF-8 
Tham số wb được truyền vào hàm open() để mở file và ghi ('b') dùng để ghi đè bất kỳ dữ liệu nào có trong file 
"""
open('index.html', 'wb').write(soup.prettify("utf-8"))

# Trích xuất thông tin thời tiết từ dữ liệu HTML
current_weather = soup.find("div", class_="contentArea")

# In kết quả ra màn hình
print(f"Location: {location}")
print(current_weather)

