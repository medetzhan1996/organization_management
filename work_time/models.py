from datetime import datetime
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class ContentTypeQuerySet(QuerySet):

    def filter_content_type(self, model, object=None):
        query = self.filter(content_type=ContentType.objects.get_for_model(
                model))
        if object:
            try:
                query = query.filter(object_id__in=object)
            except TypeError:
                query = query.filter(object_id=object)
        return query


# Еженедельные рабочие часы
class WorkTime(models.Model):
    objects = ContentTypeQuerySet.as_manager()
    WEEK_CHOICES = (
        (0, "Пн"),
        (1, "Втр"),
        (2, "Срд"),
        (3, "Чтв"),
        (4, "Птн"),
        (5, "Суб"),
        (6, "Воск")
    )
    STATUS_CHOICES = (
        (0, "не активный"),
        (1, "активный")
    )
    week = models.IntegerField(choices=WEEK_CHOICES, default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    start_time = models.TimeField()
    end_time = models.TimeField()
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'company',
                                         'equipment',
                                         'user')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


# Исключение графика работы
class WorkTimeExclusion(models.Model):
    objects = ContentTypeQuerySet.as_manager()
    STATUS_CHOICES = (
        (0, "активный"),
        (1, "не активный")
    )
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'company',
                                         'equipment',
                                         'user')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    @property
    def start_datetime(self):
        return datetime.combine(self.date, self.start_time)

    @property
    def end_datetime(self):
        return datetime.combine(self.date, self.end_time)
