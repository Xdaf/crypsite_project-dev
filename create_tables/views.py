from django.shortcuts import render
import requests
from django.http import JsonResponse
from decimal import Decimal
from .models import CurrencyPairBuy, Exchange, Combination
from django.db import transaction

def index(request):
    # Проверка, является ли запрос AJAX-запросом
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Обновление валютных пар
        update_currency_pairs()
        # Получение всех валютных пар из базы данных
        cur_pair = CurrencyPairBuy.objects.all().values('symbol', 'buying_price')
        # Возврат данных в формате JSON
        return JsonResponse(list(cur_pair), safe=False)
    
    # URL API Binance для получения цен
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        # Отправка GET-запроса к API Binance
        response = requests.get(url)
        data = response.json()
        # Получение объекта биржи Binance из базы данных
        exchange_binance = Exchange.objects.get()

        # Использование транзакции для обеспечения целостности данных
        with transaction.atomic():
            for item in data:
                symbol = item['symbol']
                buying_price = Decimal(item['price'])
                # Обновление или создание записи валютной пары
                CurrencyPairBuy.objects.update_or_create(
                    symbol=symbol,
                    exchange=exchange_binance,
                    defaults={'buying_price': buying_price}
                )
    except Exception as e:
        print(f"Error updating prices: {e}")

    # Получение всех валютных пар и бирж для отображения на странице
    cur_pair = CurrencyPairBuy.objects.all()
    exchanges = set(Exchange.objects.all())
    # Рендеринг шаблона с данными
    return render(request, 'create_tables/index.html', {"content": cur_pair, "exch": exchanges})
 
def update_currency_pairs():
    # URL API Binance для получения цен
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        # Отправка GET-запроса к API Binance
        response = requests.get(url)
        data = response.json()
        # Получение объекта биржи Binance из базы данных
        exchange_binance = Exchange.objects.get()
        
        # Использование транзакции для обеспечения целостности данных
        with transaction.atomic():
            for item in data:
                symbol = item['symbol']
                buying_price = Decimal(item['price'])
                # Обновление или создание записи валютной пары
                CurrencyPairBuy.objects.update_or_create(
                    symbol=symbol,
                    exchange=exchange_binance,
                    defaults={'buying_price': buying_price}
                )
    except Exception as e:
        print(f"Error updating prices: {e}")

def users(request):
    # Рендеринг шаблона страницы пользователей
    return render(request, 'create_tables/users.html')