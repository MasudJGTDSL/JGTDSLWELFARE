"""
INSERT INTO Employee (JGID, EmployeeName, Designation, BasicPay, AmountToPay, PRLDate, MobileNo) 
                VALUES (:JGID, :EmployeeName, :Designation, :BasicPay, :AmountToPay, :PRLDate, :MobileNo),
            {
                "JGID": entry_jgid.get(),
                "EmployeeName": entry_name.get(),
                "Designation": entry_designation.get(),
                "BasicPay": entry_basic.get(),
                "AmountToPay": func.welfare_fund_calculation(entry_basic.get()),
                "PRLDate": datetime.strptime(
                    entry_prldate.entry.get(), "%d/%m/%Y"
                ).strftime("%Y-%m-%d"),
                "MobileNo": entry_mobile.get(),
            },
"""
from JGWELFARE_FUND_base import *

# from main_signin import *


def dbconnection(sql_string: str, input_dic):
    conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
    c = conn.cursor()
    c.execute(
        sql_string,
        input_dic,
    )
    conn.commit()
    conn.close()


def add_user_execute(current_user):
    if current_user != "admin":
        Messagebox.show_info(
            "শুধুমাত্র 'admin' নতুন ইউজার তৈরী করতে পারবেন!",
            "অননুমোদিত ইউজার ",
            parent=user_create_window,
            alert=True,
        )
    else:
        # password1_entry, password2_entry, user_entry
        user_id = user_entry.get()
        pass_wd1 = password1_entry.get()
        pass_wd2 = password2_entry.get()
        conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
        c = conn.cursor()
        query = f"SELECT user_name FROM user WHERE user_name = '{user_id}';"
        c.execute(query)
        user_record = c.fetchall()
        if user_record == []:
            if (
                user_id.strip() == ""
                or pass_wd1.strip() == ""
                or pass_wd2.strip() == ""
            ):
                Messagebox.show_info(
                    "ইউজার আইডি বা পাসওয়ার্ড-১ ও পাসওয়ার্ড-২ আবশ্যক।",
                    "আবশ্যিক ফিল্ড",
                    parent=user_create_window,
                    alert=True,
                )

            elif pass_wd1 != pass_wd2:
                Messagebox.show_info(
                    "পাসওয়ার্ড-১ ও পাসওয়ার্ড-২ অভিন্ন নয়!",
                    "পাসওয়ার্ড নিশ্চিত করণ",
                    parent=user_create_window,
                    alert=True,
                )

            else:
                p1 = bytes(pass_wd1, encoding="utf-8")
                p2 = b"28605495YHlCJfMKpRPGyAw"
                m = hashlib.sha256()
                m.update(p1)
                m.update(p2)
                # m.digest()
                password = m.hexdigest()
                sql_srt = f"INSERT INTO user (user_name, password) VALUES('{user_id}', '{password}')"
                user_add = conn.cursor()
                user_add.execute(sql_srt)
                conn.commit()
                conn.close()
                Messagebox.show_info(
                    f'ধন্যবাদ, "{user_id}" নামে একটি ইউজার এন্ট্রি সম্পন্ন করা হয়েছে',
                    "ইউজার তৈরী নিশ্চিত করণ!",
                    parent=user_create_window,
                    alert=True,
                )
                user_create_window.destroy()
        else:
            Messagebox.show_info(
                f'ইতোমধ্যে "{user_id}" নামে একটি ইউজার আছে!',
                "ডুপ্লিকেট ইউজার",
                parent=user_create_window,
                alert=True,
            )


def add_user(current_user):
    global user_create_window, password1_entry, password2_entry, user_entry
    user_create_window = ttkb.Toplevel(
        # user_creation_frame,
        topmost=True,
        toolwindow=False,
        alpha=1,
        size=(470, 255),
        resizable=(False, False),
        # position=(550, 200),
    )
    user_create_window.configure(
        bg="white",
    )
    user_create_window.title("Add New User")
    user_create_window.place_window_center()
    user_creation_frame = ttkb.LabelFrame(
        user_create_window, text="নতুন ইউজার-এর প্রয়োজনীয় তথ্য"
    )

    lebel_user_name = ttkb.Label(
        user_creation_frame, text="ইউজার আইডিঃ ", font=("Nikosh", 12)
    )
    lebel_password1 = ttkb.Label(
        user_creation_frame, text="পার্সওয়ার্ডঃ ", font=("Nikosh", 12)
    )
    lebel_password2 = ttkb.Label(
        user_creation_frame, text="পার্সওয়ার্ড পুনরায়ঃ ", font=("Nikosh", 12)
    )

    user_entry = ttkb.Entry(
        user_creation_frame,
        width=25,
    )
    password1_entry = ttkb.Entry(
        user_creation_frame,
        width=25,
        show="*",
    )
    password2_entry = ttkb.Entry(
        user_creation_frame,
        width=25,
        show="*",
    )

    button_frame = ttkb.Frame(user_create_window)

    ttkb.Button(
        button_frame,
        text="Create User",
        width=12,
        bootstyle="success",
        command=lambda: add_user_execute(current_user),
    ).pack(side=RIGHT, padx=5)

    ttkb.Button(
        button_frame,
        text="Cancel",
        width=12,
        bootstyle="danger",
        command=lambda: user_create_window.destroy(),
    ).pack(side=RIGHT, padx=5)

    lebel_user_name.grid(row=0, column=0, padx=5, pady=5, sticky=E)
    user_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)
    lebel_password1.grid(row=1, column=0, padx=5, pady=5, sticky=E)
    password1_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)
    lebel_password2.grid(row=2, column=0, padx=5, pady=5, sticky=E)
    password2_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    user_creation_frame.pack(fill=X, padx=15, pady=10)
    button_frame.pack(fill=X, padx=10, pady=5)
    user_create_window.mainloop()


