from socket import socket
import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle

class ChatPage(tk.Frame):
    '''Màn hình chat của client'''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        msg_frame = tk.Frame(self)

        # For the messages to be sent.
        self.my_msg = tk.StringVar()  
        self.my_msg.set("Type your messages here.")

        # To navigate through past messages.
        scrollbar = tk.Scrollbar(msg_frame)
        
        #Khởi tạo Listbox hiển thị thông tin chat
        self.msg_list = tk.Listbox(msg_frame, height=20, width=50,
                              yscrollcommand=scrollbar.set, bg='light yellow')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack()
        msg_frame.pack()
        
        #Khởi tạo ô nhập tin nhắn
        entry_field = tk.Entry(self, textvariable=self.my_msg, width=100,)
        # entry_field.bind("<Return>", self.send)
        entry_field.pack()
        send_button = tk.Button(self, text="Send", command=self.send)
        send_button.pack()
    
    # event is passed by binders.
    def send(self):  
        """Handles sending of messages."""
        msg = self.my_msg.get()

        # Clears input field.
        self.my_msg.set("")  
        client_socket.send(bytes(msg, "utf8"))
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
                
                if msg == "tsillist":
                    msg = client_socket.recv(BUFSIZ)
                    data_recv = pickle.loads(msg)
                    print(data_recv)
                    for item in data_recv:
                        self.msg_list.insert(tk.END, item)
                    
                else:
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
