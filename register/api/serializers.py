from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from account.models import User
from customer.models import Customer
from register.models import Schedule


class ScheduleCreateSerializer(serializers.ModelSerializer):
    doctor_code = serializers.CharField(write_only=True)
    customer_iin = serializers.CharField(write_only=True)

    class Meta:
        model = Schedule
        fields = ('doctor_code', 'start_datetime', 'customer_iin')

    def create(self, validated_data):
        doctor_code = validated_data.pop('doctor_code')
        start_datetime = validated_data.get('start_datetime')
        print(doctor_code, '---------=--=======')
        customer_iin = validated_data.pop('customer_iin')
        customer = Customer.objects.get(iin=customer_iin)
        user = User.objects.get(doctor_code=doctor_code)

        # Получить content_type для модели User
        content_type = ContentType.objects.get_for_model(user)

        # Создать новый объект Schedule, указав content_type и user
        schedule = Schedule.objects.create(
            content_type=content_type,
            object_id=user.id,  # Используйте ID пользователя как object_id
            duration=30,  # Установите значение по умолчанию для duration
            status=0,  # Установите значение по умолчанию для status
            comment='',  # Установите значение по умолчанию для comment
            register=user,
            customer=customer,# Установите register в None
            start_datetime=start_datetime
        )

        return schedule
