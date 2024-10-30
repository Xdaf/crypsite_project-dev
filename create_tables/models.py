from django.db import models

# Модель бирж.
class Exchange(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name
    
# Модель для представления валютных пар для покупки.
class CurrencyPairBuy(models.Model):
    symbol = models.CharField(max_length=10)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    buying_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.symbol    
        
# Модель для представления комбинаций покупки и продажи.
class Combination(models.Model):
    currency_pair_buy = models.ForeignKey(CurrencyPairBuy, related_name="buy_pair", on_delete=models.CASCADE)
    currency_pair_sell = models.ForeignKey(CurrencyPairBuy, related_name="sell_pair", on_delete=models.CASCADE)
    profit = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self) -> str:
        return f"""| Buy: | {self.currency_pair_buy.symbol} |
                            {self.currency_pair_buy.exchange} |
                            {self.currency_pair_buy.buying_price} | 
                            --> | Sell: | {self.currency_pair_buy.symbol} | 
                            {self.currency_pair_buy.exchange} | 
                            {self.currency_pair_buy.selling_price} | 
                            == | profit: | {self.profit} |"""