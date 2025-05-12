from tkinter import *
from tkinter import ttk
from datetime import datetime
import re

root = Tk()
root.geometry('800x600+700+250')
root.title('Создание мероприятий')

def check_date_format(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


name = Label(root, font=('Sans,20'), text="Приложение для создания мероприятий.")
name.pack(anchor="n")


title = Label(root, text="Введите название мероприятия: ")
title.place(x=20, y=35)

title_mp = ttk.Entry()
title_mp.place(anchor=NW, x=210, y=35)

date = Label(root,  text="Введите дату начала мероприятия: ")
date.place(anchor=W, x=20, y=85)

date_mp = ttk.Entry()
date_mp.place(anchor=NW, x=220, y=75)


root.resizable(False, False)
root.mainloop()