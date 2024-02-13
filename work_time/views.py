from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import WorkTime, WorkTimeExclusion
from .forms import WorkTimeForm, WorkTimeExclutionForm


# Mixin рабочего времени
class WorkTimeWithExclutionMixin(LoginRequiredMixin, TemplateResponseMixin, View):
    company = None
    users = None
    today = None

    def dispatch(self, *args, **kwargs):
        self.company = self.request.user.company
        self.users = self.company.get_users(is_display_calendar=True)
        self.today = datetime.today().strftime('%Y-%m-%d')
        return super().dispatch(*args, **kwargs)

    def get_work_time_week(self, resource):
        work_time_week = WorkTime.objects.filter(
            content_type=ContentType.objects.get_for_model(
                resource), object_id=resource.id, status=1
        ).all()
        return work_time_week

    def get_work_time_exclusions(self, resource):
        work_time_exclusions = WorkTimeExclusion.objects.filter(
            date__gte=self.today,
            content_type=ContentType.objects.get_for_model(
                resource), object_id=resource.id
        ).all()
        return work_time_exclusions


# Рабочее время компании
class CompanyWorkTimeWithExclutionListView(WorkTimeWithExclutionMixin):
    template_name = 'work_time/work_time_with_exclution/list.html'

    def get(self, request, *args, **kwargs):
        resource = 'company'
        work_time_week = self.get_work_time_week(self.company)
        work_time_exclusions = self.get_work_time_exclusions(self.company)
        return self.render_to_response({
            'users': self.users, 'work_time_week': work_time_week,
            'work_time_exclusions': work_time_exclusions,
            'resource': resource})


# Рабочее время работника
class UserWorkTimeWithExclutionListView(WorkTimeWithExclutionMixin):
    template_name = 'work_time/work_time_with_exclution/list.html'

    def get(self, request, *args, **kwargs):
        resource = 'user'
        pk = kwargs.get('pk', None)
        if pk:
            user = get_object_or_404(get_user_model(), id=pk)
        else:
            user = self.company.get_priority_user(is_display_calendar=True)
        work_time_week = self.get_work_time_week(user)
        work_time_exclusions = self.get_work_time_exclusions(user)
        return self.render_to_response({
            'users': self.users, 'work_time_week': work_time_week,
            'work_time_exclusions': work_time_exclusions, 'user': user,
            'resource': resource, 'pk': pk})


class WorkTimeEditMixin(LoginRequiredMixin, View):

    def work_time_create(self, resource, data):
        work_time_form = WorkTimeForm(resource, data=data)
        if work_time_form.is_valid():
            work_time_form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Исключение рабочего времени работника
class CompanyWorkTimeCreateView(WorkTimeEditMixin):

    def post(self, request, *args, **kwargs):
        company = request.user.company
        return self.work_time_create(company, request.POST)


# Исключение рабочего времени работника
class UserWorkTimeCreateView(WorkTimeEditMixin):

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(get_user_model(), id=pk)
        return self.work_time_create(user, request.POST)


class WorkTimeExclutionMixin(LoginRequiredMixin, TemplateResponseMixin, View):
    def work_time_exclusion_delete(self, resource, date):
        WorkTimeExclusion.objects.filter(
            date=date,
            content_type=ContentType.objects.get_for_model(
                resource), object_id=resource.id
        ).delete()

    def work_time_exclusion_create(self, resource, date):
        for start, end in zip(self.start_time, self.end_time):
            data = {'date': date, 'start_time': start, 'end_time': end}
            form = WorkTimeExclutionForm(resource, data=data)
            if form.is_valid():
                form.save()

    def work_time_exclusion_create_with_delete(self, resource):
        for date in self.exclution_dates.split(", "):
            self.work_time_exclusion_delete(resource, date)
            self.work_time_exclusion_create(resource, date)

    def dispatch(self, *args, **kwargs):
        self.exclution_dates = self.request.POST.get('exclution_date')
        self.start_time = self.request.POST.getlist('start_time')
        self.end_time = self.request.POST.getlist('end_time')
        return super().dispatch(*args, **kwargs)


# Исключение рабочего времени работника
class CompanyWorkTimeExclutionCreateView(WorkTimeExclutionMixin):
    template_name = 'work_time/work_time_exclution/form.html'

    def get(self, request, *args, **kwargs):
        resource = 'company'
        return self.render_to_response({'resource': resource})

    def post(self, request, *args, **kwargs):
        resource = self.request.user.company
        self.work_time_exclusion_create_with_delete(resource)
        return JsonResponse({'success': True})


# Исключение рабочего времени работника
class UserWorkTimeExclutionCreateView(WorkTimeExclutionMixin):
    template_name = 'work_time/work_time_exclution/form.html'

    def get(self, request, *args, **kwargs):
        resource = 'user'
        return self.render_to_response({
            'resource': resource})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        resource = get_object_or_404(get_user_model(), id=pk)
        self.work_time_exclusion_create_with_delete(resource)
        return JsonResponse({'success': True})


# Исключение рабочего времени работника
class WorkTimeExclutionCreateView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'work_time/work_time_exclution/form.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        resource = get_object_or_404(get_user_model(),
                                     id=request.POST.get('user'))
        exclution_dates = request.POST.get('exclution_date')
        start_time = request.POST.getlist('start_time')
        end_time = request.POST.getlist('end_time')
        for date in exclution_dates.split(", "):
            WorkTimeExclusion.objects.filter(
                date=date,
                content_type=ContentType.objects.get_for_model(
                    resource), object_id=resource.id
            ).delete()
            for start, end in zip(start_time, end_time):
                data = {'date': date, 'start_time': start, 'end_time': end}
                form = WorkTimeExclutionForm(resource, data=data)
                if form.is_valid():
                    form.save()
        return JsonResponse({'success': True})


# Список рабочик часов
class CompanyWorkTimeListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        week = self.request.GET.get('week')
        company = request.user.company
        work_time = company.work_time.filter(status=1, week=week).all()
        return render(request, 'work_time/work_time/day_list.html',
                      {'work_time': work_time})


# Список рабочик часов
class UserWorkTimeListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        week = self.request.GET.get('week')
        user = get_object_or_404(get_user_model(), id=pk)
        work_time = WorkTime.objects.filter_content_type(
            user, user.id).filter(status=1, week=week).all()
        return render(request, 'work_time/work_time/day_list.html',
                      {'work_time': work_time})


# Обновить рабочее время
class WorkTimeUpdateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            work_time = WorkTime.objects.get(pk=pk)
            work_time.start_time = start_time
            work_time.end_time = end_time
            work_time.save()
            return JsonResponse({'status': True})
        except WorkTime.DoesNotExist:
            return JsonResponse({'status': False})


# Удалить рабочее время
class WorkTimeDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            work_time = WorkTime.objects.get(pk=pk)
            work_time.delete()
            return JsonResponse({'status': True})
        except WorkTime.DoesNotExist:
            return JsonResponse({'status': False})


# Удалить рабочее время
class WorkTimeExclutionDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            work_time = WorkTime.objects.get(pk=pk)
            work_time.delete()
            return JsonResponse({'status': True})
        except WorkTime.DoesNotExist:
            return JsonResponse({'status': False})
