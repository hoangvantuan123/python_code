import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

# Hàm lấy dữ liệu từ trang web


def get_data(url, tag_name, attributes):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            data_list = []

            for item in soup.find_all(tag_name, attributes):
                # Lấy thông tin từng sản phẩm
                name = item.text.strip()
                href = item.get('href')

                # Thêm thông tin sản phẩm vào danh sách
                data_list.append({'name': name, 'href': href})

            return data_list
        else:
            st.error(
                f"Lỗi {r.status_code}: Không thể kết nối đến đường dẫn URL. Vui lòng kiểm tra lại.")
            return []
    except:
        st.error("Không thể kết nối đến đường dẫn URL. Vui lòng kiểm tra lại.")
        return []


# Hiển thị giao diện nhập URL, tên thẻ HTML và thuộc tính
st.sidebar.title('Thu thập dữ liệu từ trang web')
url = st.sidebar.text_input('Nhập đường dẫn URL')
# Nhập nhiều tag name
# slider để nhập số lượng thuộc tính HTML
n_tag_names = st.sidebar.slider('Số lượng tag name', 1, 10, 1)
tag_names = []
for i in range(n_tag_names):
    tag = st.sidebar.text_input(f'Nhập tag name {i+1}')
    if tag:
        tag_names.append(tag)

# Nhập nhiều thuộc tính HTML
# slider để nhập số lượng thuộc tính HTML
n_attrs = st.sidebar.slider('Số lượng thuộc tính', 1, 10, 1)
attributes = []
for i in range(n_attrs):
    attr = st.sidebar.text_input(f'Nhập thuộc tính HTML {i+1}')
    if attr:
        attributes.append(attr)

# Kiểm tra dữ liệu nhập vào
if url and tag_names:
    # Tạo một danh sách các thông tin tìm kiếm
    searches = []
    for tag_name in tag_names:
        # Tạo một từ điển chứa các thuộc tính truyền vào
        attributes_dict = {}
        for attr in attributes:
            # Tách thuộc tính thành tên class
            try:
                key, val = attr.split(":")
                attributes_dict[key.strip()] = val.strip()
            except:
                st.warning(f"Không thể tách thuộc tính HTML: {attr}")

        # Tạo một từ điển chứa thông tin tìm kiếm
        search = {'tag_name': tag_name.strip(
        ), 'attributes_dict': attributes_dict}
        searches.append(search)

    # Lấy dữ liệu từ trang web
    data = []
    for search in searches:
        search_data = get_data(
            url, search['tag_name'], search['attributes_dict'])
        if search_data:
            data.extend(search_data)

    # Kiểm tra dữ liệu trả về
    if data:
        # Hiển thị dữ liệu bằng cách tạo bảng trong Streamlit
        st.title('Dữ liệu thu thập được')
        df = pd.DataFrame(data, columns=['name', 'href'])  # thêm tên cột 'href'
        st.write(df)
    else:
        st.warning('Không có dữ liệu để hiển thị')
else:
    st.warning('Vui lòng nhập đường dẫn URL và tag name để thu thập dữ liệu.')
