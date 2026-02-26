from django.contrib import admin
from .models import Categoria, Carretera, Poblacion, Tramo

@admin.register(Tramo)
class TramoAdmin(admin.ModelAdmin):
    list_display = ('carretera', 'km_inicio', 'km_fin', 'pueblo_inicio', 'pueblo_fin', 'tipo_final')
    list_filter = ('carretera', 'tipo_final')

admin.site.register(Categoria)
admin.site.register(Carretera)
admin.site.register(Poblacion)