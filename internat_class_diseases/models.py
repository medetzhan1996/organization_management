from django.db import models
from django.db.models import Q
from mptt.models import MPTTModel, TreeForeignKey


class Conclusion(models.Model):
    title = models.CharField(max_length=240)

    def __str__(self):
        return self.title

# МКБ-10
class MKB10(MPTTModel):
    title = models.CharField(max_length=240)
    code = models.CharField(max_length=180, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    def __str__(self):
        return self.title

    def get_as_json(parent=None, search=None):
        data = []
        tree_list = []
        mkb10 = MKB10.objects.all()
        if search:
            mkb10 = mkb10.filter(
                Q(title__icontains=search) | Q(code__icontains=search))
        else:
            mkb10 = mkb10.filter(parent=parent)
        for val in mkb10:
            tree_list.append(val.id)
            if not val.parent or val.parent.id not in tree_list:
                item = {
                    'id': val.id
                }
                name = val.title + '(<b>' + val.code + '</b>)'
                if not val.is_leaf_node():
                    item['load_on_demand'] = True
                else:
                    name = '<span class="get-mkb10">' + name + '</span>'
                item['name'] = name
                data.append(item)
        return data
