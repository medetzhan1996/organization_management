from django import forms
from .models import Customer

# Форма клиента
class CustomerForm(forms.ModelForm):
    date_birth = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))

    class Meta:
        model = Customer
        fields = (
            'last_name', 'first_name', 'surname', 'phono_number', 'email', 'company',
            'iin', 'date_birth', 'address', 'place_work',
            'gender',
        )
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
