from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from .models import Equipment


# Поиск услугу
class EquipmentSearchView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        equipments = Equipment.objects.filter(
            title__icontains=request.GET.get('q'))[:5]
        values = [{
            'id': equipment.id,
            'title': equipment.title
        } for equipment in equipments]
        return JsonResponse(values, safe=False)
