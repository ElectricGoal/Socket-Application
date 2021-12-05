from socket import socket
import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
from tkcalendar import DateEntry

class ChatPage(tk.Frame):
    '''Màn hình chat của client'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        # Background của giao diện
        bg = "aliceblue"

        # For the messages to be sent.
        self.my_msg = tk.StringVar()  
        self.my_msg.set("Type your messages here.")
        
        # Frame bên trái màn hình
        left_frame = tk.Frame(self, width=400, bg = bg)
        left_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        # Frame bên phải màn hình
        right_frame = tk.Frame(self, width=300, bg = bg)
        right_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        # Frame phần khung chat
        msg_frame = tk.Frame(left_frame)
        msg_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ô hiện tin nhắn và thanh trượt
        scrollbar = tk.Scrollbar(msg_frame, orient="vertical")
        self.msg_list = tk.Listbox(msg_frame, width=50, height=20, bg='light yellow', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.msg_list.yview)

        scrollbar.pack(side= tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill= tk.BOTH, expand=True)
        
        # Ô chat tin nhắn
        entry_field = tk.Entry(left_frame, textvariable=self.my_msg)
        entry_field.pack(fill=tk.BOTH, pady=2, padx=3)
        
        # Nút gửi tin nhắn
        send_button = tk.Button(left_frame, text="Send", command=self.send, background= "cornflowerblue", fg = "ghostwhite")
        send_button.pack(fill=tk.BOTH, pady=2, padx=3)
        
        # Phần Date picker
        date_label = tk.Label(right_frame, text= "Date picker", foreground="navy", bg = bg)
        self.cal = DateEntry(right_frame, width= 16, background= "cornflowerblue", foreground= "ghostwhite",bd=2, date_pattern='dd/mm/y')
        date_label.pack(pady=5)
        date_label.config(font=("Arial", 12))
        self.cal.pack(pady=1)
        tk.Button(right_frame, text = "Get Date", bg = "cornflowerblue", fg = "ghostwhite", command = self.grad_date).pack(pady=(5, 25))
        
        # Phần Instruction
        instruction_label = tk.Label(right_frame, text= "Instruction", foreground="navy", bg=bg)

        instruction_text = "- Enter the currency code you want to\nexchange to VND (ex: USD, JPY, AUD,...)\n\n- Enter \"history\" if you want to see your\nrequests history\n\n-To find the exchange rate of a particular\ndate, you need to change the date in Date\npicker section and press the \"Get Date\"\nbutton. The default date value is today"

        instruction_label.pack(fill=tk.BOTH)
        instruction_label.config(font=("Arial", 12))
        tk.Label(right_frame, text=instruction_text, anchor='w', justify= tk.LEFT, bg = bg).pack()
        
        # Nút thoat chương trình
        tk.Button(right_frame, text = "Quit", command = self.on_closing, bg="red", fg="white").pack(anchor="se", side=tk.BOTTOM, pady=2, padx=2)


    def grad_date(self):
        '''Gửi ngày tháng tới server'''
        date = self.cal.get_date().strftime("%d/%m/%Y")
        client_socket.send(bytes(date, "utf8"))

    # event is passed by binders.
    def send(self):  
        """Handles sending of messages."""
        msg = self.my_msg.get()

        # Clears input field.
        self.my_msg.set("") 
        self.msg_list.insert(tk.END, " [YOU]: %s" %msg)
        client_socket.send(bytes(msg, FORMAT))
            
            
    def on_closing(self):
        """This function is to be called when the window is closed."""
        client_socket.close()
        self.quit()
        quit()

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                # Nhận tin nhắn từ server
                msg = client_socket.recv(BUFSIZ).decode(FORMAT)
                
                # Phát hiện server đang muốn gửi thông tin user history
                if msg == "yrotsih":
                    # Chèn vào khung chat
                    self.msg_list.insert(tk.END, " [SERVER]: ")
                    while True:
                        # Nhận tin nhắn từ server
                        msg = client_socket.recv(BUFSIZ)

                        if (msg == b'Empty'):
                            self.msg_list.insert(tk.END, "   Empty :v")
                            break

                        # Phát hiện kết thúc
                        if (msg == b'end'):
                            break

                        # Chuyển đổi data bằng pickle và chèn lên khung chat
                        data_recv = pickle.loads(msg)
                        for item in data_recv:
                            self.msg_list.insert(tk.END, item)
                        client_socket.send(bytes("sc", FORMAT))
                    continue
                
                # Phát hiện server đang muốn gửi thông tin currency code user yêu cầu
                if msg == "tsillist":
                    # Nhận tin nhắn từ server
                    msg = client_socket.recv(BUFSIZ)

                    # Chuyển đổi data bằng pickle và chèn lên khung chat
                    data_recv = pickle.loads(msg)
                    self.msg_list.insert(tk.END, " [SERVER]: ")
                    for item in data_recv:
                        self.msg_list.insert(tk.END, item)
                # Trường hợp khác
                else:
                    print("Msg: ", msg)
                    self.msg_list.insert(tk.END, " [SERVER]: ")
                    self.msg_list.insert(tk.END, msg)

            # Possibly client has left the chat.
            except OSError:  
                break

class EnterIpPage(tk.Frame):
    '''Màn hình nhập Ip của server'''
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)
        
        #Khởi tạo dòng chữ "ENTER IP SERVER"
        label_title = tk.Label(self, text="ENTER IP SERVER")

        #Khởi tạo ô để nhập Ip
        self.entry_IP = tk.Entry(self, width=20, bg='light yellow')

        #Khởi tạo Nút Enter
        enterIP_button = tk.Button(self, text="Enter",
                                   command=lambda: appController.connectToServer(self.entry_IP.get()),)
        enterIP_button.configure(width=10)

        label_title.pack()
        self.entry_IP.pack()
        enterIP_button.pack()

class UnableToConnectToServerPage(tk.Frame):
    '''Màn hình khi kết nối lỗi'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        #Khởi tạo dòng chữ trên giao diện
        label_title = tk.Label(self, text="Unable to connect to server !")
        label_title.config(font=("Times New Roman", 40))
        label_title.pack()