def change_password_execute(user_name, old_passwd, passwd1, passwd2):
    conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
    old_passwd_query = conn.cursor()
    old_passwd_query.execute(
        f"SELECT user_name, password FROM user WHERE user_name = '{user_name}'"
    )
    user_record = old_passwd_query.fetchone()
    p1 = bytes(old_passwd, encoding="utf-8")
    p2 = b"28605495YHlCJfMKpRPGyAw"
    m = hashlib.sha256()
    m.update(p1)
    m.update(p2)
    passwd = m.hexdigest()

    if old_passwd.strip() == "" or passwd1.strip() == "" or passwd2.strip() == "":
        Messagebox.show_info(
            "পুরাতন পাসওয়ার্ড বা পাসওয়ার্ড-১ ও পাসওয়ার্ড-২ আবশ্যক।",
            "আবশ্যিক ফিল্ড",
            parent=change_password_window,
            alert=True,
        )
    elif user_record[1] != passwd:
        Messagebox.show_info(
            "পুরাতন পাসওয়ার্ডটি সঠিক নয়",
            "ভুল পাসওয়ার্ড",
            parent=change_password_window,
            alert=True,
        )

    elif passwd1 != passwd2:
        Messagebox.show_info(
            "পাসওয়ার্ড-১ ও পাসওয়ার্ড-২ অভিন্ন নয়!",
            "পাসওয়ার্ড নিশ্চিত করণ",
            parent=change_password_window,
            alert=True,
        )
    else:
        ps1 = bytes(passwd1, encoding="utf-8")
        ps2 = b"28605495YHlCJfMKpRPGyAw"
        m1 = hashlib.sha256()
        m1.update(ps1)
        m1.update(ps2)
        passwd = m1.hexdigest()
        c = conn.cursor()
        c.execute(
            f"UPDATE user SET password = '{passwd}' WHERE user_name = '{user_name}';"
        )
        Messagebox.show_info(
            f'"পাসওয়ার্ড পরিবর্তন করা হয়েছে',
            "পাসওয়ার্ড পরিবর্তন নিশ্চিত করণ!",
            parent=change_password_window,
            alert=True,
        )
        change_password_window.destroy()
    conn.commit()
    conn.close()


def change_password(user_name):
    global user_nm, old_passwd_entry, new_password1_entry, new_password2_entry
    user_nm = user_name

    global change_password_window
    change_password_window = ttkb.Toplevel(
        # user_creation_frame,
        topmost=True,
        toolwindow=False,
        alpha=1,
        size=(505, 255),
        resizable=(False, False),
        # position=(550, 200),
    )
    change_password_window.configure(
        bg="white",
    )
    change_password_window.title("পাসওয়ার্ড পরিবর্তন")
    change_password_window.place_window_center()
    user_creation_frame = ttkb.LabelFrame(
        change_password_window, text="বর্তমান ও নতুন পাসওয়ার্ড ইনপুট"
    )

    lebel_old_password = ttkb.Label(
        user_creation_frame, text="বর্তমান পাসওয়ার্ড ", font=("Nikosh", 12)
    )
    lebel_new_password1 = ttkb.Label(
        user_creation_frame, text="নতুন পার্সওয়ার্ডঃ ", font=("Nikosh", 12)
    )
    lebel_new_password2 = ttkb.Label(
        user_creation_frame, text="নতুন পার্সওয়ার্ড পুনরায়ঃ ", font=("Nikosh", 12)
    )

    old_passwd_entry = ttkb.Entry(
        user_creation_frame,
        width=25,
        show="*",
    )
    new_password1_entry = ttkb.Entry(
        user_creation_frame,
        width=25,
        show="*",
    )
    new_password2_entry = ttkb.Entry(
        user_creation_frame,
        width=25,
        show="*",
    )

    button_frame = ttkb.Frame(change_password_window)

    ttkb.Button(
        button_frame,
        text="Change Password",
        width=15,
        bootstyle="success",
        command=lambda: change_password_execute(
            user_nm,
            old_passwd_entry.get(),
            new_password1_entry.get(),
            new_password2_entry.get(),
        ),
    ).pack(side=RIGHT, padx=5)

    ttkb.Button(
        button_frame,
        text="Cancel",
        width=15,
        bootstyle="danger",
        command=lambda: change_password_window.destroy(),
    ).pack(side=RIGHT, padx=5)

    lebel_old_password.grid(row=0, column=0, padx=5, pady=5, sticky=E)
    old_passwd_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)
    lebel_new_password1.grid(row=1, column=0, padx=5, pady=5, sticky=E)
    new_password1_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)
    lebel_new_password2.grid(row=2, column=0, padx=5, pady=5, sticky=E)
    new_password2_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    user_creation_frame.pack(fill=X, padx=15, pady=10)
    button_frame.pack(fill=X, padx=10, pady=5)
    change_password_window.mainloop()
