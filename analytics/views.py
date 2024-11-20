from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from .models import UserAnalytic, SpecialityAnalytic,\
    CustomerAnalytic, ScheduleAnalytic


# Mixin времени
class TimeCompanyMixin(object):
    company = None
    start_date = None
    end_date = None

    def dispatch(self, *args, **kwargs):
        today = date.today().strftime("%Y-%m-%d")
        self.company = self.request.user.company
        self.start_date = self.request.GET.get('start_date', today)
        self.end_date = self.request.GET.get('end_date', today)
        return super().dispatch(*args, **kwargs)


# Аналитика записей регистраторов
class RecordView(LoginRequiredMixin, TimeCompanyMixin, TemplateResponseMixin, View):
    template_name = 'analytics/record.html'

    def get(self, request):
        users = UserAnalytic.objects.filter(
            company=self.company, user_type=2).all()
        return self.render_to_response({
            'users': users, 'start_date': self.start_date,
            'end_date': self.end_date})


# Аналитика записей регистраторов
class SpecialityView(LoginRequiredMixin, TimeCompanyMixin, TemplateResponseMixin, View):
    template_name = 'analytics/speciality.html'

    def get(self, request):
        specialities = SpecialityAnalytic.objects.filter(
            company=self.company).all()
        return self.render_to_response({
            'specialities': specialities, 'start_date': self.start_date,
            'end_date': self.end_date})


# Аналитика записей регистраторов
class DoctorView(LoginRequiredMixin, TimeCompanyMixin, TemplateResponseMixin, View):
    template_name = 'analytics/doctor.html'

    def get(self, request):
        users = UserAnalytic.objects.filter(
            company=self.company, user_type=3).all()
        return self.render_to_response({
            'users': users, 'start_date': self.start_date,
            'end_date': self.end_date})


# Аналитика записей регистраторов
class CustomerView(LoginRequiredMixin, TimeCompanyMixin, TemplateResponseMixin, View):
    template_name = 'analytics/customer.html'

    def get(self, request, **kwargs):
        schedule_services = None
        pk = kwargs.get('pk', None)
        customers = CustomerAnalytic.objects.filter(
            company=self.company).all()
        try:
            customer_selected = CustomerAnalytic.objects.get(pk=pk)
            schedule_services = customer_selected.get_schedule_services(
                self.start_date, self.end_date)
        except CustomerAnalytic.DoesNotExist:
            customer_selected = None
        return self.render_to_response({
            'customer_selected': customer_selected,
            'schedule_services': schedule_services,
            'customers': customers,
            'start_date': self.start_date,
            'end_date': self.end_date})


class VisitView(LoginRequiredMixin, TimeCompanyMixin, TemplateResponseMixin, View):
    template_name = 'analytics/visit.html'

    def get(self, request):
        schedules = ScheduleAnalytic.objects.filter_by_passed_fields(
            self.start_date, self.end_date)
        customers = schedules.values('customer')
        return self.render_to_response({
            'schedules': schedules,
            'customers': customers,
            'start_date': self.start_date,
            'end_date': self.end_date})
