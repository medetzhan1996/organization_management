from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.base import View
from django.views.generic.list import ListView

from .api.client import get_covered_services
from .models import CategoryService, Service
from .forms import CategoryServiceForm, ServiceForm


# Услуги в категориях
class ServiceInCategoryListView(LoginRequiredMixin, ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'service_system/service_in_category/list.html'
    active_category = None

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.kwargs.get('category', None)
        if category:
            qs = qs.filter(category=category)
            self.active_category = get_object_or_404(
                CategoryService, pk=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_category'] = self.active_category
        context['categories'] = CategoryService.objects.all()
        return context


# Добавить категорию услуг
class CategoryServiceCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = CategoryServiceForm(request)
        return render(request, 'service_system/category_service/form.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = CategoryServiceForm(request, data=request.POST)
        if form.is_valid():
            category = form.save()
            return render(
                request, 'service_system/category_service/list.html',
                {'category': category})


# Удалить категорию услуг
class CategoryServiceDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            category_service_obj = CategoryService.objects.get(pk=pk)
            category_service_obj.delete()
            return JsonResponse({'status': True})
        except CategoryService.DoesNotExist:
            return JsonResponse({'status': False})


# Добавить услугу
class ServiceCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        category = kwargs.get('category', None)
        form = ServiceForm(initial={'category': category})
        return render(request, 'service_system/service/form.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        return JsonResponse({'status': False})


# Обновить услугу
class ServiceUpdateView(LoginRequiredMixin, View):

    def dispatch(self, *args, **kwargs):
        self.pk = self.kwargs.get('pk')
        self.service = get_object_or_404(Service, pk=self.pk)
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = ServiceForm(instance=self.service)
        return render(request, 'service_system/service/update.html',
                      {'form': form, 'pk': self.pk})

    def post(self, request, *args, **kwargs):
        form = ServiceForm(request.POST, instance=self.service)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        return JsonResponse({'status': False})


# Удалить услугу
class ServiceDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            service_obj = Service.objects.get(pk=pk)
            service_obj.delete()
            return JsonResponse({'status': True})
        except Service.DoesNotExist:
            return JsonResponse({'status': False})


# Поиск услугу
class ServiceSearchView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        services = Service.objects.filter(
            title__icontains=request.GET.get('q'), parent=None)[:5]
        values = [{
            'id': service.id,
            'title': service.title,
            'price': service.price,
            'duration': service.duration,
            'equipments': [{
                'id': equipment.id,
                'title': equipment.title
            } for equipment in service.equipments.all()]
        } for service in services]
        return JsonResponse(values, safe=False)


# Поиск услугу
class CoveredServiceApiView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        hospital = 'markezi_clinik'
        card_number = request.POST.get('card_number')
        icd = request.POST.get('icd')
        type_appeal = request.POST.get('type_appeal')
        place = request.POST.get('place')
        covered_services = get_covered_services(card_number=card_number,
                                                hospital=hospital, icd=icd,
                                                type_appeal=type_appeal, place=place)
        print(covered_services, 'test................')
        return JsonResponse(covered_services, safe=False)
