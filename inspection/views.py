from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from actions.models import Action
from register.models import Schedule
from .utils import InspectionUtils


# Mixin клиентов на прием
class ReceptionMixin(LoginRequiredMixin, ListView):
    model = Schedule
    context_object_name = 'schedules'
    date = None
    mode = None

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        today = datetime.today().strftime('%Y-%m-%d')
        self.date = self.request.GET.get('date', today)
        self.mode = self.request.GET.get('mode', 'daily')
        if self.mode == 'weekly':
            start_end_week = InspectionUtils.get_start_end_week(self.date)
            start_date = start_end_week.get('start_date')
            end_date = start_end_week.get('end_date')
        else:
            start_date = self.date
            end_date = self.date
        qs = qs.filter_by_passed_fields(
            start_date, end_date).filter_content_type(
            get_user_model(), user.id).order_by('start_datetime__date')
        return qs


# Список клиентов на прием
class ReceptionWithActionListView(ReceptionMixin):
    template_name = 'inspection/reception_with_action/list.html'

    def get_context_data(self, **kwargs):
        today = datetime.today().strftime('%Y-%m-%d')
        context = super().get_context_data(**kwargs)
        context['actions'] = Action.objects.filter(
            user=self.request.user, created__date=today)
        context['statuses'] = []
        context['date'] = self.date
        context['mode'] = self.mode
        return context


# Список клиентов на прием
class ReceptionListView(ReceptionMixin):
    template_name = 'inspection/reception/list.html'
