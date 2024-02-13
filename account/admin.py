from rest_framework.authtoken.models import Token
from django.contrib import admin
from .models import User, Industry, Company, FuncStructure, Speciality

admin.site.register(User)
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(FuncStructure)
admin.site.register(Speciality)



@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    ordering = ('-created',)
