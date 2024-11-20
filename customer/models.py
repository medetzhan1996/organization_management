from django.db import models
from account.models import Company


# Список клиентов
class Customer(models.Model):
    GENDER_CHOICES = (
        ("man", "Мужчина"),
        ("woman", "Женщина"),
    )
    first_name = models.CharField(max_length=180)
    last_name = models.CharField(max_length=180)
    surname = models.CharField(max_length=180, null=True, blank=True)
    iin = models.CharField(max_length=12, null=True, blank=True)
    date_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=240, null=True, blank=True)
    place_work = models.CharField(max_length=240, null=True, blank=True)
    phono_number = models.CharField(max_length=180, null=True, blank=True)
    email = models.EmailField(max_length=70, null=True, blank=True)
    gender = models.CharField(max_length=180, choices=GENDER_CHOICES, null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE)

    @property
    def name(self):
        return "{} {}".format(self.last_name, self.first_name)

    def __str__(self):
        return self.name
