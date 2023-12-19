import locale
from decimal import Decimal


def enTobnNumber(Value):
    numEn = "0123456789"
    numBn = "০১২৩৪৫৬৭৮৯"
    x = {}
    #! Adding Item to Dictionary =============
    for i in numEn:
        x[i] = numBn[int(i)]

    result = ""
    for it in Value:  # ! Item in given String Value =====
        if it in x:  # ! if key in Dictionary ========
            result += x[it]
        else:  # ! if key is not in Dictionary ========
            result += it
    return result


def dateINbangla(dateValue):
    day = dateValue.day
    month = dateValue.month
    year = dateValue.year
    monthNameVal = [
        "জানুয়ারি",
        "ফেব্রুয়ারি",
        "মার্চ",
        "এপ্রিল",
        "মে",
        "জুন",
        "জুলাই",
        "আগস্ট",
        "সেপ্টেম্বর",
        "অক্টোবর",
        "নভেম্বর",
        "ডিসেম্বর",
    ][int(month) - 1]
    return enTobnNumber(str(day) + " " + monthNameVal + ", " + str(year))


def intcomma_bd(value, preserve_decimal=False):
    locale.setlocale(locale.LC_ALL, "bn_BD")
    try:
        if not isinstance(value, (int, float, Decimal)):
            value = float(value)
    except (TypeError, ValueError):
        return value
    number_with_coma = locale.format_string("%.0f", value, True)
    return number_with_coma


def welfare_fund_calculation(basic):
    if basic == "":
        last_basic = 0
    else:
        last_basic = int(basic)
    twenty_five_percent_of_basic = last_basic * (0.25)
    cur_two_point_seven_five_percent = 0
    total_amount_to_pay = 0
    x = 0

    while x < 180:
        cur_two_point_seven_five_percent = twenty_five_percent_of_basic * (0.0275)

        total_amount_to_pay += (
            twenty_five_percent_of_basic - cur_two_point_seven_five_percent
        )

        twenty_five_percent_of_basic -= cur_two_point_seven_five_percent

        x += 1

    return int(round(total_amount_to_pay, 0))
