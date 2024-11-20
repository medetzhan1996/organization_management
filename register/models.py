from datetime import timedelta
from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum, Min


class ScheduleQuerySet(QuerySet):

    def filter_content_type(self, model, object=None):
        query = self.filter(content_type=ContentType.objects.get_for_model(
                model))
        if object:
            try:
                query = query.filter(object_id__in=object)
            except TypeError:
                query = query.filter(object_id=object)
        return query

    def filter_by_passed_fields(self, start_date=None, end_date=None, status=None):
        query = self
        if start_date:
            query = query.filter(start_datetime__date__gte=start_date)
        if end_date:
            query = query.filter(start_datetime__date__lte=end_date)
        if status:
            query = query.filter(status=status)
        return query


# График работы
class Schedule(models.Model):
    objects = ScheduleQuerySet.as_manager()
    TIMER_STATUS_CHOICES = (
        (0, "Ожидание"),
        (1, "Пауза"),
        (2, "Завершен")
    )
    STATUS_CHOICES = (
        (0, "Ожидание клиента"),
        (1, "Клиент пришел"),
        (2, "Клиент не пришел"),
        (3, "клиент подтвердил")
    )
    customer = models.ForeignKey(
        'customer.Customer', on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        limit_choices_to={'model__in': ('equipment', 'user')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    start_datetime = models.DateTimeField()
    duration = models.IntegerField(default=30)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    comment = models.TextField(blank=True, null=True)
    register = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='schedule_register', blank=True, null=True)

    @property
    def end_datetime(self):
        end_datetime = self.start_datetime + timedelta(minutes=self.duration)
        return end_datetime

    @property
    def start_time(self):
        return self.start_datetime.time()

    def get_invoice(self):
        invoice = sum([
            (data.quantity * data.price) - (data.discount / 100) * data.price
            for data in self.scheduleservice_set.filter(
                status_payment=0).all()])
        return int(invoice)

    def get_paid(self):
        paid = sum([
            data.paid
            for data in self.customerpaidinvoice_set.all()])
        return int(paid)

    def get_services(self):
        return self.scheduleservice_set.all()


# Назначенные услуги приема
class ScheduleService(models.Model):
    STATUS_CHOICES = (
        (0, "не выполнена"),
        (1, "выполнена")
    )
    STATUS_PAYMENT = (
        (0, "не оплачено"),
        (1, "оплачено")
    )
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    service = models.ForeignKey(
        'service_system.Service', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    status_payment = models.IntegerField(choices=STATUS_PAYMENT, default=0)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    discount = models.DecimalField(decimal_places=0, max_digits=60, default=0)
    quantity = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.id and not self.price:
            self.price = self.service.price
        return super(ScheduleService, self).save(*args, **kwargs)

    def get_invoice(self):
        price = (self.quantity * self.price)
        discount = (self.discount / 100) * self.price
        return int(price - discount)

    @property
    def total_price(self):
        discount = (self.discount / 100) * self.price
        return int(self.price - discount)


# Ресурсы приема
class ScheduleEquipment(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    equipment = models.ForeignKey(
        'equipment_system.Equipment', on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
