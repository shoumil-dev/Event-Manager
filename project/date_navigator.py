""" A gui application that produces a calendar that will allow the user to navigate through days, months and years."""

# import relevant tk libraries
from tkinter import *
from tkcalendar import Calendar
# import date module
from datetime import date
 
# Create Tk Object
root = Tk()
 
# Set geometry
root.geometry("350x350")
 
today_date = str(date.today())
current_day = int(today_date[0:4])
current_month = int(today_date[5:7])

# Add Calendar
cal = Calendar(root, selectmode = 'day',
               year = 2022, month = current_month,
               day = current_day)
 
cal.pack(pady = 20)
 
def grad_date():
    date.config(text = "Selected Date is: " + cal.get_date())
 
# Button and Label to get event
Button(root, text = "Get Event",
       command = grad_date).pack(pady = 20)
 
date = Label(root, text = "")
date.pack(pady = 20)
 
# run the tkinter mainloop
root.mainloop()