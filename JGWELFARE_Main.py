from JGWELFARE_FUND_base import *
from create_pdf import create_pdf, pending_payment_list

# record_set = []

def query_database(jgid=0):
    conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
    c = conn.cursor()
    query = """SELECT substr('000'||a.JGID, -3,3) as JGID, a.EmployeeName, a.Designation, a.BasicPay, a.AmountToPay, 
            strftime('%d/%m/%Y',a.PRLDate) as PRLDate, substr('00000000000'||a.MobileNo, -11,11) as MobileNo, 
            SUM(IFNULL(b.PaidAmount,0)) as PaidAmount, 
            count(b.JGID) as Installment
            FROM Employee a LEFT JOIN Payment b ON a.JGID = b.JGID  
            """
    c.execute(f"{query} GROUP BY a.JGID ORDER BY a.JGID")
    all_records = c.fetchall()

    single_c = conn.cursor()
    single_c.execute(
        f"""SELECT * FROM (SELECT a.JGID, a.EmployeeName, a.Designation, a.BasicPay, a.AmountToPay, a.PRLDate, a.MobileNo, 
        b.id, b.PaidAmount, b.PaymentDate, b.Remarks 
        FROM Employee a LEFT JOIN Payment b on a.JGID = b.JGID) c WHERE JGID = '{int(jgid)}'"""
    )
    single_record = single_c.fetchall()

    payment_c = conn.cursor()
    payment_c.execute(
        """SELECT SUM(a.AmountToPay) as TotalAmountToPay, SUM(b.PaidAmount) as TotalPaidAmount 
        FROM Employee a LEFT JOIN Payment b on a.JGID = b.JGID
        """
    )
    payment_remaining = payment_c.fetchall()

    single_c_summary = conn.cursor()

    single_c_summary.execute(f"{query} WHERE a.JGID ={int(jgid)} GROUP BY a.JGID")
    single_record_summary = single_c_summary.fetchone()

    conn.commit()
    conn.close()
    return {
        "all_records": all_records,
        "single_record": single_record,
        "payment_remaining": payment_remaining,
        "single_record_summary": single_record_summary,
    }


def insert_into_payment_table():
    conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
    c = conn.cursor()
    c.execute(
        """INSERT INTO Payment (PaidAmount, PaymentDate, Remarks, JGID) 
            VALUES (:PaidAmount, :PaymentDate, :Remarks, :JGID)""",
        {
            "PaidAmount": entry_amount.get(),
            "PaymentDate": datetime.strptime(
                entry_payment_date.entry.get(), "%d/%m/%Y"
            ).strftime("%Y-%m-%d"),
            "Remarks": entry_remark.get(),
            "JGID": entry_jgid_payment.get(),
        },
    )

    conn.commit()
    conn.close()


