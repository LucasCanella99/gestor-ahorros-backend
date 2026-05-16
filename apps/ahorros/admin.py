from django.contrib import admin
from .models import SafeBox, Alcancia, Movimiento

# Register your models here.

admin.site.register(SafeBox)
admin.site.register(Alcancia)
admin.site.register(Movimiento)