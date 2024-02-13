from django import forms
from .models import CategoryGood, Good, Storage, StorageOperation,\
    StorageOperationGood


# Категория товаров
class CategoryGoodForm(forms.ModelForm):

    class Meta:
        model = CategoryGood
        fields = ['title', 'comment']
        exclude = ('company', )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.company = self.request.user.company
        if commit:
            instance.save()
        return instance


# Форма Товаров в категориях
class GoodForm(forms.ModelForm):

    class Meta:
        model = Good
        fields = ['title', 'comment',
                  'category', 'barcode', 'sale_unit',
                  'write_off_unit', 'unit_equals', 'cost', 'actual_cost',
                  'critical_amount', 'desired_amount']


# Форма Складов
class StorageForm(forms.ModelForm):

    class Meta:
        model = Storage
        fields = ['title', 'company', 'comment']
        exclude = ('company', )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.company = self.request.user.company
        if commit:
            instance.save()
        return instance


# Форма Складов
class StorageOperationForm(forms.ModelForm):

    class Meta:
        model = StorageOperation
        fields = ['storage',
                  'type_operation', 'provider', 'customer']
        exclude = ('company', )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.company = self.request.user.company
        instance.user = self.request.user
        if commit:
            instance.save()
        return instance


# Форма Складов
class StorageOperationGoodForm(forms.ModelForm):

    class Meta:
        model = StorageOperationGood
        fields = ['good', 'quantity', 'quantity_write_off']
        exclude = ('storage_operation', )