def payment_details(event):
    single_record = query_database(entry_jgid_payment.get())["single_record"]
    global payment_window, employ_details_frame, payment_details_frame
    jgid_payment = entry_jgid_payment.get()
    employ_details_frame.destroy()
    payment_details_frame.destroy()
    entry_amount.delete(0, END)
    employ_details_frame = ttkb.LabelFrame(
        payment_window, text="কর্মকর্তা/কমচারীর বিস্তারিত তথ্য"
    )
    ttkb.Label(employ_details_frame, text="          জেজি আইডিঃ ").grid(
        row=0, column=0, padx=5, pady=5, sticky="E"
    )
    global id_lebel, nm_label
    id_lebel = ttkb.Label(
        employ_details_frame,
        width=20,
        text=f"{single_record[0][0]}",
    )
    id_lebel.grid(row=0, column=1, padx=5, pady=5, sticky="W")

    ttkb.Label(employ_details_frame, text="নামঃ ").grid(
        row=1, column=0, padx=5, pady=5, sticky="E"
    )

    nm_label = ttkb.Label(
        employ_details_frame,
        text=f"{single_record[0][1]},",
        bootstyle="danger",
    )
    nm_label.grid(row=1, column=1, padx=5, sticky="W")

    ttkb.Label(employ_details_frame, text="পদবীঃ ").grid(
        row=1, column=2, padx=5, pady=5, sticky="E"
    )
    ttkb.Label(employ_details_frame, text=f"{single_record[0][2]}").grid(
        row=1, column=3, padx=5, pady=5, sticky="W"
    )
    ttkb.Label(employ_details_frame, text="পিআরএল তারিখঃ ").grid(
        row=2, column=0, padx=5, pady=5, sticky="E"
    )
    ttkb.Label(
        employ_details_frame,
        text=f"{func.dateINbangla(datetime.strptime(single_record[0][5],'%Y-%m-%d'))},",
    ).grid(row=2, column=1, padx=5, pady=5, sticky="W")
    ttkb.Label(employ_details_frame, text="সর্বশেষ ব্যাসিকঃ ").grid(
        row=2, column=2, padx=5, sticky="E"
    )
    ttkb.Label(
        employ_details_frame,
        text=f"৳ {func.enTobnNumber(func.intcomma_bd(int(single_record[0][3])))}/-",
    ).grid(row=2, column=3, padx=5, pady=5, sticky="W")
    # employ_details_frame.pack(fill=X, pady=10, padx=5)
    ttkb.Label(employ_details_frame, text="মোট দেয় অর্থঃ ").grid(
        row=3, column=0, padx=5, pady=5, sticky="E"
    )
    ttkb.Label(
        employ_details_frame,
        text=f"৳ {func.enTobnNumber(func.intcomma_bd(int(single_record[0][4])))}/-,",
        bootstyle="danger",
    ).grid(row=3, column=1, padx=5, pady=5, sticky="W")
    # employ_details_frame.pack(fill=X, pady=10, padx=5)

    ttkb.Label(employ_details_frame, text="মোবাইল নম্বরঃ ").grid(
        row=3, column=2, padx=5, pady=5, sticky="E"
    )
    ttkb.Label(
        employ_details_frame,
        text=f"{single_record[0][6].rjust(11, '0')}",
    ).grid(
        row=3, column=3, padx=5, pady=5, sticky="W"
    )  #!.rjust(5, "0") or .zfill(11)
    employ_details_frame.pack(fill=X, pady=10, padx=10)

    if query_database(jgid_payment)["single_record"][0][7] != None:
        payment_details_frame = ttkb.LabelFrame(
            payment_window, text="কল্যান তহবিল থেকে পরিশেধের তথ্য"
        )
        employee_info_data = [
            [
                dt[7],
                func.dateINbangla(datetime.strptime(dt[9], "%Y-%m-%d")),
                f"{func.enTobnNumber(func.intcomma_bd(int(dt[8])))}/-",
                dt[10],
            ]
            for dt in query_database(entry_jgid_payment.get())["single_record"]
        ]
        payment_coldata = [
            {
                "text": "",
                # "minwidth": 0,
                "stretch": False,
                # "anchor": "w",
                "width": 0,
                # "command": show_message,
            },
            {"text": "তারিখ", "width": 160, "stretch": False},
            {"text": "পরিশোধিত অর্থ", "width": 140, "stretch": False},
            {"text": "মন্তব্য", "anchor": "e", "stretch": True},
        ]
        global payment_table_dt
        # rowdata = employee_info_data
        payment_table_dt = Tableview(
            master=payment_details_frame,
            coldata=payment_coldata,
            rowdata=employee_info_data,
            paginated=False,
            searchable=False,
            # bootstyle=SUCCESS,
            pagesize=5,
            height=5,
            stripecolor=("antiquewhite", None),
        )
        # payment_table_dt.autofit_columns()

        ttkb.Button(
            payment_details_frame,
            text="Delete",
            width=10,
            bootstyle="danger",
            command=delete_payment,
        ).pack(side=LEFT, padx=5)

        payment_table_dt.pack(fill=BOTH, expand=YES, padx=5, pady=10)
        # payment_table_dt.bind_all("<<TreeviewSelect>>", delete_payment)
        payment_details_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)


def payment_amount(event):
    global entry_jgid_payment, entry_amount
    dt = query_database(entry_jgid_payment.get())["single_record_summary"]
    entry_amount.delete(0, END)
    entry_amount.insert(0, (int(dt[4]) - int(dt[7])))


def delete_payment():
    row_ob = payment_table_dt.get_rows(selected=True)
    msg = Messagebox.okcancel(
        f"""Are you sure you want to delete record:\nজেজি আইডি: {id_lebel["text"]}\nDate: {row_ob[0].values[1]}\nAmount: {row_ob[0].values[2]}?""",
        "Delete Confirmation!",
        parent=employ_details_frame,
        alert=True,
    )
    if msg == "OK":
        conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
        c = conn.cursor()
        c.execute(f"DELETE FROM Payment WHERE id = {int(row_ob[0].values[0])};")
        conn.commit()
        conn.close()
        payment_details("event")


