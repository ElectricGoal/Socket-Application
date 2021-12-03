from socket import socket
import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
from babel.dates import DateTimePattern
from tkcalendar import Calendar, DateEntry

class ChatPage(tk.Frame):
    '''Màn hình chat của client'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # For the messages to be sent.
        self.my_msg = tk.StringVar()  
        self.my_msg.set("Type your messages here.")
        
        #Frame bên trái
        left_frame = tk.Frame(self)
        left_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        msg_frame = tk.Frame(left_frame)
        msg_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(msg_frame)
        self.msg_list = tk.Listbox(msg_frame, yscrollcommand=scrollbar.set, bg='light yellow')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(fill=tk.BOTH, expand=True)
        

        entry_field = tk.Entry(left_frame, textvariable=self.my_msg)
        entry_field.pack(fill=tk.BOTH)

        send_button = tk.Button(left_frame, text="Send", command=self.send)
        send_button.pack()
        
        #Frame bên phải
        right_frame = tk.Frame(self)
        right_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        text_label = tk.Label(right_frame, text= "Choose a Date", background= 'gray61', foreground="white")
        cal = DateEntry(right_frame, width= 16, background= "magenta3", foreground= "white",bd=2, date_pattern='dd/mm/y')
        text_label.pack()
        cal.pack()


    
    # event is passed by binders.
    def send(self):  
        """Handles sending of messages."""
        msg = self.my_msg.get()

        # Clears input field.
        self.my_msg.set("") 
        client_socket.send(bytes(msg, "utf8"))
        self.msg_list.insert(tk.END, "You: %s" %msg)
        if msg == "{quit}":
            client_socket.close()
            self.quit()
            
    def on_closing(self):
        """This function is to be called when the window is closed."""
        self.my_msg.set("{quit}")
        self.send()

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = client_socket.recv(BUFSIZ).decode(FORMAT)

                if msg == "yrotsih":
                    msg = client_socket.recv(BUFSIZ)
                    data_recv = pickle.loads(msg)
                    self.msg_list.insert(tk.END, "Server: ")
                    for items in data_recv:
                        for item in items:
                            self.msg_list.insert(tk.END, item)
                        self.msg_list.insert(tk.END, "   ---------------------")
                    continue

                if msg == "tsillist":
                    msg = client_socket.recv(BUFSIZ)
                    data_recv = pickle.loads(msg)
                    self.msg_list.insert(tk.END, "Server: ")
                    for item in data_recv:
                        self.msg_list.insert(tk.END, item)
                    
                else:
                    self.msg_list.insert(tk.END, "Server: ")
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
        self.title("Currency converter")
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
