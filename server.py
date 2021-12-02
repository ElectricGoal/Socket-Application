from socket import AF_INET, socket, SOCK_STREAM
import socket as sk
from threading import Thread
import tkinter as tk
import api_network as api
import pickle
import time

def accept_incoming_connections():
    '''Sets up handling for incoming clients'''
    try:
        while True:
            #Lấy thông tin kết nối của client
            client, client_address = SERVER.accept()

            #In thông tin của client lên màn hình console và màn hình giao diện của server
            client_connected = "%s:%s has connected." % client_address
            server_app.insertMsg(client_connected)
            print("%s:%s has connected." % client_address)
            
            #Gửi lời chào mừng tới client
            client.send(
                bytes("Greetings from server! Now type your name and press enter!", FORMAT))
            
            #Bắt đầu tiến trình giao tiếp với client
            Thread(target=handle_client, args=(client,)).start()
    except:
        #Trường hợp server bị lỗi
        print("Error")


#Takes client socket as argument
def handle_client(client):
    '''Handles a single client connection'''

    #Nhận tên {name} của client
    name = client.recv(BUFSIZ).decode(FORMAT)
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name

    #Server gửi {welcome} tới client
    client.send(bytes(welcome, FORMAT))

    #Khởi tạp biến {msg} dùng trong giao tiếp giữa server vs client
    msg = None
    
    #Nếu server nhận {quit} thì ngắt kết nối tới client
    while msg != "{quit}":
        try:
            msg = client.recv(BUFSIZ).decode(FORMAT)

            if msg != bytes("{quit}", FORMAT):
                client.send(bytes(msg, FORMAT))
            
            #In ra màn hình console server {msg} của client gửi tới server
            print(name, ': ', msg)

            # if msg == "USD to VND":
            #     client.send(bytes("=> USD to VND: 23", FORMAT))

            reply = api.find_currency(msg)
            
            if (len(reply) == 5):
                client.send(bytes("tsillist", FORMAT))
                data_send = pickle.dumps(reply)
                client.send(data_send)
            # for item in reply:
            #     print(item)
            #     client.send(bytes(item, FORMAT))
            

        except:
            '''Phát hiện client ngắt kết nối tới server'''
            msg = "Unable to connect to " + name
            
            #Chèn message vào Listbox tkinter
            server_app.insertMsg(msg)
            break
    
    #Client đóng
    client.close()

def countdown(t):
    '''Hàm đếm thời gian'''
    while t: # while t > 0 for clarity 
      time.sleep(1)
      t -= 1

def updateData():
    '''Upadate data mới sau mỗi 30 phút'''

    #Lúc bắt đầu khởi động, lấy data về
    api.getDataFromAPI()

    while True:
        #Đếm ngược 30 phút
        countdown(1800)

        #Lấy data mới
        api.getDataFromAPI()


class ServerApp(tk.Tk):
    '''
    Server application: Giao diện server sử dụng tkinter
    Hiện lên các thông báo về kết nối của client
    '''
    def __init__(self):
        tk.Tk.__init__(self)

        #Khởi tạo khung của cửa sổ server
        self.title("Server")
        self.geometry("400x600")
        self.resizable(width=False, height=False)
        
        #Lấy thông tin {hostname} và {ip_address} của thiết bị sử dụng làm server
        hostname = sk.gethostname()
        ip_address = sk.gethostbyname(hostname)
        
        #In ra màn hình giao diện của server
        hostname_label = tk.Label(self, text=f"Hostname: {hostname}")
        ip_address_label = tk.Label(self, text=f"IP Address: {ip_address}")
        hostname_label.pack()
        ip_address_label.pack()

        #Khởi tạo Listbox hiển thị thông tin client thông qua {server_list}
        self.server_list = tk.Listbox(self)
        self.server_list.pack(side = tk.LEFT, fill = tk.BOTH, expand=True)
        
        #Khởi tạo thanh trượt
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack()

        scrollbar.config(command = self.server_list.yview)
        self.server_list.config(yscrollcommand = scrollbar.set)
        
        
    #Nhận {msg} làm argument
    #{msg} là một string message
    def insertMsg(self, msg):
        '''Chèn {msg} vào Listbox'''
        self.server_list.insert(tk.END, msg)

# --------------------------------------------MAIN---------------------------------------------------
if __name__ == "__main__":
    #Khởi tạo các biến cần thiết
    HOST = ''
    PORT = 33000
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    FORMAT = "utf8"
    ip_address = ""
    
    #Khởi động server
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(5)

    DATA_THREAD = Thread(target=updateData)
    DATA_THREAD.start()
    
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.daemon = True
    ACCEPT_THREAD.start()
    
    #Khởi động giao diện server
    server_app = ServerApp()
    server_app.mainloop()
    
    SERVER.close()

