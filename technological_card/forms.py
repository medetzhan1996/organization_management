from django import forms
from .models import TechnologicalCard, Consumable


# Категория услуг
class TechnologicalCardForm(forms.ModelForm):

    class Meta:
        model = TechnologicalCard
        fields = ['title', 'comment']


# Категория услуг
class ConsumableForm(forms.ModelForm):

    class Meta:
        model = Consumable
        fields = ['technological_card', 'storage', 'good', 'receipt_amount']
