from django.db import models
from django.db.models import Sum


# Базовый абстрактный класс
class ItemBase(models.Model):
    title = models.CharField(max_length=180)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# Категория товаров
class CategoryGood(ItemBase):
    company = models.ForeignKey('account.Company',
                                on_delete=models.CASCADE)


# Провайдер
class Provider(ItemBase):
    company = models.ForeignKey('account.Company',
                                on_delete=models.CASCADE)


# Товары
class Good(ItemBase):
    UNIT_CHOICES = (
        (1, "штук"),
        (2, "миллилитр"),
        (3, "грамм"),
        (4, "упаковка"),
        (5, "миллиграмм"),
        (6, "сантиметр"),
        (7, "микролитр"),
        (9, "сетр"),
        (10, "рулон"),
        (11, "литр"),
        (12, "флакон"),
        (13, "единица"),
        (14, "килограмм"),
        (15, "ампула"),
        (16, "коробка"),
        (17, "капсула"),
        (18, "доза"),
        (19, "другое")
    )
    category = models.ForeignKey(CategoryGood,
                                 on_delete=models.CASCADE)
    barcode = models.CharField(max_length=180)
    sale_unit = models.IntegerField(choices=UNIT_CHOICES, default=0)
    write_off_unit = models.IntegerField(choices=UNIT_CHOICES, default=0)
    unit_equals = models.IntegerField(default=0)
    cost = models.DecimalField(
        max_digits=8, decimal_places=1, null=True, blank=True)
    actual_cost = models.DecimalField(
        max_digits=8, decimal_places=1, null=True, blank=True)
    critical_amount = models.IntegerField(default=0, null=True, blank=True)
    desired_amount = models.IntegerField(default=0, null=True, blank=True)


# Склад
class Storage(ItemBase):
    company = models.ForeignKey('account.Company',
                                on_delete=models.CASCADE)


# Складские операции
class StorageOperation(models.Model):
    TYPE_OPERATION = (
        (1, "Приход товара"),
        (2, "Перемещение товара"),
        (3, "Списание товара"),
        (4, "Продажа товара")
    )
    storage = models.ForeignKey(
        Storage, on_delete=models.CASCADE)
    type_operation = models.IntegerField(choices=TYPE_OPERATION, default=0)
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey('customer.Customer',
                                 on_delete=models.CASCADE,
                                 null=True, blank=True)
    user = models.ForeignKey('account.User',
                             on_delete=models.CASCADE)
    company = models.ForeignKey('account.Company',
                                on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


# Товары складской операции
class StorageOperationGood(models.Model):
    storage_operation = models.ForeignKey(
        StorageOperation, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    quantity_write_off = models.FloatField(default=1)

    # Получить остаток товара
    def get_remainder(self, type_operation):
        query = StorageOperationGood.objects.filter(
            id__lte=self.id, storage_operation__type_operation=type_operation,
            storage_operation__storage=self.storage_operation.storage
        )
        return query.aggregate(Sum('quantity')).get('quantity__sum', 0)
