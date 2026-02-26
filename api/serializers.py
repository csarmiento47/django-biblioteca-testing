from core.models import *
from rest_framework import serializers

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = [
            'id',
            'autor',
            'pais'
        ]


class LibroSerializer(serializers.ModelSerializer):

    #Solo lectura (para mostrar el nombre del autor)
    autores_detalle = AutorSerializer(source='autores',many=True,read_only=True)

    #Escritura (usar IDs)
    autores = serializers.PrimaryKeyRelatedField(many=True,queryset=Autor.objects.all(),write_only=True)

    class Meta:
        model = Libro
        fields = [
            'id',
            'titulo',
            'fecha_publicacion',
            'paginas',
            'idioma',
            'autores',              #Para escritura POST/PUT
            'autores_detalle',      #para lectura GET
        ]