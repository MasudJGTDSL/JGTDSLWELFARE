from JGWELFARE_FUND_base import base_url, subprocess, func, datetime, date
import sqlite3
from weasyprint import HTML, CSS


def query_database():
    conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
    c = conn.cursor()
    # c_all = conn.cursor()

    query_payment_pending = """SELECT * FROM (
            SELECT substr('000'||a.JGID, -3,3) as JGID, 
            a.EmployeeName, a.Designation, a.PRLDate, a.BasicPay, a.AmountToPay, 
            SUM(IFNULL(b.PaidAmount,0)) as PaidAmount
            FROM Employee a LEFT JOIN Payment b ON a.JGID = b.JGID GROUP BY a.JGID) a WHERE a.AmountToPay > a.PaidAmount;
            """

    c.execute(query_payment_pending)
    payment_pending_records = c.fetchall()

    c_all = conn.cursor()
    query_payment_all = """SELECT substr('000'||a.JGID, -3,3) as JGID, 
        a.EmployeeName, a.Designation, a.PRLDate, a.BasicPay, a.AmountToPay, 
        SUM(IFNULL(b.PaidAmount,0)) as PaidAmount
        FROM Employee a LEFT JOIN Payment b ON a.JGID = b.JGID GROUP BY a.JGID;
        """
    c_all.execute(query_payment_all)
    payment_all_records = c_all.fetchall()
    # single_c = conn.cursor()
    # single_c.execute(
    #     f"""SELECT * FROM (SELECT a.JGID, a.EmployeeName, a.Designation, a.BasicPay, a.AmountToPay, a.PRLDate, a.MobileNo,
    #     b.id, b.PaidAmount, b.PaymentDate, b.Remarks
    #     FROM Employee a LEFT JOIN Payment b on a.JGID = b.JGID) c WHERE JGID = '{int(jgid)}'"""
    # )
    # single_record = single_c.fetchall()

    # payment_c = conn.cursor()
    # payment_c.execute(
    #     """SELECT SUM(a.AmountToPay) as TotalAmountToPay, SUM(b.PaidAmount) as TotalPaidAmount
    #     FROM Employee a LEFT JOIN Payment b on a.JGID = b.JGID
    #     """
    # )
    # payment_remaining = payment_c.fetchall()

    # single_c_summary = conn.cursor()

    # single_c_summary.execute(f"{query_payment_pending} WHERE a.JGID ={int(jgid)} GROUP BY a.JGID")
    # single_record_summary = single_c_summary.fetchone()

    conn.commit()
    conn.close()
    return {
        # "all_records": all_records,
        "payment_pending_records": payment_pending_records,
        "payment_all_records": payment_all_records,
        # "single_record_summary": single_record_summary,
    }


def payment_info(jgid):
    conn = sqlite3.connect("JG_WELFARE_FUND.sqlite3")
    c = conn.cursor()
    query_payment_details = f"SELECT * FROM Payment WHERE JGID={jgid}"

    c.execute(query_payment_details)
    payment_details_records = c.fetchall()
    return payment_details_records


