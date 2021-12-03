#Import tkinter library
from tkinter import *
from babel.dates import DateTimePattern
from tkcalendar import Calendar, DateEntry
#Create an instance of tkinter frame
win= Tk()
#Set the Geometry
win.geometry("750x250")
win.title("Date Picker")
#Create a Label
Label(win, text= "Choose a Date", background= 'gray61', foreground="white").pack(padx=20,pady=20)
#Create a Calendar using DateEntry
cal = DateEntry(win, width= 16, background= "magenta3", foreground= "white",bd=2, date_pattern='dd/mm/y')
cal.pack(pady=20)


def grad_date():
    print( "Selected Date is: " + cal.get_date().strftime("%d/%m/%Y"))
 
# Add Button and Label
Button(win, text = "Get Date",
       command = grad_date).pack(pady = 20)


win.mainloop()