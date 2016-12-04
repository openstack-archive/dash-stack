from django.contrib import admin
from .models import Provider, Type

class ProviderAdmin(admin.ModelAdmin):
    model = Provider
    list_display = ['id', 'name', 'provider', 'enabled', 'validated']

class TypeAdmin(admin.ModelAdmin):
    model = Type
    list_display = ['id', 'name', 'type', 'logo']

admin.site.register(Provider,ProviderAdmin)
admin.site.register(Type,TypeAdmin)