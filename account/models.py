from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from register.models import Schedule
from rest_framework.authtoken.models import Token


# Базовый абстрактный класс
class ItemBase(models.Model):
    title = models.CharField(max_length=180)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# Список видов деятельности
class Industry(ItemBase):
    pass


# Список компании
class Company(ItemBase):
    phono_number = models.CharField(max_length=18)
    address = models.CharField(max_length=180, null=True, blank=True)
    industry = models.ForeignKey(Industry,
                                 related_name='companies_industry',
                                 on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Больницы"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Company, self).save(*args, **kwargs)

    def get_users(self, func_structure=None, is_display_calendar=False):
        query = self.user_set
        if is_display_calendar:
            query = query.filter(is_display_calendar=True)
        if func_structure:
            query = query.filter(func_structure=func_structure)
        return query.all()

    def get_group_equipments(self):
        return self.equipmentgroup_set.all()

    def get_equipments(self, equipment_group=None):
        query = self.equipment_set
        if equipment_group:
            query = query.filter(equipment_group=equipment_group)
        return query.all()

    def get_func_structures(self):
        return self.funcstructure_set.all()

    def get_priority_user(self, is_display_calendar=False):
        query = self.user_set
        if is_display_calendar:
            query = query.filter(is_display_calendar=True)
        query = query.order_by('id').first()
        if query:
            return query
        return None

    def get_priority_func_structure(self, is_display_calendar=False):
        return self.funcstructure_set.order_by('id').first()

    def get_priority_equipment(self):
        equipment = self.equipment_set.order_by('id').first()
        if equipment:
            return equipment.id
        return None

    def get_work_time(self):
        return self.companyworktime_set.all()

    def get_forms(self):
        return self.companyform_set.all()


# Функциональная структура компаний
class FuncStructure(ItemBase):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE)


# Специальность компаний
class Speciality(ItemBase):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE)


# Расширенный модель пользователя
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (2, 'Регистратор'),
        (3, 'Доктор')
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True)
    func_structure = models.ForeignKey(
        FuncStructure, on_delete=models.CASCADE, null=True, blank=True)
    speciality = models.ForeignKey(
        Speciality, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, default=1)
    is_display_calendar = models.BooleanField(default=True)
    schedules = GenericRelation(Schedule, content_type_field='content_type', object_id_field='object_id')
    doctor_code = models.CharField(max_length=10, verbose_name='Doctor Code', default='Doctor Code')
    # def save(self, *args, **kwargs):
    #    self.slug = slugify(self.username)
    #    super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()

    @property
    def full_name(self):
        return "{} {}".format(self.last_name, self.first_name)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super(User, self).save(*args, **kwargs)
        if is_new:
            Token.objects.create(user=self)
