import os

base_url = os.path.dirname(os.path.realpath(__file__))
import subprocess
import tkinter as tk
import PIL.Image

# from tkinter import ttk
from tkinter import *
from datetime import datetime
from datetime import date
import sqlite3
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.widgets import DateEntry, Querybox
import hashlib

# from tkinter import font
# import pyglet
# from tkextrafont import Font

# from tkextrafont import load_extrafont

from welfareutils import functions as func
from welfareutils import database_functions as dbfunc

main = ttkb.Window(themename="simplex")
main.title("জালালাবাদ গ্যাস ওয়েলফেয়ার ফান্ড")
# main.configure(=("Nikosh 14 bold"))
# main:window.-font Arial 12 bold


main.iconbitmap("images/032.ico")
main.iconbitmap(default="images/032.ico")

main.geometry("1200x850")
main.configure(bg="#6B6B6B")
main.resizable(False, False)
main.place_window_center()
signup_frm = ttkb.Frame(main, width=850, height=400, bootstyle="white")
signup_frm.pack(expand=True)
main_frm = ttkb.Frame(main, bootstyle="white")
menu_frame = ttkb.Frame(main, bootstyle="white")
# main.mainloop()
