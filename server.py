from socket import AF_INET, socket, SOCK_STREAM
import socket as sk
from threading import Thread
import tkinter as tk
import server_components as svc
import pickle
import time
from datetime import datetime


def accept_incoming_connections():
    '''Sets up handling for incoming clients'''
    try:
        while True:
            # Lấy thông tin kết nối của client
            client, client_address = SERVER.accept()

            # In thông tin của client lên màn hình console và màn hình giao diện của server
            client_connected = "%s:%s has connected." % client_address
            server_app.insertMsg(client_connected)
            print("%s:%s has connected." % client_address)

            # Bắt đầu tiến trình giao tiếp với client
            # Cài đặt user_name tại đây, sau khi phần đăng nhập hoặc đăng kí kết thúc
            # có thể dùng 1 hàm để truyền {user_name} ngay tại đây
            user_name = "B"
            Thread(target=handle_client, args=(client, user_name)).start()
    except:
        # Trường hợp server bị lỗi
        print("Error")


# Takes client socket as argument
def handle_client(client, name):
    '''Handles a single client connection'''

    welcome = '    Welcome %s! Please read the Instruction and tell me your requests' % name

    # Server gửi {welcome} tới client
    client.send(bytes(welcome, FORMAT))

    # Khởi tạp biến {msg} dùng trong giao tiếp giữa server vs client
    msg = None
    
    # Khởi tạo biến {date} để lưu ngày tháng hiện tại làm giá trị default
    date = datetime.now().strftime("%d/%m/%Y")

    while True:
        try:
            # Nhận tin nhắn từ client
            msg = client.recv(BUFSIZ).decode(FORMAT)

            # In ra màn hình console server {msg} của client gửi tới server
            # Dùng để check, có thể xoá sau khi hoàn thành
            print(name, ': ', msg)
            
            # Kiểm tra tin nhắn vừa nhận có phải là ngày tháng ko
            # Nếu có thì {date = msg} và gửi tin nhắn tới client
            if (svc.is_date(msg)):
                date = msg
                set_date_msg = "   Set date: %s" %date
                client.send(bytes(set_date_msg, FORMAT))
                continue
            
            # Tạo độ delay cho server để cho giống một đoạn chat thật
            time.sleep(0.7)

            # Kiểm tra tin nhắn vừa được gửi tới có phải là "history" ko
            if msg.lower() == "history":
                # Nếu có thì gửi tin nhắn này tới client
                # để cho client chuẩn bị nhận thông tin lịch sử người dùng
                client.send(bytes("yrotsih", FORMAT))

                # Tìm kiếm lịch sử người dùng thông qua tên người dùng {name}
                history_data = svc.findUserHistory(name)

                # {history_data} có kiểu list bao gồm nhiều list khác nhau
                # Vd: history_data = [[data1, data2, data3], [data4, data5, data6], [data7, data8, data9]]

                # Bắt đầu gửi user history data tới client
                for item in history_data:
                    # Dùng pickle để gửi data kiểu list tới người dùng
                    data_send = pickle.dumps(item)
                    client.send(data_send)
                    
                    # Nhận tin nhắn từ client để biết đã gửi thành công và tránh lỗi xảy ra
                    client.recv(BUFSIZ).decode(FORMAT)
                # Gửi tới client tin nhắn thông báo kết thúc quá trình
                client.send(bytes("end", FORMAT))

            else:
                # Tìm dữ liệu trong thời điểm mà user yêu cầu thông qua biến {date}
                # và {msg}, trong đó msg nếu như đúng là mã tiền tệ (ex: USD) còn
                # date là ngày tháng
                reply_dict = svc.find_currency(msg, date)
                
                # Kiểm tra nếu như không có dữ liệu thì gửi tin nhắn như dưới tới client
                if (reply_dict == {}):
                    client.send(bytes("   Sorry, I can't fulfill this request :(", FORMAT))

                # Trường hợp có dữ liệu
                elif (reply_dict):
                    # Gửi tin nhắn này tới client để cho client chuẩn bị nhận thông tin user yêu cầu
                    client.send(bytes("tsillist", FORMAT))

                    #Chuyển đổi từ dạng dictionary sang list để có thể gửi tới client
                    # {reply_dict} có kiểu dictionary
                    # {reply} có kiểu list
                    reply = svc.dictToDataSendClient(reply_dict)

                    # Kiểm tra, có thể xoá khi hoàn thành
                    print(reply)

                    # Lưu data vừa lấy được vào lịch sử người dùng
                    svc.saveUserHistory(name, reply_dict)

                    # Gửi data tới client
                    data_send = pickle.dumps(reply)
                    client.send(data_send)
                else:
                    # Trường hợp xảy ra lỗi ngoài ý muốn
                    client.send(bytes("   Something went wrong!", FORMAT))

        except:
            '''Phát hiện client ngắt kết nối tới server'''
            msg = "Unable to connect to " + name

            # Chèn message vào Listbox tkinter
            server_app.insertMsg(msg)
            break

    # Client đóng
    client.close()


def countdown(t):
    '''Hàm đếm thời gian'''
    while t:  # while t > 0 for clarity
        time.sleep(1)
        t -= 1


def updateData():
    '''Upadate data mới sau mỗi 30 phút'''

    # Lúc bắt đầu khởi động, lấy data về
    svc.getDataFromAPI()

    while True:
        # Đếm ngược 30 phút
        countdown(1800)

        # Lấy data mới
        svc.getDataFromAPI()


class ServerApp(tk.Tk):
    '''
    Server application: Giao diện server sử dụng tkinter
    Hiện lên các thông báo về kết nối của client
    '''

    def __init__(self):
        tk.Tk.__init__(self)

        # Khởi tạo khung của cửa sổ server
        self.title("Server")
        self.geometry("400x600")
        self.resizable(width=False, height=False)

        # Lấy thông tin {hostname} và {ip_address} của thiết bị sử dụng làm server
        hostname = sk.gethostname()
        ip_address = sk.gethostbyname(hostname)

        # In ra màn hình giao diện của server
        hostname_label = tk.Label(self, text=f"Hostname: {hostname}")
        ip_address_label = tk.Label(self, text=f"IP Address: {ip_address}")
        hostname_label.pack()
        ip_address_label.pack()

        # Khởi tạo Listbox hiển thị thông tin client thông qua {server_list}
        self.server_list = tk.Listbox(self)
        self.server_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Khởi tạo thanh trượt
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack()

        scrollbar.config(command=self.server_list.yview)
        self.server_list.config(yscrollcommand=scrollbar.set)

    # Nhận {msg} làm argument
    # {msg} là một string message
    def insertMsg(self, msg):
        '''Chèn {msg} vào Listbox'''
        self.server_list.insert(tk.END, msg)


# --------------------------------------------MAIN---------------------------------------------------
if __name__ == "__main__":
    # Khởi tạo các biến cần thiết
    HOST = ''
    PORT = 33000
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    FORMAT = "utf8"
    ip_address = ""

    # Khởi động server
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(5)

    DATA_THREAD = Thread(target=updateData)
    DATA_THREAD.start()

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.daemon = True
    ACCEPT_THREAD.start()

    # Khởi động giao diện server
    server_app = ServerApp()
    server_app.mainloop()

    SERVER.close()
