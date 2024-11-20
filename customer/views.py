from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic.base import View

from .api.client import get_customer_by_iin, get_customer_professional_examination_by_iin
from .forms import CustomerForm
from .models import Customer


# Mixin клиента
class CustomerMixin(View):
    pk = None
    customer = None

    def dispatch(self, request, *args, **kwargs):
        self.pk = self.kwargs.get('pk')
        self.customer = Customer.objects.get(pk=self.pk)
        return super().dispatch(request, *args, **kwargs)


# Поиск клиента
class CustomerSearchView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.filter(
            name__icontains=request.GET.get('q'))[:5]
        values = [{
            'id': customer.id,
            'name': customer.name} for customer in customers]
        return JsonResponse(values, safe=False)


# Поиск клиента
class CustomerApiSearchView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        search_val = request.GET.get('search_val')

        # Call the first API
        data1 = get_customer_by_iin(search_val)

        # Call the second API (I'm just guessing the function name here)
        data2 = get_customer_professional_examination_by_iin(search_val)

        # Combine the data from both APIs (this depends on the structure of your data)
        combined_data = {
            'data1': data1,
            'data2': data2,
        }

        return JsonResponse(combined_data, safe=False)


# Обновить клиента
class CustomerUpdateView(LoginRequiredMixin, CustomerMixin):

    def get(self, request, *args, **kwargs):
        url = reverse('customer:update', kwargs={'pk': self.pk})
        form = CustomerForm(
            request, instance=self.customer)
        return render(request, 'customer/form.html',
                      {'form': form,
                       'customer': self.customer, 'url': url})

    def post(self, request, *args, **kwargs):
        form = CustomerForm(request, data=request.POST, instance=self.customer)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({'status': True, 'id': obj.id, 'name': obj.name})
        return JsonResponse({'status': False})


# Создать клиента
class CustomerCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        url = reverse('customer:create')
        form = CustomerForm(request)
        return render(request, 'customer/form.html',
                      {'form': form, 'url': url})

    def post(self, request, *args, **kwargs):
        form = CustomerForm(request, data=request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({'status': True, 'id': obj.id, 'name': obj.name})
        return JsonResponse({'status': False})


# Детальная информация клиента
class CustomerDetailView(LoginRequiredMixin, CustomerMixin):

    def get(self, request, *args, **kwargs):
        return render(request, 'customer/detail.html',
                      {'customer': self.customer})


# Данные клиента
class CustomerDataView(LoginRequiredMixin, CustomerMixin):

    def get(self, request, *args, **kwargs):
        return render(request, 'customer/data.html',
                      {'customer': self.customer})
