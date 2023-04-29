import socket
import threading

HOST = '192.168.19.60'
PORT = 65432

# tạo ra hàm handle_clinet để xử lý kết nối từ clinet đến server 
""" 
`client_socket` là socket của client đó, được truyền vào hàm `handle_client` khi một client mới kết nối đến server.
`client_addr` là địa chỉ của client đó (bao gồm địa chỉ IP và số port tương ứng), cũng được truyền vào hàm `handle_client`.
"""
def handle_client(client_socket, client_addr):
    while True:
        try:
            # được sử dụng để nhận dữ liệu từ clinet  thông qua biến với khởi tạo là clinet_socket
            # recv(1024) nếu như vượt quá kích thươcs tối đa 1024 bytes => thì nó sẽ gửi nhiều lần cho đến đến khi hết hoặc báo lỗi 
            
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Client {client_addr}: {data.decode('utf8')} ")
            # Gửi lại tin nhắn cho tất cả các client khác
            for c in clients:
                if c != client_socket:
                    c.sendall(data)
        except:
            break
    print(f"Client {client_addr} disconnected")
    clients.remove(client_socket)
    client_socket.close()


def accept_clients():
    global clients
    while True:
        client_socket, client_addr = s.accept()
        clients.append(client_socket)
        print(f"Client {client_addr} connected")
        t = threading.Thread(target=handle_client,
                             args=(client_socket, client_addr))
        t.start()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print("Server started, waiting for clients to connect...")

clients = []
accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()
accept_thread.join()

s.close()