def create_pdf(
    jgid, employee_name, designamtion, prl_date, basic_pay, paid_amount, is_new
):
    if is_new == True:
        mar_left, pad_left = 50, 30
    else:
        mar_left, pad_left = 10, 10

    if is_new == False:
        payment_list = payment_info(int(jgid))
        if is_new == False and payment_list == []:
            mar_left, pad_left = 50, 30

    html_string = """<html>
    <head>
        <link  rel="stylesheet" type="text/css" href="static/bootstrap.min.css">
    <link  rel="stylesheet" type="text/css" href="static/rana.css">
        <style>
        @page {
        size: a5 portrait;
        margin: 15mm 15mm 15mm 15mm;
        counter-increment: page;
        @bottom-right {
            font-family: 'Times New Roman';
            content: 'Page No : ' counter(page);
            white-space: pre;
            color: grey;
        }
        }
        h, p {
        margin-top:0;
        margin-bottom:0;
        text-align:center;
        font-weight: bold;
        }
        h2 {color:red;
        margin-top:0;
        margin-bottom:0;
        text-align:center;}
        th, td {
        padding: 2px;
        # text-align: left;
        }
        h3 {margin-bottom:0;
        padding-bottom: 0px;}
        .tbltbl {
        width: 100%;
        border-collapse: collapse;
        }
        .tbltd {
        text-align:center;
        width:20%;
        }
        </style>
    </head>
    <body>"""
    html_string += f"""<h2><img src="images\JGICON.jpg" alt='JG' style='width: 38px; height: 38px'/>"""
    html_string += """<span class="b_fontpadmo">&nbsp;জালালাবাদ গ্যাস টি এ্যান্ড ডি সিস্টেম লিঃ</span></h2>
    <p class="b_fontNikosh">(পেট্রোবাংলার একটি কোম্পানি)</p>
    <h3 class="b_fontNikosh text-danger" style = 'border:1px; text-align:center;'>‍গ্যাস ভবন, মেন্দিবাগ, সিলেট।</h3>
    <hr style='padding-top: 0px;padding-bottom: 0px; margin-top:0; margin-bottom:0;'>"""

    html_string += f"<p class='b_fontNikosh' style = 'text-align:right; padding-top: 0px; padding-bottom: 0px; margin-top:0; margin-bottom:2;font-weight: normal;'>তারিখঃ {func.dateINbangla(date.today())}</p>"
    html_string += f"""<h4 class="b_fontNikosh text-danger" style = 'border:1px; text-align:left;'>বিষয়ঃ <strong><u>কল্যান তহবিল থেকে দেয় ও প্রদানকৃত অর্থের হিসাব।</u></strong></h4>
    <div style='margin-left:{mar_left}px; padding-left:{pad_left}px;'><table>"""

    html_string += f"<tr><th class='b_fontNikosh' style = 'text-align:right;'>জেজি আইডিঃ</th><th class='b_fontNikosh'>{func.enTobnNumber(jgid)}</th></tr>"
    html_string += f"<tr><td class='b_fontNikosh' style = 'text-align:right;'>নামঃ</td><th class='b_fontNikosh' style='font-weight: bold;'>{employee_name}</th></tr>"
    html_string += f"<tr><td class='b_fontNikosh' style = 'text-align:right;'>পদবীঃ</td><td class='b_fontNikosh'>{designamtion}</td></tr>"
    html_string += f"<tr><td class='b_fontNikosh' style = 'text-align:right;'>পিআরএল তারিখঃ</td><td class='b_fontNikosh'>{func.dateINbangla(datetime.strptime(prl_date,'%d/%m/%Y'))}</td></tr>"
    html_string += f"<tr><td class='b_fontNikosh' class='b_fontNikosh text-danger' style = 'text-align:right;'>সর্বশেষ মূল বেতনঃ</td><td class='b_fontNikosh' style='font-weight: bold;'>{func.enTobnNumber(func.intcomma_bd(int(basic_pay)))}/-</td></tr>"
    html_string += f"<tr><td class='b_fontNikosh' style = 'text-align:right;'>সর্বমোট দেয় অর্থঃ</td><td class='b_fontNikosh'>{func.enTobnNumber(str(func.intcomma_bd(func.welfare_fund_calculation(int(basic_pay)))))}/-</td></tr>"
    if is_new == False:
        if payment_list != []:
            html_string += "<tr><td class='b_fontNikosh' style='text-align:right;'>পরিশোধিত অর্থঃ</td><td></td></tr>"
            html_string += f"""<tr>
                <td class='b_fontNikosh' style = 'text-align:right;'></td>
                <td>
                <table class ='tbltbl'><tr>
                <td class='b_fontNikosh' style="border: 1px solid; text-align:center; height: 15px;">তারিখ</td>
                <td class='b_fontNikosh' style="border: 1px solid; text-align:center; height: 15px; width:200px;">টাকা</td></tr>"""
            for row in payment_list:
                html_string += f"""
                <tr>
                <td class='b_fontNikosh' style="border: 1px solid; height: 15px;">{func.dateINbangla(datetime.strptime(row[2],'%Y-%m-%d'))}</td>
                <td class='b_fontNikosh' style="border: 1px solid; height: 15px; text-align:center;">{func.enTobnNumber(str(func.intcomma_bd(int(row[1]))))}/-</td>
                </tr>"""
            html_string += "</table></td></tr>"
        html_string += f"<tr><td class='b_fontNikosh' style = 'text-align:right;'>মোট পরিশোধিত অর্থঃ</td><td class='b_fontNikosh'>{func.enTobnNumber(str(func.intcomma_bd(int(paid_amount))))}/-</td></tr>"
        html_string += f"<tr><td class='b_fontNikosh' style = 'text-align:right;'>অবশিষ্ট দেয়ঃ</td><td class='b_fontNikosh'>{func.enTobnNumber(str(func.intcomma_bd(func.welfare_fund_calculation(int(basic_pay))-int(paid_amount))))}/-</td></tr>"

    html_string += """</table></div><div style='padding-top:50px;'><table style='width: 100%;'>
                    <tr>
                    <td></td>
                    <td class='tbltd b_fontNikosh' style="border-top: 1px solid;">প্রস্তুতকারী</td>
                    <td class='tbltd'></td>
                    <td class='tbltd b_fontNikosh' style="border-top: 1px solid;">ব্যবস্থাপক</td>
                    <td class='tbltd'></td>
                    </tr>
                    </table></div> 
                    <script src="static/bootstrap.min.js"></script></body></html>"""
    html_doc = HTML(string=html_string, base_url=base_url)

    # html = HTML(string=source_html, base_url=base_url)
    css1 = CSS("static/bootstrap.min.css", base_url=base_url)
    css2 = CSS("static/rana.css", base_url=base_url)
    # html.write_pdf(output_filename, stylesheets=[css])

    html_doc.write_pdf(f"pdf\{jgid}.pdf", stylesheets=[css1])
    subprocess.Popen(f"pdf\{jgid}.pdf", shell=True)


