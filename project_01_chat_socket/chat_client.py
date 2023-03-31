import socket
import threading

HOST = '192.168.19.60'
PORT = 65432


def recv_msg(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                # print(f"Server: {data.decode('utf-8')}")
                client_address = sock.getpeername()[0]
                print(f"Client {client_address}: {data.decode('utf-8')}")
        except:
            break
def send_msg(sock):
    while True: 
        try:
            msg = input()
            sock.sendall(msg.encode('utf-8'))
        except:
            break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

recv_thread = threading.Thread(target=recv_msg, args=(s,))
recv_thread.start()

send_thread = threading.Thread(target=send_msg, args=(s,))
send_thread.start()

recv_thread.join()
send_thread.join()

s.close()
