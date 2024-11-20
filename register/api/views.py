# views.py
from rest_framework.generics import CreateAPIView
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from register.api.serializers import ScheduleCreateSerializer
from .services import get_free_slots_for_specializations_in_date_range
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from register.models import Schedule


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class FreeSlotsForSpecializationsInDateRangeView(APIView):

    def get(self, request):
        specializations = request.query_params.getlist('specialization')
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if not start_date_str or not end_date_str:
            return Response({'error': 'Both start_date and end_date are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        slots = get_free_slots_for_specializations_in_date_range(specializations, start_date, end_date)
        return Response(slots, status=status.HTTP_200_OK)

class ScheduleCreateView(CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleCreateSerializer

# class ScheduleCreateView(APIView):
#     def post(self, request):
#         doctor_code = request.data.get('doctor_code')
#         start_datetime = request.data.get('start_datetime')
#         customer_iin = request.data.get('customer_iin')
#         print(doctor_code)
#         return Response('test')

