
class ConvertSetOptions:

    def __init__(self, options=None):
        self.model = getattr(options, 'model', None)
        self.fields = getattr(options, 'fields', None)
        self.extra = getattr(options, 'extra', None)


class ConvertSetMetaclass(type):

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        new_class._meta = ConvertSetOptions(getattr(new_class, 'Meta', None))
        return new_class


class BaseConvert:

    def __init__(self, queryset=None):
        self.queryset = queryset
        if queryset is None:
            queryset = self._meta.model._default_manager.all()

    def convert_to_dict(self, query):
        data = {}
        if self._meta.fields:
            for key, field in self._meta.fields.items():
                field_split = field.split("__")
                attr_val = getattr(query, field_split[0])
                try:
                    attr_val = getattr(attr_val, field_split[1])
                except IndexError:
                    pass
                try:
                    attr_val = getattr(attr_val, field_split[2])
                except IndexError:
                    pass
                key = key or field
                data[key] = attr_val
                if self._meta.extra:
                    data = {**data, **self._meta.extra}
        elif self._meta.extra:
            data = {**data, **self._meta.extra}
        return data

    def convert_to_list_of_dict(self):
        try:
            data = [self.convert_to_dict(val) for val in self.queryset]
        except TypeError:
            data = [self.convert_to_dict(self.queryset)]
        return data


class ConvertToListOfDict(BaseConvert, metaclass=ConvertSetMetaclass):
    pass
