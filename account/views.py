from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic.base import View


class IdentifyRole(View):

    def get(self, request):
        if request.user.user_type == 2:
            return redirect('register:index')
        elif request.user.user_type == 3:
            return redirect('inspection:reception_with_action_list')


# получить приоритетного пользователя
class UserPriorityView(View):

    def get(self, request, *args, **kwargs):
        company = self.request.user.company
        user = company.get_priority_user(is_display_calendar=True)
        return JsonResponse({'id': user.id})


# получить приоритетного оборудования
class EquipmentPriorityView(View):

    def get(self, request, *args, **kwargs):
        company = self.request.user.company
        equipment = company.get_priority_equipment()
        return JsonResponse({'id': equipment})
