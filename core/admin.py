from django.contrib import admin
from .models import *

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('autor','pais')
    search_fields = ('autor','pais')
    list_filter = ('pais',)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo','idioma','paginas','fecha_publicacion','mostrar_autores')
    filter_horizontal = ('autores',)

    def mostrar_autores(self, obj):
        return ", ".join([a.autor for a in obj.autores.all()])
    
    mostrar_autores.short_description = 'Autores'