def pending_payment_list(is_all):
    if is_all == True:
        items = query_database()["payment_all_records"]
    else:
        items = query_database()["payment_pending_records"]

    html_string = """<html>
    <head>
        <link  rel="stylesheet" type="text/css" href="static/bootstrap.min.css">
    <link  rel="stylesheet" type="text/css" href="static/rana.css">
        <style>
        @page {
        size: a4 landscape;
        margin: 15mm 15mm 15mm 15mm;
        counter-increment: page;
        @bottom-right {
            font-family: 'Times New Roman';
            content: 'Page No : ' counter(page);
            white-space: pre;
            color: grey;
        }
        }
        h, p {
        margin-top:0;
        margin-bottom:0;
        text-align:center;
        font-weight: bold;
        }
        h2 {color:red;
        margin-top:0;
        margin-bottom:0;
        text-align:center;}
        th, td {
        padding: 2px;
        # text-align: left;
        }
        h3 {margin-bottom:0;
        padding-bottom: 0px;}

        .tbltbl {
        width: 100%;
        border: 1px solid black;
        border-collapse: collapse;
        }

        .tbltd {
        text-align:center;
        font-size:14pt;
        border: 1px solid black;
        # width:20%;
        }
        </style>
    </head>
    <body>"""
    html_string += f"""<h2><img src="images\JGICON.jpg" alt='JG' style='width: 38px; height: 38px'/>"""
    html_string += """<span class="b_fontpadmo">&nbsp;জালালাবাদ গ্যাস টি এ্যান্ড ডি সিস্টেম লিঃ</span></h2>
    <p class="b_fontNikosh">(পেট্রোবাংলার একটি কোম্পানি)</p>
    <h3 class="b_fontNikosh text-danger" style = 'border:1px; text-align:center;'>‍গ্যাস ভবন, মেন্দিবাগ, সিলেট।</h3>
    <hr style='padding-top: 0px;padding-bottom: 0px; margin-top:0; margin-bottom:0;'>"""

    html_string += f"<p class='b_fontNikosh' style = 'text-align:right; padding-top: 0px; padding-bottom: 0px; margin-top:0; margin-bottom:2;font-size: 14pt;'>তারিখঃ {func.dateINbangla(date.today())}</p>"
    if is_all == True:
        html_string += "<h2 class='b_fontNikosh' style = 'border:1px; text-align:left; color:black;'>বিষয়ঃ <strong><u>কল্যান তহবিল থেকে দেয় ও প্রদানকৃত অর্থের তালিকা (সকল)।</u></strong></h2>"
    else:
        html_string += "<h2 class='b_fontNikosh' style = 'border:1px; text-align:left; color:black;'>বিষয়ঃ <strong><u>কল্যান তহবিল থেকে পরিশোধ চলমান কর্মকর্তা/কর্মচারীদের দেয় ও প্রদানকৃত অর্থের তালিকা।</u></strong></h2>"

    html_string += "<div><table class ='tbltbl'><thead><tr>"

    html_string += f"<th rowspan='2' class='b_fontNikosh tbltd' style = 'text-align:center;'>#</th>"
    html_string += f"<th rowspan='2' class='b_fontNikosh tbltd' style = 'text-align:center;'>জেজি আইডি</th>"
    html_string += f"<th rowspan='2' class='b_fontNikosh tbltd' style = 'text-align:center;'>নাম</th>"
    html_string += f"<th rowspan='2' class='b_fontNikosh tbltd' style = 'text-align:center;'>পদবী</th>"
    html_string += f"<th rowspan='2' class='b_fontNikosh tbltd' style = 'text-align:center;'>পিআরএল তারিখ</th>"
    html_string += f"<th rowspan='2' class='b_fontNikosh tbltd' class='b_fontNikosh text-danger' style = 'text-align:center;'>সর্বশেষ মূল বেতন</th>"

    html_string += f"<th colspan='3' class='b_fontNikosh tbltd' class='b_fontNikosh text-danger' style = 'text-align:center;'>দেয় ও প্রদানকৃত অর্থের হিসাব</th></tr><tr>"
    html_string += (
        f"<th class='b_fontNikosh tbltd' style = 'text-align:center;'>মোট দেয়</th>"
    )
    html_string += (
        f"<th class='b_fontNikosh tbltd' style = 'text-align:center;'>পরিশোধিত</th>"
    )
    html_string += f"<th class='b_fontNikosh tbltd' style = 'text-align:center;'>অবশিষ্ট</th></tr></thead><tbody>"
    # 0 জেজি আইডি, 1 নাম, 2 পদবী, 3 পিআরএল তারিখ, 4 সর্বশেষ মূল বেতন, 5 সর্বমোট দেয়, 6 পরিশোধিত, 7 অবশিষ্ট
    sl = 0
    total_payable = 0
    total_paid = 0
    total_remain_payment = 0
    for item in items:
        sl += 1
        total_payable += int(item[5])
        total_paid += int(item[6])
        total_remain_payment += int(item[5]) - int(item[6])

        html_string += (
            f"<tr><td class='b_fontNikosh tbltd'>{func.enTobnNumber(str(sl))}</td>"
        )
        html_string += (
            f"<td class='b_fontNikosh tbltd'>{func.enTobnNumber(item[0])}</td>"
        )
        html_string += f"<td class='b_fontNikosh tbltd' style='font-weight: bold; text-align:left;'>{item[1]}</td>"
        html_string += f"<td class='b_fontNikosh tbltd'>{item[2]}</td>"
        html_string += f"<td class='b_fontNikosh tbltd'>{func.dateINbangla(datetime.strptime(item[3],'%Y-%m-%d'))}</td>"  # item[3]
        html_string += f"<td class='b_fontNikosh tbltd' style='font-weight: bold;'>{func.enTobnNumber(func.intcomma_bd(int(item[4])))}/-</td>"
        html_string += f"<td class='b_fontNikosh tbltd'>{func.enTobnNumber(str(func.intcomma_bd(int(item[5]))))}/-</td>"
        html_string += f"<td class='b_fontNikosh tbltd'>{func.enTobnNumber(str(func.intcomma_bd(int(item[6]))))}/-</td>"
        html_string += f"<td class='b_fontNikosh tbltd'>{func.enTobnNumber(str(func.intcomma_bd(int(item[5])-int(item[6]))))}/-</td></tr>"

    html_string += f"<tr><th colspan='6' class='b_fontNikosh tbltd' style = 'text-align:right;'>সর্বমোট = </th>"
    html_string += f"<th class='b_fontNikosh tbltd' style = 'text-align:center;'>{func.enTobnNumber(str(func.intcomma_bd(total_payable)))}</th>"
    html_string += f"<th class='b_fontNikosh tbltd' style = 'text-align:center;'>{func.enTobnNumber(str(func.intcomma_bd(total_paid)))}</th>"
    html_string += f"<th class='b_fontNikosh tbltd' style = 'text-align:center;'>{func.enTobnNumber(str(func.intcomma_bd(total_remain_payment)))}</th></tr>"

    html_string += """</tbody></table></div><div style='padding-top:70px;'><table style='width: 100%;'>
                    <tr>
                    <td></td>
                    <td></td>
                    <td class='b_fontNikosh' style="text-align:center; border-top: 1px solid; font-size:14pt;">প্রস্তুতকারী</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td class='b_fontNikosh' style="text-align:center; border-top: 1px solid; font-size:14pt;">ব্যবস্থাপক</td>
                    <td></td>
                    <td></td>
                    </tr>
                    </table></div> 
                    <script src="static/bootstrap.min.js"></script></body></html>"""
    html_doc = HTML(string=html_string, base_url=base_url)

    # html = HTML(string=source_html, base_url=base_url)
    css1 = CSS("static/bootstrap.min.css", base_url=base_url)
    css2 = CSS("static/rana.css", base_url=base_url)
    # html.write_pdf(output_filename, stylesheets=[css])

    if is_all == True:
        html_doc.write_pdf(
            f"pdf\Reports\{'Payment_all_' + date.today().strftime('%Y%m%d')}.pdf",
            stylesheets=[css1],
        )
        subprocess.Popen(
            f"pdf\Reports\{'Payment_all_' + date.today().strftime('%Y%m%d')}.pdf",
            shell=True,
        )
    else:
        html_doc.write_pdf(
            f"pdf\Reports\{'Pending_paid_' + date.today().strftime('%Y%m%d')}.pdf",
            stylesheets=[css1],
        )
        subprocess.Popen(
            f"pdf\Reports\{'Pending_paid_' + date.today().strftime('%Y%m%d')}.pdf",
            shell=True,
        )
