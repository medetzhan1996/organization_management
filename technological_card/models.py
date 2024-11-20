from django.db import models
from warehouse.models import Storage, Good


# Технологическая карта
class TechnologicalCard(models.Model):
    title = models.CharField(max_length=180)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_consumables(self):
        return self.consumable_set.all()


# Расходные материалы
class Consumable(models.Model):
    technological_card = models.ForeignKey(TechnologicalCard,
                                           on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage,
                                on_delete=models.CASCADE)
    good = models.ForeignKey(Good,
                             on_delete=models.CASCADE)
    receipt_amount = models.FloatField(default=0)