class ClientApp(tk.Tk):
    '''
    Client application: Giao diện client sử dụng tkinter
    '''
    def __init__(self):
        tk.Tk.__init__(self)
        
        #Khởi tạo khung của cửa sổ client
        self.title("Exchange rate")
        self.geometry("700x400")
        self.resizable(width=False, height=False)

        self.container = tk.Frame()
        self.container.configure(bg="red")

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


    def showEnterIpPage(self):
        '''Hiện lên màn hình nhập ip address'''
        frame = EnterIpPage(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")

    def showChatPage(self):
        '''Hiện lên màn hình chat với server'''
        frame = ChatPage(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        
        #Bắt đầu nhận dữ liệu từ server
        receive_thread = Thread(target=frame.receive)
        receive_thread.start()

    def showUnableToConnectToServerPage(self):
        '''Hiện lên màn hình hiển thị lỗi khi không thể kết nối tới server'''
        frame = UnableToConnectToServerPage(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
    
    #Lấy {msg} làm argument
    def connectToServer(self, msg):
        '''Kết nối tới server'''

        #Lấy thông tin HOST từ msg
        HOST = msg
          
        #Thử kết nối tới server
        try:
            client_socket.connect((HOST, 33000))
        except:
            '''Trường hợp không kết nối được tới server'''
            print("Error")

            #Hiện màn hình lỗi
            self.showUnableToConnectToServerPage()
            return
        
        #Nếu kết nối thành công hiện màn hình chat {ChatPage}
        self.showChatPage()

# --------------------------------------------MAIN---------------------------------------------------
if __name__ == "__main__":
    #Khởi tạo các biến cần thiết
    FORMAT = "utf8"
    HOST = 0
    BUFSIZ = 1024
    ADDR = (HOST, 33000)
    
    #Khởi động client
    client_socket = socket(AF_INET, SOCK_STREAM)
    
    client_app = ClientApp()
    client_app.showEnterIpPage()
    client_app.mainloop()
