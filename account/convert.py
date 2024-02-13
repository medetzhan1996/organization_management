from modal_convert.convert import ConvertToListOfDict
from .models import User, Company


class CompanyConvert(ConvertToListOfDict):

    class Meta:
        model = Company
        fields = {
            'id': 'pk',
            'title': 'title'
        }


class UserConvert(ConvertToListOfDict):

    class Meta:
        model = User
        fields = {
            'id': 'pk',
            'title': 'full_name'
        }
        extra = {
            'extendedProps': {
                'resource': 'user'
            }
        }
