from . import shamsi
from zipfile import ZipFile
from django.utils import timezone


def price_amount(data):

    english_to_persian = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }

    add_number = ""
    for digit in str(data):
        add_number += english_to_persian.get(digit, "شما باید حتما عدد وارد کنید!")

    save_num = []
    while add_number:
        save_num.append(add_number[-3:])
        add_number = add_number[:-3]
        jo = "/".join(save_num[::-1])
    return f"{jo} تومان"


def converter_date_time(time):
    allmonth = [
        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند",
    ]
    timezone.localtime(time)
    time_to_str = time.year, time.month, time.day
    time_to_tuple = shamsi.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(allmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    output = "{}{}{}, ساعت {}:{}".format(
        time_to_list[2], time_to_list[1], time_to_list[0], time.hour, time.minute
    )
    return output


def zip_voice(value):
    with ZipFile('mediafile/all_voices', 'a') as filezip:
        filezip.write(value)

