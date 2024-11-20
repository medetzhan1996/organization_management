from django import forms
from .models import ReadyPhrase


# Форма готового шаблона
class ReadyPhraseForm(forms.ModelForm):

    class Meta:
        model = ReadyPhrase
        fields = ['phrase', 'parent', 'marker']
        widgets = {'marker': forms.HiddenInput()}

    def __init__(self, marker=None, user=None, **kwargs):
        super(ReadyPhraseForm, self).__init__(**kwargs)
        if kwargs.get('instance', None):
            user = kwargs['instance'].user
            marker = kwargs['instance'].marker
            self.fields['parent'].queryset = ReadyPhrase.objects.filter(
                user=user, marker=marker)
        else:
            self.fields['marker'].initial = marker
            if marker and user:
                self.fields['parent'].queryset = ReadyPhrase.objects.filter(
                    user=user, marker=marker)
