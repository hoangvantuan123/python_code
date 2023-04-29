import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from collections import OrderedDict
import io
# Hàm lấy dữ liệu từ trang web


def get_data(url, tags_attributes):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            st.code(soup)
            data_list = []
            # tạo đối tượng data_dict với kiểu dữ liệu là OrderedDict
            data_dict = OrderedDict()
            for tag, attributes in tags_attributes.items():
                for item in soup.find_all(tag, attributes):
                    # Lấy thông tin từng sản phẩm
                    name = item.text.strip()
                    # Thêm thông tin sản phẩm vào danh sách
                    data_dict.setdefault(f"{tag}", []).append(name)

            # Chuyển đổi thành list
            data_list = list(data_dict.values())
            # Đảo ngược thứ tự của các hàng
            data_list = list(zip(*data_list))
            # Trả về danh sách dữ liệu sản phẩm
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
url = st.sidebar.text_input('Nhập đường dẫn URL', key='url')

# Tạo danh sách các thẻ HTML và thuộc tính tương ứng
tag_count = 0
tags_attributes = {}
while True:
    tag_count += 1
    tag = st.sidebar.text_input(
        "Nhập tên thẻ HTML (để trống để dừng)", key=f"tag_{tag_count}")
    if not tag:
        break
    attributes = st.sidebar.text_input(
        f"Nhập thuộc tính của thẻ {tag} (để trống nếu không có)", key=f"attributes_{tag_count}")
    attributes_dict = {}
    if attributes:
        parts = [part.strip() for part in attributes.split(",")]
        for part in parts:
            key_value = part.split(":")
            if len(key_value) < 2:
                st.warning(f"Thuộc tính không đúng định dạng: {part}")
            else:
                key = key_value[0].strip()
                value = key_value[1].strip()
                attributes_dict[key] = value
    tags_attributes[tag] = attributes_dict

# Kiểm tra dữ liệu nhập vào
if url and tags_attributes:
    # Lấy dữ liệu từ trang web
    data = get_data(url, tags_attributes)
    st.code('url: ' + url)
    st.code(tags_attributes)

    # Kiểm tra dữ liệu trả về
    if data:
        # Hiển thị dữ liệu bằng cách tạo bảng trong Streamlit
        st.title('Dữ liệu thu thập được')
        df = pd.DataFrame(data, columns=[f'Item_{i}' for i in range(len(data[0]))])
        st.write(df)
    else:
        st.warning('Không có dữ liệu để hiển thị')

    # Chức năng tải dữ liệu xuống dưới dạng CSV
    def convert_df(df):
        # sử dụng io.StringIO() để tạo một object stramlit có thể ghi vào bộ nhớ đệm như file
        stream = io.StringIO()
        df.to_csv(stream, index=False, encoding="utf-8-sig")
        # sử dụng getValue() để lấy gía trị của stramlit đã được ghi  ra
        # `encoding="utf-8-sig"` để ghi file CSV với định dạng Unicode, bao gồm các ký tự Latin và tiếng Việt.
        # Sử dụng `.encode("utf-8-sig")` để mã hóa Unicode thành nhị phân theo định dạng UTF-8.
        return stream.getvalue().encode("utf-8-sig")

    csv = convert_df(pd.DataFrame(data))

    st.download_button(
        label="Download Data",
        data=csv,
        file_name='data_name.csv',
        mime='text/csv'
    )
else:
    st.warning(
        'Vui lòng nhập đường dẫn URL và các thẻ HTML cùng với các thuộc tính tương ứng để thu thập dữ liệu.')
