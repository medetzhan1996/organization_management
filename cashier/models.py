from django.db import models
from customer.models import Customer
from register.models import Schedule


# Оплаченный счет клиента
class CustomerPaidInvoice(models.Model):
    PAYMENT_METHOD = (
        ("Наличные", "Наличные"),
        ("Терминал", "Терминал"),
        ("KASPI RED", "KASPI RED"),
        ("KASPI перевод", "KASPI перевод"),
        ("Рассрочка", "Рассрочка"),
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    paid = models.DecimalField(max_digits=6, decimal_places=0)
    date = models.DateTimeField(auto_now_add=True)
    schedule = models.ForeignKey(
        Schedule, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=80, choices=PAYMENT_METHOD,
                                      default="Наличные")
    comment = models.TextField(null=True, blank=True)