def add_payment():
    global entry_jgid_payment, payment_window, employ_details_frame, payment_details_frame
    payment_window = ttkb.Toplevel(
        main,
        topmost=True,
        toolwindow=False,
        alpha=1,
        size=(900, 650),
        resizable=(False, False),
        # position=(550, 200),
    )
    payment_window.configure(
        bg="white",
    )
    payment_window.title("Welfare Fund Payment")
    payment_window.place_window_center()

    def execute_add():
        payment_date = datetime.strptime(entry_payment_date.entry.get(), "%d/%m/%Y")
        msgtxt = f"আপনি কি নিম্নোক্ত পরিশোধটি এন্ট্রি করতে চাইছেন?\n"
        msgtxt += f"{'-'*len(msgtxt)}\n"
        msg = Messagebox.yesno(
            (
                f"{msgtxt}"
                f"জেজি আইডি: {id_lebel['text']},\n"
                f"নামঃ {nm_label['text']}\n"
                f"তারিখঃ {func.dateINbangla(payment_date)}\n"
                f"টাকার পরিমানঃ ৳{func.enTobnNumber(func.intcomma_bd(entry_amount.get()))}/-"
            ),
            "নতুন পরিশোধটি নিশ্চিত করুন!",
            parent=employ_details_frame,
            alert=True,
        )
        if msg == "Yes":
            insert_into_payment_table()
            refresh_dt = entry_jgid_payment.get()
            entry_jgid_payment.delete(0, END)
            entry_amount.delete(0, END)
            entry_remark.delete(0, END)
            entry_jgid_payment.insert(0, refresh_dt)
            payment_details("event")

    payment_frame = ttkb.LabelFrame(payment_window, text="কল্যান তহবিল থেকে পরিশোধ")

    label_jgid_payment = ttkb.Label(
        payment_frame, text="জেজি আইডিঃ ", font=("Nikosh", 12)
    )
    label_payment_date = ttkb.Label(payment_frame, text="তারিখঃ ", font=("Nikosh", 12))
    label_amount = ttkb.Label(
        payment_frame, text="পরিশোধিত অর্থঃ ", font=("Nikosh", 12)
    )
    label_remarks = ttkb.Label(payment_frame, text="মন্তব্যঃ ", font=("Nikosh", 12))

    combo_item = []
    for item in query_database()["all_records"]:
        if int(item[4]) > int(item[7]):
            combo_item.append(item[0])

    global entry_payment_date, entry_amount, entry_remark, entry_jgid_payment
    first_string = ttkb.StringVar(value=combo_item[0])
    entry_jgid_payment = ttkb.Combobox(
        payment_frame,
        textvariable=first_string,
        width=13,
    )
    entry_jgid_payment["values"] = combo_item

    entry_payment_date = DateEntry(
        payment_frame,
        # style='TCalendar',
        width=15,
        bootstyle="secondary",
        # startdate = prl_date,
        dateformat="%d/%m/%Y",
    )
    entry_amount = ttkb.Entry(
        payment_frame,
        width=15,
    )
    entry_remark = ttkb.Entry(
        payment_frame,
        width=40,
    )

    label_jgid_payment.grid(row=0, column=0, padx=5, pady=10, sticky=E)
    entry_jgid_payment.grid(row=0, column=1, padx=5, pady=10, sticky=W)
    label_payment_date.grid(row=0, column=2, padx=5, pady=10, sticky=E)
    entry_payment_date.grid(row=0, column=3, padx=5, pady=10, sticky=W)
    label_amount.grid(row=1, column=0, padx=5, pady=10, sticky=E)
    entry_amount.grid(row=1, column=1, padx=5, pady=10, sticky=W)
    label_remarks.grid(row=1, column=2, padx=5, pady=10, sticky=E)
    entry_remark.grid(row=1, column=3, columnspan=3, padx=6, pady=10, sticky=W)
    # entry_jgid.bind("<Enter>", payment_details)
    # entry_jgid_payment.bind("<FocusOut>", payment_details)
    entry_jgid_payment.bind("<<ComboboxSelected>>", payment_details)
    entry_amount.bind("<FocusIn>", payment_amount)
    ttkb.Button(
        payment_frame,
        text="Add Payment",
        width=18,
        bootstyle=SUCCESS,
        command=execute_add,
    ).grid(row=2, column=3, padx=5, pady=10, sticky="E")
    ttkb.Button(
        payment_frame,
        text="Cancel",
        width=18,
        bootstyle=DANGER,
        command=lambda: payment_window.destroy(),
    ).grid(row=2, column=4, padx=5, pady=10, sticky="E")

    payment_frame.pack(fill=X, pady=10, padx=10)
    employ_details_frame = ttkb.LabelFrame(
        payment_window, text="কর্মকর্তা/কমচারীর বিস্তারিত তথ্য"
    )
    payment_details_frame = ttkb.LabelFrame(
        payment_window, text="পরিশোধ বিস্তারিত তথ্য"
    )


