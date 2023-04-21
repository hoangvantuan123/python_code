import requests
from bs4 import BeautifulSoup
import streamlit as st


def get_amazon_price(url):
    # Tải trang Amazon
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Tìm giá cả sản phẩm
    price = soup.find('span', {'class': 'a-price-whole'}).text
    decimals = soup.find('span', {'class': 'a-price-fraction'}).text
    return price + '.' + decimals


def main():
    # Hiển thị tiêu đề và mô tả ứng dụng
    st.title('Ứng dụng xem giá cả sản phẩm trên Amazon')
    st.write('Vui lòng nhập link sản phẩm vào ô bên dưới để xem giá cả sản phẩm.')

    # Tính toán giá cả sản phẩm
    url = st.text_input('Nhập link sản phẩm Amazon:')
    if not url.startswith('https://www.amazon.com/'):
        st.warning('Link sản phẩm không hợp lệ!')
    else:
        price = get_amazon_price(url)

        # Hiển thị kết quả
        st.success('Giá sản phẩm: $' + price)


if __name__ == '__main__':
    main()
