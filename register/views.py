import requests
from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin

from actions.utils import create_action
from customer.models import Customer
from equipment_system.models import Equipment
from modal_convert.helpers import merge_list_filter_by_date
from account.convert import UserConvert
from equipment_system.convert import EquipmentConvert
from work_time.models import WorkTime, WorkTimeExclusion
from work_time.convert import WorkTimeExclusionConvert, WorkTimeConvert
from .models import Schedule, ScheduleService
from .convert import ScheduleConvert, ScheduleUserConvert
from .forms import ScheduleForm, ScheduleTimerForm, ScheduleServiceForm
from .helpers import get_free_slots
from django.db import connections


# Календарь работы
class IndexView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'register/index.html'

    def get(self, request):
        company = request.user.company
        users = company.get_users(is_display_calendar=True)
        func_structure = company.get_priority_func_structure()
        func_structures = company.get_func_structures()
        group_equipments = company.get_group_equipments()
        equipments = company.get_equipments()
        return self.render_to_response(
            {'users': users, 'equipments': equipments,
             'func_structures': func_structures,
             'group_equipments': group_equipments,
             'func_structure': func_structure
             })


class ConvertMixin(object):

    @staticmethod
    def get_schedule_user_convert(model, object, start=None, end=None):
        schedule = Schedule.objects.filter_content_type(
            model, object)
        return ScheduleUserConvert(
            queryset=schedule).convert_to_list_of_dict()

    @staticmethod
    def get_work_time_convert(model, object, start=None, end=None):
        queryset = WorkTime.objects.filter_content_type(
            model, object)
        return WorkTimeConvert(
            queryset=queryset).week_to_date(start, end)

    @staticmethod
    def get_work_time_exclusion_convert(model, object, start=None, end=None):
        work_time_exclusion = WorkTimeExclusion.objects.filter_content_type(
            model, object)
        return WorkTimeExclusionConvert(
            queryset=work_time_exclusion).convert_to_list_of_dict()


# Mixin события
class EventMixin(ConvertMixin):
    company = None
    start = None
    end = None

    def dispatch(self, *args, **kwargs):
        self.company = self.request.user.company
        self.start = datetime.fromisoformat(
            self.request.GET.get('start')).date()
        self.end = datetime.fromisoformat(self.request.GET.get('end')).date()
        return super().dispatch(*args, **kwargs)

    def merge_events(self, model, object, start=None, end=None):
        schedule_convert = self.get_schedule_user_convert(
            model, object, start, end)
        work_time_convert = self.get_work_time_convert(
            model, object, start, end)
        work_time_exclusion_convert = self.get_work_time_exclusion_convert(
            model, object, start, end)
        merge_list = merge_list_filter_by_date(
            work_time_exclusion_convert,
            work_time_convert, start, end)
        events = schedule_convert
        events += merge_list
        return events


# Ресурс пользователя
class UserResourceView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(get_user_model(), id=pk)
        resources = UserConvert(queryset=queryset).convert_to_list_of_dict()
        return JsonResponse(resources, safe=False)


# Ресурсы пользователей
class UsersResourceView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        func_structure = kwargs.get('func_structure')
        company = request.user.company
        queryset = company.get_users(
            func_structure=func_structure, is_display_calendar=True)
        resources = UserConvert(queryset=queryset).convert_to_list_of_dict()
        return JsonResponse(resources, safe=False)


# Получить график пользователя
class UserEventsView(LoginRequiredMixin, EventMixin, View):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=kwargs.get('pk'))
        result = self.merge_events(
            get_user_model(), user.id, self.start, self.end)
        return JsonResponse(result, safe=False)


# Получить график пользователей
class UsersEventsView(LoginRequiredMixin, EventMixin, View):

    def get(self, request, *args, **kwargs):
        func_structure = kwargs.get('func_structure', None)
        users = self.company.get_users(
            func_structure=func_structure, is_display_calendar=True)
        result = self.merge_events(
            get_user_model(), users, self.start, self.end)
        return JsonResponse(result, safe=False)


# Ресурс
class EquipmentResourceView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Equipment, id=pk)
        resources = EquipmentConvert(
            queryset=queryset).convert_to_list_of_dict()
        return JsonResponse(resources, safe=False)


# Ресурсы пользователей
class EquipmentsResourceView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        equipment_group = kwargs.get('equipment_group', None)
        company = request.user.company
        queryset = company.get_equipments(
            equipment_group=equipment_group)
        resources = EquipmentConvert(
            queryset=queryset).convert_to_list_of_dict()
        return JsonResponse(resources, safe=False)


# Получить график ресурса
class EquipmentEventsView(LoginRequiredMixin, EventMixin, View):

    def get(self, request, *args, **kwargs):
        equipment = get_object_or_404(Equipment, id=kwargs.get('pk'))
        result = self.merge_events(
            Equipment, equipment.id, self.start, self.end)
        return JsonResponse(result, safe=False)


