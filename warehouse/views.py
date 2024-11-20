from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.base import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import ListView
from django.forms.models import inlineformset_factory
from .forms import CategoryGoodForm, GoodForm, StorageForm, \
    StorageOperationForm
from .models import Good, CategoryGood, Storage, StorageOperation,\
    StorageOperationGood


# Товары в категориях
class GoodInCategoryListView(LoginRequiredMixin, ListView):
    model = Good
    context_object_name = 'goods'
    template_name = 'warehouse/good_in_category/list.html'
    active_category = None

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.kwargs.get('category', None)
        if category:
            qs = qs.filter(category=category)
            self.active_category = get_object_or_404(
                CategoryGood, pk=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_category'] = self.active_category
        context['categories'] = CategoryGood.objects.all()
        return context


# Добавить категорию товара
class CategoryGoodCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = CategoryGoodForm(request)
        return render(request, 'warehouse/category_good/form.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = CategoryGoodForm(request, data=request.POST)
        if form.is_valid():
            category = form.save()
            return render(
                request, 'warehouse/category_good/list.html',
                {'category': category})


# Удалить категорию товара
class CategoryGoodDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            category_good_obj = CategoryGood.objects.get(pk=pk)
            category_good_obj.delete()
            return JsonResponse({'status': True})
        except CategoryGood.DoesNotExist:
            return JsonResponse({'status': False})


# Добавить товар
class GoodCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        category = kwargs.get('category', None)
        form = GoodForm(initial={'category': category})
        return render(request, 'warehouse/good/form.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = GoodForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        return JsonResponse({'status': False})


# Обновить товар
class GoodUpdateView(LoginRequiredMixin, View):
    good = None

    def dispatch(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.good = get_object_or_404(Good, pk=pk)
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = GoodForm(instance=self.good)
        return render(request, 'warehouse/good/update.html',
                      {'good': self.good, 'form': form})

    def post(self, request, *args, **kwargs):
        form = GoodForm(data=request.POST, instance=self.good)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        return JsonResponse({'status': False})


# Удалить товар
class GoodDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            good_obj = Good.objects.get(pk=pk)
            good_obj.delete()
            return JsonResponse({'status': True})
        except Good.DoesNotExist:
            return JsonResponse({'status': False})


# Список категориев услуг
class StorageListView(LoginRequiredMixin, ListView):
    model = Storage
    context_object_name = 'storages'
    template_name = 'warehouse/storage/list.html'


# Добавить склад товаров
class StorageCreateView(View):

    def get(self, request, *args, **kwargs):
        form = StorageForm(request)
        return render(request, 'warehouse/storage/form.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = StorageForm(request, data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        return JsonResponse({'status': False})


# Удалить категорию товар
class StorageDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            storage_good_obj = Storage.objects.get(pk=pk)
            storage_good_obj.delete()
            return JsonResponse({'status': True})
        except Storage.DoesNotExist:
            return JsonResponse({'status': False})


# Приход товара на склад
class StorageOperationListView(LoginRequiredMixin, ListView):
    model = StorageOperationGood
    context_object_name = 'storage_good_operations'
    template_name = 'warehouse/arrival_good/list.html'
    ordering = ['-id']


# Mixin формы товара
class GoodFormMixin(LoginRequiredMixin, TemplateResponseMixin, View):
    storage_operation = None

    def get_formset(self, data=None):
        StorageOperationGoodFormSet = inlineformset_factory(
            StorageOperation,
            StorageOperationGood,
            fields=['good', 'quantity'],
            extra=0, can_delete=True)
        return StorageOperationGoodFormSet(instance=self.storage_operation,
                                           data=data)

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk:
            self.storage_operation = get_object_or_404(
                StorageOperation, id=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = StorageOperationForm(request.GET,
                                    instance=self.storage_operation)
        storage_operation_good_formset = self.get_formset()
        return self.render_to_response(
            {'form': form,
             'storage_operation_good_formset': storage_operation_good_formset})

    def post(self, request, *args, **kwargs):
        form = StorageOperationForm(
            request, data=request.POST,
            instance=self.storage_operation)
        storage_operation_good_formset = self.get_formset(data=request.POST)
        if form.is_valid() and storage_operation_good_formset.is_valid():
            storage_operation = form.save()
            storage_operation_goods = storage_operation_good_formset.save(
                commit=False
            )
            for storage_operation_good in storage_operation_goods:
                storage_operation_good.storage_operation = storage_operation
                storage_operation_good.save()
            deleted_objects = storage_operation_good_formset.deleted_objects
            for storage_operation_good in deleted_objects:
                storage_operation_good.delete()
            return redirect("warehouse:storage_operation_list")
        return self.render_to_response(
            {'form': form,
             'storage_operation_good_formset': storage_operation_good_formset})


# Приход товара на склад
class ArrivalGoodFormView(GoodFormMixin):
    template_name = 'warehouse/arrival_good/form.html'


# Списание товара на склад
class WriteOffGoodFormView(GoodFormMixin):
    template_name = 'warehouse/write_off_good/form.html'


# Продажа товара на склад
class SaleGoodFormView(GoodFormMixin):
    template_name = 'warehouse/sale/form.html'


# Поиск клиента
class GoodSearchView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        goods = Good.objects.filter(
            title__icontains=request.GET.get('q'))[:5]
        values = [{
            'id': good.id,
            'title': good.title} for good in goods]
        return JsonResponse(values, safe=False)
