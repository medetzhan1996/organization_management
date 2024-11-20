from django import forms
from .models import CategoryService, Service
from technological_card.models import TechnologicalCard
from account.models import User


# Категория услуг
class CategoryServiceForm(forms.ModelForm):

    class Meta:
        model = CategoryService
        fields = ['title']
        exclude = ['company']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.company = self.request.user.company
        if commit:
            instance.save()
        return instance


# Услуги
class ServiceForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)
    technological_cards = forms.ModelMultipleChoiceField(
        queryset=TechnologicalCard.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Service
        fields = ['title', 'price', 'category', 'duration',
                  'technological_cards', 'users']
        exclude = ['company', 'parent']
