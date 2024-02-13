from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from service_system.models import Service
from customer.models import Customer
from register.models import ScheduleService
from warehouse.forms import StorageOperationForm, StorageOperationGoodForm
from .models import TechnologicalCard, Consumable
from .forms import ConsumableForm, TechnologicalCardForm


# Mixin клиентов на прием
class ConsumableInTechCardListView(LoginRequiredMixin, ListView):
    template_name = 'technological_card/consumable_in_tech_card/list.html'
    model = Consumable
    context_object_name = 'consumables'
    active_technological_card = None

    def get_queryset(self):
        qs = super().get_queryset()
        technological_card = self.kwargs.get('technological_card', None)
        if technological_card:
            qs = qs.filter(technological_card=technological_card)
            self.active_technological_card = get_object_or_404(
                TechnologicalCard, pk=technological_card)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_technological_card'] = self.active_technological_card
        context['technological_cards'] = TechnologicalCard.objects.all()
        return context


class TechnologicalCardCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = TechnologicalCardForm()
        return render(request,
                      'technological_card/technological_card/form.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = TechnologicalCardForm(request.POST)
        if form.is_valid():
            technological_card = form.save()
            return render(
                request, 'technological_card/technological_card/list.html',
                {'technological_card': technological_card})
            return JsonResponse({'status': 200})
        return JsonResponse({'status': 500})


# Обновить услугу
class TechnologicalCardUpdateView(LoginRequiredMixin, View):

    def dispatch(self, *args, **kwargs):
        self.pk = self.kwargs.get('pk')
        self.technological_card = get_object_or_404(
            TechnologicalCard, pk=self.pk)
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TechnologicalCardForm(instance=self.technological_card)
        return render(request,
                      'technological_card/technological_card/update.html',
                      {'form': form,
                       'technological_card': self.technological_card})

    def post(self, request, *args, **kwargs):
        form = TechnologicalCardForm(
            request.POST, instance=self.technological_card)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        return JsonResponse({'status': False})


# Удалить категорию услуг
class TechnologicalCardDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            technological_card = TechnologicalCard.objects.get(pk=pk)
            technological_card.delete()
            return JsonResponse({'status': True})
        except TechnologicalCard.DoesNotExist:
            return JsonResponse({'status': False})


# Добавить расходной материал
class ConsumableCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        technological_card = self.kwargs.get('technological_card', None)
        form = ConsumableForm(
            initial={'technological_card': technological_card})
        return render(request, 'technological_card/consumable/form.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = ConsumableForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        return JsonResponse({'status': False})


# Mixin клиентов на прием
class ConsumableListView(LoginRequiredMixin, ListView):
    template_name = 'technological_card/consumable/list.html'
    model = Consumable
    context_object_name = 'consumables'


# Обновить расходной материал
class ConsumableUpdateView(LoginRequiredMixin, View):

    def dispatch(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.consumable = get_object_or_404(Consumable, pk=pk)
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = ConsumableForm(instance=self.consumable)
        return render(request, 'technological_card/consumable/update.html',
                      {'form': form, 'consumable': self.consumable})

    def post(self, request, *args, **kwargs):
        form = ConsumableForm(instance=self.consumable, data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        return JsonResponse({'status': False})


# Удалить расходной материал
class ConsumableDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            service_obj = Consumable.objects.get(pk=pk)
            service_obj.delete()
            return JsonResponse({'status': True})
        except Consumable.DoesNotExist:
            return JsonResponse({'status': False})


# Расходные материалы
class ConsumableСalculateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        data = []
        service = get_object_or_404(
            Service, pk=self.kwargs.get('service'))
        technological_cards = service.technological_cards
        for technological_card in technological_cards.all():
            for consumable in technological_card.consumable_set.all():
                item = {
                    'good': {
                        'id': consumable.good.id,
                        'title': consumable.good.title
                    },
                    'receipt_amount': consumable.receipt_amount,
                    'storage': {
                        'id': consumable.storage.id,
                        'title': consumable.storage.title
                    }
                }
                data.append(item)
        return JsonResponse(data, safe=False)


# Cписать расходной материал
class ConsumableInAppointedServiceView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'technological_card/consumable_in_appointed_service/form.html'

    def dispatch(self, *args, **kwargs):
        customer_id = self.kwargs.get('customer')
        self.customer = get_object_or_404(Customer, id=customer_id)
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        history = request.GET.get('history', '')
        today = datetime.today().strftime('%Y-%m-%d')
        schedules = self.customer.schedule_set.filter(
            start_datetime__date=today)
        return self.render_to_response({
            'schedules': schedules,
            'customer': self.customer,
            'history': history
        })

    def post(self, request, *args, **kwargs):
        schedule_services = request.POST.getlist('schedule_service')
        goods = request.POST.getlist('good')
        storages = request.POST.getlist('storage')
        receipt_amounts = request.POST.getlist('receipt_amount')
        for schedule_service in schedule_services:
            schedule_service_obj = get_object_or_404(
                ScheduleService, id=schedule_service)
            schedule_service_obj.status = 1
            schedule_service_obj.save()
        for good, storage, receipt_amount in \
                zip(goods, storages, receipt_amounts):
            storage_operation_form_data = {
                'storage': storage,
                'type_operation': 3,
                'customer': self.customer.id
            }
            storage_operation_good_form_data = {
                'good': good,
                'quantity': receipt_amount,
                'quantity_write_off': receipt_amount
            }
            storage_operation_form = StorageOperationForm(
                request, data=storage_operation_form_data)
            storage_operation_good_form = StorageOperationGoodForm(
                data=storage_operation_good_form_data)
            if storage_operation_form.is_valid() and \
                    storage_operation_good_form.is_valid():
                storage_operation = storage_operation_form.save()
                obj = storage_operation_good_form.save(commit=False)
                obj.storage_operation = storage_operation
                obj.save()
        return JsonResponse({'status': True})
