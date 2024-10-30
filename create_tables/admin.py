from django.contrib import admin

from .models import Exchange, CurrencyPairBuy, Combination


admin.site.register(Exchange)
admin.site.register(CurrencyPairBuy)
admin.site.register(Combination)