# def change_password():
#     present_user = current_user_label.cget("text").strip("বর্তমান ইউজারঃ ")
#     lambda: dbfunc.change_password(present_user)


def my_top_lavel(user_name):
    global entry_prldate, entry_jgid, paid_amnt, entry_basic, entry_name, entry_designation, current_user_label
    signup_frm.destroy()
    #! Menu ==========================
    menu_button = ttkb.Menubutton(
        menu_frame, text="File", style="success.Outline.TMenubutton"
    )
    menu_button.configure(width=8)
    menu_button_report = ttkb.Menubutton(
        menu_frame, text="Report", style="warning.Outline.TMenubutton"
    )
    menu_button_report.configure(width=8)

    current_user_label = ttkb.Label(
        menu_frame,
        padding=5,
        text=f"বর্তমান ইউজারঃ {user_name}",
        bootstyle="warning, inverse",
    )

    def refresh_data():
        table_dt.destroy()
        populate_data_in_table()

    button_sub_menu = ttkb.Menu(menu_button, tearoff=False)
    button_sub_menu.add_command(label="Refresh", command=refresh_data)
    button_sub_menu.add_separator()
    button_sub_menu.add_command(
        label="Change Password",
        command=lambda: dbfunc.change_password(
            current_user_label.cget("text").strip("বর্তমান ইউজারঃ ")
        ),
    )
    button_sub_menu.add_command(
        label="Add User",
        command=lambda: dbfunc.add_user(
            current_user_label.cget("text").strip("বর্তমান ইউজারঃ ")
        ),
    )
    #! Report Menu ===========================
    button_sub_menu_report = ttkb.Menu(menu_button_report, tearoff=False)
    button_sub_menu_report.add_command(
        label="Payment Pending List",
        command=lambda: pending_payment_list(False),
    )
    button_sub_menu_report.add_command(
        label="All Payment List",
        command=lambda: pending_payment_list(True),
    )
    menu_button_report["menu"] = button_sub_menu_report
    img_refresh = PhotoImage(file="images/refresh-24.png")
    refresh_button = ttkb.Button(
        menu_frame,
        text="Refresh",
        image=img_refresh,
        compound=LEFT,
        # width=10,
        bootstyle="info,outline",
        command=refresh_data,
    )
    #! Report Menu ===========================
    menu_button["menu"] = button_sub_menu
    menu_button.pack(side=LEFT, pady=10, padx=5)
    menu_button_report.pack(side=LEFT, pady=10, padx=5)
    refresh_button.pack(side=LEFT, pady=10, padx=5)
    current_user_label.pack(side=RIGHT, padx=10)
    menu_frame.pack(
        fill=X,
    )
    #! Menu ==========================
    main_frm.pack(expand=True, fill=X, pady=0, padx=0)

    def clear_entry():
        # Clear entry boxes
        entry_jgid.delete(0, END)
        entry_name.delete(0, END)
        entry_designation.delete(0, END)
        entry_basic.delete(0, END)
        # entry_prldate.delete(0, END)
        entry_mobile.delete(0, END)
        payment_status.configure(
            subtext="", amountused=0.0  # (1245031 / int(row_obj[0].values[6]))
        )

    def clear_entry_for_button():
        global entry_prldate
        entry_jgid.configure(state="enabled")
        btn_print.configure(state="disabled")
        btn_payment.configure(state="disabled")
        btn_update.configure(state="disabled")
        entry_prldate.destroy()
        entry_prldate = DateEntry(
            entry_frame,
            width=10,
            bootstyle="secondary",
            # startdate=prl_date,
            dateformat="%d/%m/%Y",
        )
        # entry_prldate.configure(startdate=prl_date)
        entry_prldate.grid(row=2, column=1, padx=5, pady=10, sticky=W)
        clear_entry()
        btn_save.configure(state="enabled")

    def select_record(e):
        # global record_set
        global entry_prldate, paid_amnt, prl_date, jgid, employee_name, designation, basic_pay, mobile_no
        entry_jgid.configure(state="enabled")
        clear_entry()
        row_obj = table_dt.get_rows(selected=True)
        # record_set +=[x.values for x in row_obj]
        # print(record_set)
        paid_amnt = row_obj[0].values[5]
        # print(row_obj[0].values)
        entry_jgid.insert(0, row_obj[0].values[0])
        entry_name.insert(0, row_obj[0].values[1])
        entry_designation.insert(0, row_obj[0].values[2])
        entry_basic.insert(0, row_obj[0].values[3])
        prl_date = datetime.strptime(row_obj[0].values[6], "%d/%m/%Y")
        entry_mobile.insert(0, row_obj[0].values[7])
        entry_jgid.configure(state="disabled")
        btn_save.configure(state="disabled")
        btn_print.configure(state="enabled")
        btn_payment.configure(state="enabled")
        btn_update.configure(state="enabled")
        payment_status.configure(
            subtext=f"পরিশোধঃ৳{func.enTobnNumber(func.intcomma_bd(paid_amnt))}/-",
            amountused=(
                round((int(row_obj[0].values[5]) / int(row_obj[0].values[4])) * 100, 1)
            ),  # (1245031 / int(row_obj[0].values[6]))
        )
        entry_prldate.destroy()
        entry_prldate = DateEntry(
            entry_frame,
            width=10,
            bootstyle="secondary",
            startdate=prl_date,
            dateformat="%d/%m/%Y",
        )
        jgid = entry_jgid.get()
        employee_name = entry_name.get()
        designation = entry_designation.get()
        prl_date = entry_prldate.entry.get()
        basic_pay = entry_basic.get()
        mobile_no = entry_mobile.get()
        entry_prldate.configure(startdate=prl_date)
        entry_prldate.grid(row=2, column=1, padx=5, pady=10, sticky=W)

    def add_new():
        jgid = entry_jgid.get()
        employee_name = entry_name.get()
        designation = entry_designation.get()
        prl_date = entry_prldate.entry.get()
        basic_pay = entry_basic.get()
        mobile_no = entry_mobile.get()

        if (
            jgid.strip() == ""
            or employee_name.strip() == ""
            or designation.strip() == ""
            or basic_pay.strip() == ""
            or mobile_no.strip() == ""
        ):
            msg = Messagebox.show_info(
                "ফরমের সকল তথ্য অবশ্যিক!",
                "তথ্য পুরণ নিশ্চিত করণ",
                parent=button_frame,
                alert=True,
            )
        else:
            conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
            c = conn.cursor()
            query = f"SELECT * FROM Employee WHERE JGID = '{jgid.strip()}';"
            c.execute(query)
            user_record = c.fetchall()
            conn.commit()
            conn.close()
            if user_record == []:
                entry_prldate.configure(startdate=prl_date)
                conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
                msgtxt = f"আপনি কি নিম্নবর্নিত কর্মকর্তাকে যোগ করতে চান?\n"
                msgtxt += f"{'-'*len(msgtxt)}\n"
                msg = Messagebox.okcancel(
                    (
                        f"{msgtxt}"
                        f"জেজি আইডি: {func.enTobnNumber(jgid)},\n"
                        f"নামঃ {employee_name}\n"
                        f"পদবীঃ {designation}\n"
                        f"মূল বেতনঃ ৳ {func.enTobnNumber(func.intcomma_bd(basic_pay))}\n"
                        f"পিআরএল তারিখঃ {func.dateINbangla(datetime.strptime(prl_date, '%d/%m/%Y'))}"
                    ),
                    "নতুন কর্মকর্তা যোগ করণের সতর্ক বার্তা!",
                    parent=button_frame,
                    alert=True,
                )
                if msg == "OK":
                    c = conn.cursor()
                    c.execute(
                        """INSERT INTO Employee (JGID, EmployeeName, Designation, BasicPay, AmountToPay, PRLDate, MobileNo) 
                            VALUES (:JGID, :EmployeeName, :Designation, :BasicPay, :AmountToPay, :PRLDate, :MobileNo)""",
                        {
                            "JGID": jgid,
                            "EmployeeName": employee_name,
                            "Designation": designation,
                            "BasicPay": basic_pay,
                            "AmountToPay": func.welfare_fund_calculation(basic_pay),
                            "PRLDate": datetime.strptime(prl_date, "%d/%m/%Y").strftime(
                                "%Y-%m-%d"
                            ),
                            "MobileNo": mobile_no,
                        },
                    )
                    conn.commit()
                    conn.close()
                    table_dt.destroy()
                    populate_data_in_table()
                    paid_amount = 0
                    toast_msg()
                    create_pdf(
                        jgid,
                        employee_name,
                        designation,
                        prl_date,
                        basic_pay,
                        paid_amount,
                        True,  # is_new Entry
                    )
                    entry_jgid.configure(state="disabled")
                    clear_entry()
                    btn_save.configure(state="disabled")
                    btn_print.configure(state="enabled")
                    btn_payment.configure(state="enabled")
                    btn_update.configure(state="enabled")
            else:
                msg = Messagebox.show_info(
                    f"জেজিআইডিঃ {user_record[0][1]} \n নামঃ {user_record[0][2]} \n--এর তথ্য ইতোমধ্যে অন্তর্ভুক্ত করা হয়েছে।",
                    "ডুপ্লিকেট এন্ট্রি!",
                    parent=button_frame,
                    alert=True,
                )

    def update_record():
        jgid = entry_jgid.get()
        employee_name = entry_name.get()
        designation = entry_designation.get()
        prl_date = entry_prldate.entry.get()
        basic_pay = entry_basic.get()
        mobile_no = entry_mobile.get()
        total_amount_to_pay = func.welfare_fund_calculation(basic_pay)

        msgtxt = f"আপনি কি নিম্নবর্নিত তথ্য হালনাগাদ করতে চান?\n"
        msgtxt += f"{'-'*len(msgtxt)}\n"
        msg = Messagebox.okcancel(
            (
                f"{msgtxt}"
                f"জেজি আইডি: {func.enTobnNumber(jgid)},\n"
                f"নামঃ {employee_name}\n"
                f"পদবীঃ {designation}\n"
                f"মূল বেতনঃ ৳ {func.enTobnNumber(func.intcomma_bd(basic_pay))}\n"
                f"পিআরএল তারিখঃ {func.dateINbangla(datetime.strptime(prl_date, '%d/%m/%Y'))}"
            ),
            "তথ্য হালনাগাদ করণের সতর্ক বার্তা!",
            parent=button_frame,
            alert=True,
        )
        if msg == "OK":
            conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
            c = conn.cursor()
            c.execute(
                """UPDATE Employee set  EmployeeName =:EmployeeName, Designation =:Designation, 
                    BasicPay=:BasicPay, AmountToPay=:AmountToPay, PRLDate = :PRLDate, MobileNo =:MobileNo 
                    WHERE JGID=:JGID""",
                {
                    "JGID": jgid,
                    "EmployeeName": employee_name,
                    "Designation": designation,
                    "BasicPay": basic_pay,
                    "AmountToPay": total_amount_to_pay,
                    "PRLDate": datetime.strptime(prl_date, "%d/%m/%Y").strftime(
                        "%Y-%m-%d"
                    ),
                    "MobileNo": mobile_no,
                },
            )
            conn.commit()
            conn.close()
            table_dt.destroy()
            populate_data_in_table()
            create_pdf(
                jgid, employee_name, designation, prl_date, basic_pay, paid_amnt, True
            )
            clear_entry()

    #! Fields name of table Payment =====
    # def create_pdf_file():
    #     create_pdf(jgid, employee_name, designation, prl_date, basic_pay, paid_amnt)

    # def show_message():
    #     msg = Messagebox.show_info(
    #         f"""🌼🌸কল্যান তহবিল থেকে \nমোট দেয় অর্থের পরিমানঃ {func.welfare_fund_calculation(entry_basic.get())}\nপিআরএল তারিখঃ {datetime.strptime(entry_prldate.entry.get(),"%d/%m/%Y").strftime('%d %b %Y')}""",
    #         title="Welfare Fund amount",
    #         parent=entry_frame_left,
    #         alert=True,
    #         padding=(10, 10),
    #     )

    def toast_msg():
        toast = ToastNotification(
            title="নতুন কর্মকর্তার তথ্য যোগ",
            message="কর্মকর্তার তথ্য যোগ করা হয়েছে",
            icon="🌼🌸",
            bootstyle=DANGER,
            duration=2000,
        )
        toast.show_toast()

    header_frame = ttkb.Frame(
        main_frm,
        bootstyle="success",
    )
    # pyglet.font.add_file('banglafont\Padmo UNICODE.ttf')

    # custom_font = font.Font(family="Serif", size=14, file="banglafont/Nikosh")
    heading_label = ttkb.Label(
        header_frame,
        text="কল্যান তহবিল থেকে পরিশোধিত অর্থের বিস্তারিত তথ্য",
        bootstyle="success, inverse",
        padding=3,
    )
    #! relative_path = "=banglafont\\Padmo UNICODE.ttf"
    #! font_path = os.path.join(base_url, relative_path)
    #! masud_font = Font(heading_label, file=font_path)
    masud_font = "Nikosh"

    heading_label.config(font=(masud_font, 16))  # ("Nikosh", 14)
    heading_label.pack(pady=10)
    header_frame.pack(fill=X, padx=5, pady=10)

    #! ttk_line = ttkb.Separator(root, bootstyle="white")
    #! ttk_line.pack(fill=X, padx=5, expand=False)
    entry_frame_root = ttkb.Frame(main_frm)
    entry_frame_root.pack(fill=X, padx=0)

    entry_frame_left = ttkb.Frame(
        entry_frame_root,
    )  # width=710, height=100
    entry_frame_right = ttkb.Frame(
        entry_frame_root,
    )  # width=450, height=100

    entry_frame = ttkb.Labelframe(
        entry_frame_left, text="সাধারণ তথ্যঃ", bootstyle="secondary"
    )
    # entry_frame.columnconfigure(0, weight=1)
    # entry_frame.columnconfigure(3, weight=3)

    label_jgid = ttkb.Label(entry_frame, text="জেজি আইডিঃ ", font=("Nikosh", 12))
    label_name = ttkb.Label(entry_frame, text="নামঃ ", font=("Nikosh", 12))
    label_designation = ttkb.Label(entry_frame, text="পদবীঃ ", font=("Nikosh", 12))
    label_basic = ttkb.Label(entry_frame, text="মূল বেতনঃ ", font=("Nikosh", 12))
    label_prldate = ttkb.Label(entry_frame, text="পিআরএল তারিখঃ ", font=("Nikosh", 12))
    label_mobile = ttkb.Label(entry_frame, text="মোবাইল নংঃ ", font=("Nikosh", 12))

    entry_jgid = ttkb.Entry(
        entry_frame,
        width=10,
    )
    entry_name = ttkb.Entry(
        entry_frame,
        width=32,
    )
    entry_designation = ttkb.Entry(
        entry_frame,
        width=32,
    )
    entry_basic = ttkb.Entry(
        entry_frame,
        width=10,
    )

    entry_prldate = DateEntry(
        entry_frame,
        # style='TCalendar',
        width=10,
        bootstyle="secondary",
        # startdate = prl_date,
        dateformat="%d/%m/%Y",
    )
    entry_prldate.configure(
        startdate=date(2021, 3, 15),
        # state="disabled",
    )
    entry_mobile = ttkb.Entry(entry_frame)

    label_jgid.grid(row=0, column=0, padx=5, pady=10, sticky=E)
    entry_jgid.grid(row=0, column=1, padx=5, pady=10, sticky=W)
    label_name.grid(row=0, column=2, padx=5, pady=10, sticky=E)
    entry_name.grid(row=0, column=3, padx=5, pady=10, sticky=W)
    label_basic.grid(row=1, column=0, padx=5, pady=10, sticky=E)
    entry_basic.grid(row=1, column=1, padx=5, pady=10, sticky=W)
    label_designation.grid(row=1, column=2, padx=5, pady=10, sticky=E)
    entry_designation.grid(row=1, column=3, padx=5, pady=10, sticky=W)
    label_prldate.grid(row=2, column=0, padx=5, pady=10, sticky=W)
    # entry_prldate.grid(row=2, column=1, padx=5, pady=10, sticky=W)

    # entry_prldate["state"] = "readonly"
    label_mobile.grid(row=2, column=2, padx=5, pady=10, sticky=W)
    entry_mobile.grid(row=2, column=3, columnspan=3, padx=5, pady=10, sticky=W)

    entry_frame.pack(padx=5, pady=0)
    entry_frame_left.pack(side=LEFT)

    # entry_frame_left.configure(state="disabled")
    # success colored meter with warning colored subtext
    total_amount_to_paid = 500000
    paid_amount = 180000
    payment_status = ttkb.Meter(
        master=entry_frame_right,
        metersize=140,
        padding=0,
        amountused=20,
        # metertype='semi',
        # subtext=f"Paid:{paid_amount}",
        interactive=True,
        # textfont=["B", 18],
        subtextfont=["Nikosh", 9],
        # button_frame,
        # metersize=100,
        # # metertype='semi',
        # labeltext="project completion",
        # bootstyle="success",
        # subtextstyle="warning",
    )
    payment_status.configure(
        amounttotal=100,
        amountused=((paid_amount / total_amount_to_paid) * 100),
        interactive=True,
        textright="%",
        stripethickness=2,
    )
    payment_status.pack(padx=10, pady=5)
    # Style.configure('custom.TLabel', background='red', foreground='white', font=('Helvetica', 24))

    entry_frame_right.pack(fill=X)

    button_frame = ttkb.Frame(main_frm)
    btn_save = ttkb.Button(
        button_frame,
        text="Add Entry",
        width=10,
        bootstyle=SUCCESS,
        command=add_new,
    )
    btn_save.configure(state="disabled")

    btn_clear = ttkb.Button(
        button_frame,
        text="Clear Entry",
        width=10,
        bootstyle=(INFO, OUTLINE),
        command=clear_entry_for_button,
    )
    btn_update = ttkb.Button(
        button_frame,
        text="Update",
        width=10,
        bootstyle=(SUCCESS),
        command=update_record,
    )

    btn_payment = ttkb.Button(
        button_frame, text="Payment", width=10, bootstyle="info", command=add_payment
    )
    btn_exit = ttkb.Button(
        button_frame,
        text="Exit",
        width=10,
        bootstyle="warning",
        command=lambda: main.destroy(),
    )
    btn_print = ttkb.Button(
        button_frame,
        text="Print",
        width=10,
        bootstyle="danger",
        command=lambda: create_pdf(
            jgid,
            employee_name,
            designation,
            prl_date,
            basic_pay,
            paid_amnt,
            False,
        ),
    )

    payment_status_summary = ttkb.Label(
        button_frame,
        text=f"""মোট পরিশোধিতব্যঃ {func.enTobnNumber(func.intcomma_bd(int(query_database()['payment_remaining'][0][0]) - 
                int(query_database()['payment_remaining'][0][1])))}/-""",
        font=("Nikosh", 12),
        style="success.Inverse.TLabel",
        bootstyle="danger",
        # background="skyblue4",
        relief="flat",  # flat, groove, raised, ridge, solid, sunken
        # width=50,
        padding=3,
        justify="center",  # left, right, center
    )

    btn_save.pack(fill=X, side=LEFT, padx=4, pady=5)
    # btn_show.pack(fill=X, side=LEFT, padx=5, pady=5)
    btn_clear.pack(fill=X, side=LEFT, padx=4, pady=5)
    btn_update.pack(fill=X, side=LEFT, padx=4, pady=5)
    btn_payment.pack(fill=X, side=LEFT, padx=4, pady=5)
    btn_print.pack(fill=X, side=LEFT, padx=4, pady=5)
    btn_exit.pack(fill=X, side=LEFT, padx=4, pady=5)
    payment_status_summary.pack(padx=5, pady=5)
    button_frame.pack(fill=X, pady=5)

    # colors = main_frm.style.colors
    coldata = [
        {
            "text": "আইডি",
            # "minwidth": 10,
            "width": 70,
            "stretch": False,
            "anchor": "w",
            # "command": show_message,
        },
        {"text": "নাম", "width": 300, "stretch": False},
        {"text": "পদবী", "width": 230, "stretch": False},
        {
            "text": "শেষ ব্যসিক",
            "width": 110,
            "stretch": False,
        },
        {
            "text": "দেয় অর্থ",
            "width": 105,
            "stretch": False,
        },
        {
            "text": "পরিশোধিত",
            "width": 105,
            "stretch": False,
        },
        {
            "text": "পিআরএল তাং",
            "width": 130,
            "stretch": False,
        },
        {
            "text": "মোবাইল",
            "width": 130,
            "stretch": False,
        },
    ]

    def populate_data_in_table():
        global table_dt
        items = query_database()["all_records"]
        rowdata = [
            [
                item[0],
                item[1],
                item[2],
                item[3],
                item[4],
                item[7],
                item[5],
                item[6],
            ]
            for item in items
        ]
        table_dt = Tableview(
            master=main_frm,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=True,
            # bootstyle=SUCCESS,
            pagesize=10,
            height=10,
            stripecolor=("antiquewhite", None),
        )
        # table_dt.configure()
        # table_dt.autofit_columns()
        table_dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        table_dt.bind_all("<<TreeviewSelect>>", select_record)

        table_rows = table_dt.tablerows

    populate_data_in_table()
    main_frm.mainloop()
