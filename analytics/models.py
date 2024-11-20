from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from account.models import User, Speciality
from register.models import Schedule, ScheduleService
from customer.models import Customer


# Create your models here.
class UserAnalytic(User):
    class Meta:
        proxy = True

    def get_quantity_schedule(
            self, start_date=None, end_date=None, status=None):
        query = Schedule.objects.filter_content_type(
            get_user_model(), self.id).filter_by_passed_fields(
            start_date, end_date, status)
        return query.count()

    def get_schedule_service_quantity(self, start_date=None,
                                      end_date=None, status=None):
        query = ScheduleServiceAnalytic.objects.filter(
            schedule__content_type=ContentType.objects.get_for_model(get_user_model()),
            schedule__object_id=self.id).filter_by_passed_fields(
            start_date, end_date, status)
        return query.count()

    def get_schedule_service_price_sum(self, start_date=None,
                                       end_date=None, status=None):
        query = ScheduleServiceAnalytic.objects.filter(
            schedule__content_type=ContentType.objects.get_for_model(get_user_model()),
            schedule__object_id=self.id).filter_by_passed_fields(
            start_date, end_date, status)
        return query.aggregate(Sum('price')).get('price__sum') or 0

    def get_quantity_schedule_by_register(
            self, start_date=None, end_date=None, status=None):
        query = ScheduleAnalytic.objects.filter(
            register=self).filter_by_passed_fields(
            start_date, end_date, status)
        return query.count()


class SpecialityAnalytic(Speciality):
    class Meta:
        proxy = True

    def get_schedule_service_quantity(self, start_date=None,
                                      end_date=None, status=None):
        users = self.user_set.all()
        query = ScheduleServiceAnalytic.objects.filter(
            schedule__content_type=ContentType.objects.get_for_model(
                get_user_model()), schedule__object_id__in=users).filter_by_passed_fields(
            start_date, end_date, status)
        return query.count()

    def get_schedule_service_price_sum(self, start_date=None,
                                       end_date=None, status=None):
        users = self.user_set.all()
        query = ScheduleServiceAnalytic.objects.filter(
            schedule__content_type=ContentType.objects.get_for_model(
                get_user_model()), schedule__object_id__in=users).filter_by_passed_fields(
            start_date, end_date, status)
        return query.aggregate(Sum('price')).get('price__sum') or 0


class CustomerAnalytic(Customer):
    class Meta:
        proxy = True

    def get_schedule_services(self, start_date=None,
                              end_date=None, status=None):
        query = ScheduleServiceAnalytic.objects.filter(
            schedule__customer=self).filter_by_passed_fields(
            start_date, end_date, status)
        return query


class ScheduleAnalytic(Schedule):

    class Meta:
        proxy = True

    @staticmethod
    def get_quantity_primary_customers(customers, date=None):
        result = ScheduleAnalytic.objects.filter(
            customer__in=customers).values(
            'customer').annotate(customer_count=Count('customer'))
        if date:
            result = result.filter(start_datetime__date__lte=date)
        return result.filter(customer_count=1).count()

    @staticmethod
    def get_quantity_repeated_customers(customers, date=None):
        result = ScheduleAnalytic.objects.filter(
            customer__in=customers).values(
            'customer').annotate(customer_count=Count('customer'))
        if date:
            result = result.filter(start_datetime__date__lte=date)
        return result.filter(customer_count__gt=1).count()


class ScheduleServiceQuerySet(QuerySet):

    def filter_by_passed_fields(self, start_date=None, end_date=None, status=None):
        query = self
        if start_date:
            query = query.filter(schedule__start_datetime__date__gte=start_date)
        if end_date:
            query = query.filter(schedule__start_datetime__date__lte=end_date)
        if status:
            query = query.filter(status=status)
        return query


class ScheduleServiceAnalytic(ScheduleService):
    objects = ScheduleServiceQuerySet.as_manager()

    class Meta:
        proxy = True
