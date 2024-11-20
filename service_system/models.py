from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from technological_card.models import TechnologicalCard
from document_circulation.models import Form
from account.models import Company


# Базовый абстрактный класс
class ItemBase(models.Model):
    title = models.CharField(max_length=180)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# Категория услуг
class CategoryService(ItemBase):
    company = models.ForeignKey('account.Company', on_delete=models.CASCADE)


# Список услуг
class Service(ItemBase, MPTTModel):
    price = models.DecimalField(max_digits=19, decimal_places=0)
    category = models.ForeignKey(CategoryService, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    technological_cards = models.ManyToManyField(TechnologicalCard, blank=True)
    users = models.ManyToManyField('account.User', blank=True)
    equipments = models.ManyToManyField(
        'equipment_system.Equipment', blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')


# Услуги пользователя
class UserService(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    service = models.ForeignKey(Service,
                                related_name='user_services',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=0, null=True)


# Услуги пользователя
class FormService(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True)
