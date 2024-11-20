from datetime import datetime, date
from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from equipment_system.models import Equipment
from register.utils import RegisterUtils
from .models import Schedule, ScheduleEquipment, ScheduleService


# Форма расписании
class ScheduleForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d')))
    start_time = forms.TimeField()

    class Meta:
        model = Schedule
        fields = ['date', 'start_time', 'status',
                  'customer', 'duration', 'comment',
                  'object_id', 'content_type']

        widgets = {
            'content_type': forms.HiddenInput
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('instance', None):
            self.fields['date'].initial = \
                kwargs['instance'].start_datetime.date()
            self.fields['start_time'].initial = \
                kwargs['instance'].start_datetime.time()
        else:
            self.fields['date'].initial = date.today()

    def save(self, commit=True):
        start_datetime = datetime.combine(self.cleaned_data['date'],
                                          self.cleaned_data['start_time'])
        form = super(ScheduleForm, self).save(commit=False)
        form.start_datetime = start_datetime
        form.duration = self.cleaned_data['duration']
        if commit:
            form.save()
        return form


# Форма расписании
class ScheduleTimerForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d')))
    start_time = forms.TimeField()
    end_date = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d')))
    end_time = forms.TimeField()

    class Meta:
        model = Schedule
        fields = ['start_date',
                  'start_time', 'end_date', 'end_time', 'object_id']

    def save(self, commit=True):
        start_datetime = datetime.combine(self.cleaned_data['start_date'],
                                          self.cleaned_data['start_time'])
        end_datetime = datetime.combine(self.cleaned_data['end_date'],
                                        self.cleaned_data['end_time'])
        duration = RegisterUtils.get_duration(start_datetime, end_datetime)
        form = super(ScheduleTimerForm, self).save(commit=False)
        form.start_datetime = start_datetime
        form.duration = duration
        if commit:
            form.save()
        return form


class ScheduleServiceForm(forms.ModelForm):

    class Meta:
        model = ScheduleService
        fields = ['service']
        exclude = ('price', 'discount', 'quantity', )
