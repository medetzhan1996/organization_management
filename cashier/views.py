from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import inlineformset_factory
from register.models import Schedule, ScheduleService
from register.views import ScheduleServiceFormSetMixin
from .models import CustomerPaidInvoice


# Прием платежа
class AcceptPaymentView(ScheduleServiceFormSetMixin, View):
    schedule = None

    @staticmethod
    def get_invoice_formset(schedule, data=None):
        extra = 0 if schedule.customerpaidinvoice_set.count() else 1
        InvoiceFormSet = inlineformset_factory(
            Schedule,
            CustomerPaidInvoice,
            fields=['paid', 'payment_method', 'comment'],
            extra=extra, can_delete=True)
        return InvoiceFormSet(
            instance=schedule, data=data)

    def dispatch(self, *args, **kwargs):
        self.schedule = get_object_or_404(
            Schedule, id=self.kwargs.get('schedule', None))
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        schedule_service_formset = self.get_service_formset(self.schedule)
        schedule_invoice_formset = self.get_invoice_formset(self.schedule)
        return render(request, 'cashier/form.html', {
            'schedule_service_formset': schedule_service_formset,
            'schedule_invoice_formset': schedule_invoice_formset,
            'schedule': self.schedule
        })

    def post(self, request, *args, **kwargs):
        schedule_service_formset = self.get_service_formset(
            self.schedule, data=request.POST)
        schedule_invoice_formset = self.get_invoice_formset(
            self.schedule, data=request.POST)
        if schedule_service_formset.is_valid():
            schedule_services = schedule_service_formset.save(
                commit=False
            )
            self.save_service_formset(self.schedule, schedule_services)
            self.delete_service_formset(schedule_service_formset)
        if schedule_invoice_formset.is_valid():
            schedule_invoices = schedule_invoice_formset.save(
                commit=False
            )
            for schedule_invoice in schedule_invoices:
                schedule_invoice.customer = self.schedule.customer
                schedule_invoice.schedule = self.schedule
                schedule_invoice.save()
            invoice_deleted_objects = schedule_invoice_formset.deleted_objects
            for schedule_invoice in invoice_deleted_objects:
                schedule_invoice.delete()
            # if paid:
            #     schedule_services = self.schedule.scheduleservice_set.filter(
            #         status_payment=0).all()
            #     for schedule_service in schedule_services:
            #         if paid >= schedule_service.price:
            #             schedule_service.status_payment = 1
            #             schedule_service.save()
            #             paid -= schedule_service.price
        return JsonResponse({'status': True})