# Получить график ресурсов
class EquipmentsEventsView(LoginRequiredMixin, EventMixin, View):

    def get(self, request, *args, **kwargs):
        equipment_group = kwargs.get('equipment_group', None)
        equipments = self.company.get_equipments(
            equipment_group=equipment_group)
        result = self.merge_events(Equipment, equipments, self.start, self.end)
        return JsonResponse(result, safe=False)


# Удалить график работы
class ScheduleDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            schedule = Schedule.objects.get(pk=pk)
            schedule.delete()
            return JsonResponse({'status': True})
        except Schedule.DoesNotExist:
            return JsonResponse({'status': False})


# свободные слоты ?
class FreeSlotsView(LoginRequiredMixin, ConvertMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.GET.get('user')
        duration = int(request.GET.get('duration', 30))
        date = request.GET.get('date')
        schedule_convert = self.get_schedule_user_convert(get_user_model(), user)
        free_slots = get_free_slots(
            schedule_convert, '08:00:00', '20:00:00', duration)
        return JsonResponse({'is_free': True,
                             'free_slots': free_slots})


# Обновить события ?
class ScheduleTimerUpdateView(LoginRequiredMixin, View):

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        schedule = get_object_or_404(Schedule, pk=pk)
        form = ScheduleTimerForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Mixin schedule form set
class ScheduleServiceFormSetMixin(object):

    @staticmethod
    def get_service_formset(schedule=None, data=None):
        ScheduleFormSet = inlineformset_factory(
            Schedule,
            ScheduleService,
            form=ScheduleServiceForm,
            extra=0, can_delete=True)
        return ScheduleFormSet(
            instance=schedule, data=data)

    @staticmethod
    def save_service_formset(schedule, schedule_services):
        for schedule_service in schedule_services:
            schedule_service.schedule = schedule
            schedule_service.save()

    @staticmethod
    def delete_service_formset(schedule_service_formset):
        schedule_deleted_objects = schedule_service_formset.deleted_objects
        for schedule_service in schedule_deleted_objects:
            schedule_service.delete()


# Mixin schedule edit
class ScheduleEditMixin(object):
    schedule = None
    last_customer = None
    func_structures = None
    group_equipments = None

    def dispatch(self, *args, **kwargs):
        pk = kwargs.get('pk', None)
        company = self.request.user.company
        self.func_structures = company.get_func_structures()
        self.group_equipments = company.get_group_equipments()
        self.last_customer = Customer.objects.filter(company=company).last()
        if pk:
            self.schedule = get_object_or_404(Schedule, id=pk)
        return super().dispatch(*args, **kwargs)

    def post(self, request, **kwargs):
        messages.success(request, 'Запись успешна сохранена!')
        schedule_form = ScheduleForm(
            request, data=request.POST, instance=self.schedule)
        schedule_service_formset = self.get_service_formset(
            data=request.POST, schedule=self.schedule)
        if schedule_form.is_valid() and schedule_service_formset.is_valid():
            schedule = schedule_form.save()
            schedule_services = schedule_service_formset.save(
                commit=False
            )
            self.save_service_formset(schedule, schedule_services)
            self.delete_service_formset(schedule_service_formset)
            if self.schedule:
                create_action(request.user, 'Обновлен прием', schedule)
            else:
                create_action(request.user, 'Добавлен на прием', schedule)
            return JsonResponse({'status': True, 'schedule': schedule.id})
        return JsonResponse({'status': False})


# Добавить запись
class ScheduleCreateView(
        LoginRequiredMixin, ScheduleEditMixin, ScheduleServiceFormSetMixin, View):

    def get(self, request):
        customer = request.GET.get('customer', None)
        schedule_form = ScheduleForm(
            request.GET, initial={'customer': customer})
        if customer:
            customer = get_object_or_404(Customer, id=customer)
        schedule_service_formset = self.get_service_formset()
        return render(request, 'register/schedule/form.html', {
            'func_structures': self.func_structures,
            'group_equipments': self.group_equipments,
            'schedule_form': schedule_form,
            'schedule_service_formset': schedule_service_formset,
            'last_customer': self.last_customer,
            'customer': customer
        })


# Обновить запись
class ScheduleUpdateView(
        LoginRequiredMixin, ScheduleEditMixin, ScheduleServiceFormSetMixin, View):

    def get(self, request, **kwargs):
        schedule_form = ScheduleForm(
            request.GET, instance=self.schedule)
        schedule_service_formset = self.get_service_formset(
            schedule=self.schedule)
        return render(request, 'register/schedule/form.html', {
            'func_structures': self.func_structures,
            'group_equipments': self.group_equipments,
            'schedule_form': schedule_form,
            'schedule_service_formset': schedule_service_formset,
        })