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

                # Thêm thông tin sản phẩm vào danh sách
                data_list.append({'name': name})

            return data_list
        else:
            st.error(f"Lỗi {r.status_code}: Không thể kết nối đến đường dẫn URL. Vui lòng kiểm tra lại.")
            return []
    except:
        st.error("Không thể kết nối đến đường dẫn URL. Vui lòng kiểm tra lại.")
        return []

# Hiển thị giao diện nhập URL, tên thẻ HTML và thuộc tính
st.sidebar.title('Thu thập dữ liệu từ trang web')
url = st.sidebar.text_input('Nhập đường dẫn URL')
tag_name = st.sidebar.text_input('Nhập tên thẻ HTML')
attributes = st.sidebar.text_input('Nhập thuộc tính của thẻ HTML')

# Kiểm tra dữ liệu nhập vào
if url and tag_name:
    # Tạo một từ điển chứa các thuộc tính truyền vào
    attributes_dict = {}
    if attributes:
        # Tách chuỗi thuộc tính thành các cặp key-value
        parts = [part.strip() for part in attributes.split(",")]
        for part in parts:
            # Tách key-value thành key và value
            key_value = part.split(":")
            if len(key_value) < 2:
                st.warning(f"Thuộc tính không đúng định dạng: {part}")
            else:
                key = key_value[0].strip()
                value = key_value[1].strip()
                attributes_dict[key] = value

                
    # Lấy dữ liệu từ trang web
    data = get_data(url, tag_name, attributes_dict)

    # Kiểm tra dữ liệu trả về
    if data:
        # Hiển thị dữ liệu bằng cách tạo bảng trong Streamlit
        st.title('Dữ liệu thu thập được')
        st.write(pd.DataFrame(data))
    else:
        st.warning('Không có dữ liệu để hiển thị')
else:
    st.warning('Vui lòng nhập đường dẫn URL, tên thẻ HTML và thuộc tính (nếu có) để thu thập dữ liệu.')
