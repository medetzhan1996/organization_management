import json
import requests
import weasyprint

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin

from cashier.api.client import api_invoice_create
from register.models import Schedule
from customer.api.client import get_customer_by_iin
from .models import Form, FormHistory, Marker, AdaptiveMarker,\
    ReadyPhrase, FuncStructureForm
from internat_class_diseases.models import MKB10, Conclusion
from .forms import ReadyPhraseForm
from register.api.services import create_examination_result

api2_url = '82.200.165.222:19603'
api2_token = '020a2cef2f0e05ece1e8ccb85f35706a28c75735'
insurance = 'insurance1'

# Заполнить форму внутри ИБ
class WriteFormInHistoryView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'document_circulation/form/form_in_history.html'

    def dispatch(self, request, *args, **kwargs):
        self.history = self.kwargs.get('history', None)
        self.form = self.kwargs.get('form', None)
        self.schedule = get_object_or_404(Schedule, id=self.kwargs.get('pk'))
        self.customer = self.schedule.customer
        if self.history:
            self.history = get_object_or_404(FormHistory, id=self.history)
        if self.form:
            self.form = get_object_or_404(Form, id=self.form)
        url_customer_search_api = 'http://82.200.165.222:19603/api/customer_personal_cabinet/customer/examination/appointment?insurance={}&iin={}'.format(insurance, self.customer.iin)
        result = requests.get(url_customer_search_api, headers={
            'Authorization': 'Token 020a2cef2f0e05ece1e8ccb85f35706a28c75735'})
        print(url_customer_search_api)

        result.raise_for_status()
        data = result.json()
        if data:
            self.appointments = data[0].get('Data', [])
        else:
            print("No data returned from API.")
            self.appointments = []

        url_customer_examination_result = 'http://{}/api/customer_personal_cabinet/customer/examination/result?insurance={}&iin={}'.format(api2_url, insurance, self.customer.iin)
        result2 = requests.get(url_customer_examination_result, headers={
            'Authorization': 'Token ' + api2_token})
        result2.raise_for_status()
        data2 = result2.json()
        self.mkbs = MKB10.objects.all()
        self.conclusions = Conclusion.objects.all()
        if data2:
            self.results = data2[0].get('Data', [])
        else:
            self.results = []
        url_package_list_api = 'http://{}/api/customer_personal_cabinet/api/package?insurance={}&iin={}'.format(
            api2_url, insurance, self.customer.iin)
        result3 = requests.get(url_package_list_api, headers={
            'Authorization': 'Token ' + api2_token})
        result3.raise_for_status()
        data_package = result3.json()
        if data_package:
            self.packages = data_package[0].get('Data', [])
        else:
            self.packages = []
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # markers = Marker.objects.filter(name__in=['sex'],
        #                                 kind='pacient').update(kind='customer')
        # print(markers)
        histories = FormHistory.objects.filter(
            customer=self.customer).order_by('-pk').all()
        insurances = get_customer_by_iin(self.customer.iin)
        final_data = []

        for appointment in self.appointments:
            entry = {
                'appointment': appointment,
                'result_data': None
            }

            for result in self.results:
                if result['examination_appointment'] == appointment['id']:
                    entry['result_data'] = result
                    break

            final_data.append(entry)

        return self.render_to_response({
            'history': self.history,
            'customer': self.customer,
            'histories': histories,
            'schedule': self.schedule,
            'insurances': insurances,
            'appointments': self.appointments,
            'results': self.results,
            'mkbs': self.mkbs,
            'final_data': final_data,
            'conclusions': self.conclusions,
            'packages': self.packages
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        status = request.POST.get('status', '')
        service = request.POST.get('usluga')
        type_appeal = request.POST.get('type_appeal')
        place = request.POST.get('place')
        customer_insurance = request.POST.get('card_number')
        icd = request.POST.get('icd')
        performing_doctor = user.username
        customer = self.customer.iin
        history = FormHistory.save_history(
            self.customer, request.POST,
            self.form, self.history, status, user)
        if status == 1:
            data = api_invoice_create(service=service, type_appeal=type_appeal, place=place,
                                      customer_insurance=customer_insurance, icd=icd, customer=customer,
                                      performing_doctor=performing_doctor)
        next_page = reverse('document_circulation:form_in_history', kwargs={
            'pk': self.schedule.id, 'history': history})
        return redirect(next_page)


# ИБ пациента
class HistoryPdfView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        history_id = self.kwargs.get('history')
        self.history = get_object_or_404(FormHistory, id=history_id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'document_circulation/history/detail.html',
                      {'history': self.history})

    def post(self, request, *args, **kwargs):
        data = {
            'history': self.history
        }
        html = render_to_string('document_circulation/history/pdf.html', data)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="form_{}.pdf"'.format(
            self.history)
        weasyprint.HTML(string=html).write_pdf(
            response, stylesheets=[weasyprint.CSS(
                settings.STATIC_ROOT + '/css/print_pdf.css')])
        return response


# ИБ пациента
class FuncStructureFormListView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'document_circulation/form_func_structure/list.html'

    def get(self, request, *args, **kwargs):
        func_structure = request.user.func_structure
        company = request.user.company
        func_structure_forms = FuncStructureForm.objects.filter(
            func_structure=func_structure,
            company_form__company=company).all()
        schedule = get_object_or_404(Schedule, id=self.kwargs.get('schedule'))
        return self.render_to_response(
            {'func_structure_forms': func_structure_forms, 'schedule': schedule})


# Удалить незавершенную ИБ
class HistoryDeleteView(LoginRequiredMixin, TemplateResponseMixin, View):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        schedule = request.POST.get('schedule')
        history = get_object_or_404(
            FormHistory, id=pk)
        history.delete()
        next_page = reverse('document_circulation:form_in_history', kwargs={
            'pk': schedule})
        return redirect(next_page)


# Связанные формы
class FormRelationView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        self.http_referer = request.META.get('HTTP_REFERER')
        self.company = request.user.company
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        next_page = request.GET.get('next_page', self.http_referer)
        company_forms = self.company.get_forms()
        return render(request, 'document_circulation/form_relation/form.html',
                      {'company_forms': company_forms, 'next_page': next_page})

    def post(self, request, *args, **kwargs):
        func_structure = request.user.func_structure
        next_page = request.POST.get('next_page', self.http_referer)
        relation_form = request.POST.get('relation_form')
        relation_markers = request.POST.getlist('relation_markers')
        options = {
            "form_id": relation_form,
            "markers": []
        }
        for marker_id in relation_markers:
            marker = Marker.objects.get(pk=marker_id)
            options['markers'].append(marker.name)
            AdaptiveMarker.objects.update_or_create(
                company=self.company,
                func_structure=func_structure,
                marker_id__id=marker_id,
                defaults={
                    'marker_id': marker_id,
                    'kind': 'parent',
                    'options': json.dumps(options),
                    'company': self.company,
                    'func_structure': func_structure,
                }
            )
        return redirect(next_page)


# Связанные формы
class MarkerRelationView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form_id = self.kwargs.get('form')
        form = get_object_or_404(Form, id=form_id)
        return render(request,
                      'document_circulation/marker_relation/list.html',
                      {'form': form})


# Удалить связанную форму маркера
class MarkerRelationDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            adaptive_marker = AdaptiveMarker.objects.get(pk=pk)
            adaptive_marker.delete()
            return JsonResponse({'status': True})
        except AdaptiveMarker.DoesNotExist:
            return JsonResponse({'status': False})


# Список готовых шаблонов
class ReadyPhraseJsonView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        marker = self.kwargs.get('marker')
        parent = request.GET.get('node', None)
        search = request.GET.get('search', '')
        marker = Marker.objects.get(pk=marker)
        if marker.kind == 'mkb10':
            if search:
                data = MKB10.get_as_json(None, search)
            else:
                if(parent):
                    data = MKB10.get_as_json(parent)
                else:
                    data = MKB10.get_as_json()
        else:
            if search:
                data = ReadyPhrase.get_as_json(marker, None, search)
            else:
                if(parent != '#'):
                    data = ReadyPhrase.get_as_json(marker, parent)
                else:
                    data = ReadyPhrase.get_as_json(marker, None)
        return JsonResponse(data, safe=False)


# Ввод текста по аудио диктовке
class AudioTextView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'document_circulation/audio_text/form.html'

    def get(self, request, *args, **kwargs):
        marker = request.GET.get('marker')
        return self.render_to_response({
            'marker': marker
        })


class ReadyPhraseListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        marker = self.kwargs.get('marker')
        ready_phrases = ReadyPhrase.objects.filter(
            user=user, marker=marker).all()
        return render(request, 'document_circulation/ready_phrase/list.html',
                      {'ready_phrases': ready_phrases})


class ReadyPhraseCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        marker = self.kwargs.get('marker')
        form = ReadyPhraseForm(user=user, marker=marker)
        return render(request, 'document_circulation/ready_phrase/create.html',
                      {'form': form, 'marker': marker})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = ReadyPhraseForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class ReadyPhraseUpdateView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        pk = self.kwargs.get('pk')
        self.ready_phrase = get_object_or_404(ReadyPhrase, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = ReadyPhraseForm(instance=self.ready_phrase)
        return render(request, 'document_circulation/ready_phrase/update.html',
                      {'form': form, 'ready_phrase': self.ready_phrase})

    def post(self, request, *args, **kwargs):
        form = ReadyPhraseForm(instance=self.ready_phrase, data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Удалить незавершенную ИБ
class ReadyPhraseDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            ready_phrase = get_object_or_404(ReadyPhrase, id=pk)
            ready_phrase.delete()
            return JsonResponse({'status': True})
        except ReadyPhrase.DoesNotExist:
            return JsonResponse({'status': False})


class AdminFormDetail(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'admin/document_circulation/form/detail.html'

    def get(self, request, *args, **kwargs):
        form = get_object_or_404(Form, id=kwargs.get('pk'))
        return self.render_to_response({
            'form': form
        })


class CreateExaminationResultView(View):

    def post(self, request, *args, **kwargs):
        examination_appointment = request.POST.get('examination_appointment_id')
        icd_code = request.POST.get('icd')
        conclusion_id = request.POST.get('conclusion')
        recommendations = request.POST.get('recommendations')
        icd = MKB10.objects.get(code=icd_code)
        conclusion = Conclusion.objects.get(id=conclusion_id)
        data = {
            'examination_appointment': examination_appointment,
            'icd': icd.id,
            'conclusion': conclusion.id,
            'recommendations': recommendations
        }
        examination_result = create_examination_result(data)
        return redirect('document_circulation:form_in_history', pk=31)
