from datetime import datetime, timedelta, date
from django import forms
from .models import WorkTime, WorkTimeExclusion


class WorkTimeForm(forms.ModelForm):

    class Meta:
        model = WorkTime
        fields = ['week']
        exclude = ('status', 'start_time', 'end_time', )

    def __init__(self, resource, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = resource

    def save(self, commit=True):
        form = super(WorkTimeForm, self).save(commit=False)
        week = self.cleaned_data['week']
        work_last_time = WorkTime.objects.filter_content_type(
            self.resource, self.resource.id).filter(week=week).last()
        if work_last_time:
            start_datetime = datetime.combine(
                date(1, 1, 1), work_last_time.end_time)
            start_time = (start_datetime + timedelta(hours=1)).time()
        else:
            start_time = datetime.strptime('08:00:00', '%H:%M:%S').time()
        end_datetime = datetime.combine(date(1, 1, 1), start_time)
        end_time = (end_datetime + timedelta(hours=1)).time()
        form.status = '1'
        form.start_time = start_time
        form.end_time = end_time
        form.item = self.resource
        if commit:
            form.save()
        return form


class WorkTimeExclutionForm(forms.ModelForm):

    def __init__(self, resource, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = resource

    class Meta:
        model = WorkTimeExclusion
        fields = ['date', 'start_time', 'end_time']

    def save(self, commit=True):
        form = super(WorkTimeExclutionForm, self).save(commit=False)
        form.item = self.resource
        if commit:
            form.save()
