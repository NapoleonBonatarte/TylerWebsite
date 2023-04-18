from django.contrib import admin
from .models import Element

class ElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'atomic_number', 'atomic_weight')

admin.site.register(Element, ElementAdmin)