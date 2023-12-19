from JGWELFARE_FUND_base import *
from JGWELFARE_Main import my_top_lavel


def signin():
    #! Password encripted ===================
    username = user.get()
    p1 = bytes(code.get(), encoding="utf-8")
    p2 = b"28605495YHlCJfMKpRPGyAw"
    m = hashlib.sha256()
    m.update(p1)
    m.update(p2)
    # m.digest()
    password = m.hexdigest()
    #! Password encripted End ===================

    conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
    user_name_password = conn.cursor()
    user_name_password.execute(
        f"SELECT * FROM user WHERE user_name = '{username}' AND password='{password}'"
    )
    record_user_name_password = user_name_password.fetchall()
    # print(record_user_name_password)
    conn.commit()
    conn.close()
    # if username == "admin" and password == "12":
    if record_user_name_password != []:
        my_top_lavel(username)
        # signup_frm.destroy()
    else:
        Messagebox.show_error(
            "ইউজারনেম এবং/অথবা পাসওয়ার্ড সঠিক নয়!",
            "অসঠিক তথ্য",
            parent=signup_frm,
        )
    # return {'username':username}


img = PhotoImage(file=os.path.join(base_url, "images/login.png"))
ttkb.Label(signup_frm, image=img, bootstyle="white").place(x=30, y=50)

frame = ttkb.Frame(signup_frm, width=400, height=350, bootstyle="white")
frame.place(x=430, y=55)

heading = ttkb.Label(
    frame,
    text="Sign in",
    bootstyle="success",
    font=("Arial", 23, "bold"),
)
heading.place(x=100, y=5)


#!################==============================
def on_enter(e):
    user.delete(0, "end")


def on_leave(e):
    name = user.get()
    if name == "":
        user.insert(0, "Username")


user = ttkb.Entry(
    frame,
    width=25,
    # fg="black",
    # border=0,
    # bg="white",
    bootstyle="light",
    font=("Microsoft YaHei UI Light", 11),
)
user.place(x=30, y=80)
user.insert(0, "Username")
user.bind("<FocusIn>", on_enter)
user.bind("<FocusOut>", on_leave)
ttkb.Frame(frame, width=315, height=2, bootstyle="dark").place(x=35, y=117)


#!################==============================
def on_enter(e):
    code.delete(0, "end")


def on_leave(e):
    name = code.get()
    if name == "":
        code.insert(0, "Password")


code = ttkb.Entry(
    frame,
    width=25,
    # fg="black",
    # border=0,
    show="*",
    bootstyle="light",
    font=("Microsoft YaHei UI Light", 11),
)
code.place(x=30, y=150)
code.insert(0, "Password")
code.bind("<FocusIn>", on_enter)
code.bind("<FocusOut>", on_leave)
ttkb.Frame(frame, width=315, height=2, bootstyle="dark").place(x=35, y=187)

#!#####Hide and show button button_mode=True

button_mode = False


def hide():
    global button_mode
    if button_mode:
        eyeButton.config(
            image=closeeye,
        )  # activebackground="white"
        code.config(show="*")
        button_mode = False
    else:
        eyeButton.config(
            image=openeye,
        )  # activebackground="white"
        code.config(show="")
        button_mode = True


img_openeye = PhotoImage(
    file=os.path.join(base_url, "images/openeye.png")
)  # ,width=int(381/15),height=int(275/15)
img_closeeye = PhotoImage(
    file=os.path.join(base_url, "images/closeeye.png")
)  # ,width=int(381/15),height=int(275/15)
# openeye.configure(height=55, width=50)
openeye = img_openeye  # .subsample(15, 15)
closeeye = img_closeeye  # .subsample(15, 15)
# closeeye.configure(height=55, width=50)

eyeButton = ttkb.Button(
    frame, image=closeeye, bootstyle=("light-outline"), command=hide
)
eyeButton.place(x=350, y=160)

#!#####Hide and show button

ttkb.Button(
    frame,
    width=30,
    text="Sign in",
    bootstyle="success",
    command=signin,
).place(x=35, y=204)

signup_frm.mainloop()
main.mainloop()
