import json

from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse


def main_page(request):
    return render(request, 'app/main_page.html', {})


def get_count_client(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT count(distinct "Код клиента") from Клиент''')
    result = cursor.fetchone()
    response_data = {
        'data': result[0],
        'status': 200,
        'message': 'Ok.'
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_count_per_user(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT users.*, orders.order_count
    from
    (
        SELECT "Код клиента", count(distinct "Код заказа") as order_count
        from "Заказ клиента" group by "Код клиента"
    ) as orders
    join Клиент as users on orders."Код клиента" == users."Код клиента"''')
    result = cursor.fetchall()

    response_data = [{"Код клиента": obj[0], "Фамилия":obj[1], "Имя":obj[2], "Город":obj[3], "Код заказа":obj[4], "Количество ордеров":obj[5]} for obj in result]

    return HttpResponse(json.dumps(response_data), content_type="application/json")
