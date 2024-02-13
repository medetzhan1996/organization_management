from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from register.models import Schedule

# Оборудовании организации
class EquipmentGroup(models.Model):
    title = models.CharField(max_length=180)
    company = models.ForeignKey('account.Company', on_delete=models.CASCADE)


# Оборудовании организации
class Equipment(models.Model):
    title = models.CharField(max_length=180)
    equipment_group = models.ForeignKey(EquipmentGroup, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey('account.Company', on_delete=models.CASCADE)
    schedules = GenericRelation(Schedule, content_type_field='content_type', object_id_field='object_id')
