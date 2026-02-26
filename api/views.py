from rest_framework.viewsets import ModelViewSet
from core.models import *
from .serializers import *
from .filters import LibroFilter

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework.response import Response


class AutorViewSet(ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

    permission_classes = [DjangoModelPermissions]

    #Búsqueda textual
    search_fields = ['autor','pais']
    
    #Filtros exactos
    filterset_fields = ['pais']

    ordering_fields = ['autor']
    ordering = ['autor']


class LibroViewSet(ModelViewSet):
    queryset = Libro.objects.all().distinct()
    serializer_class = LibroSerializer
    filterset_class = LibroFilter

    permission_classes = [DjangoModelPermissions]

    #Búsqueda textual
    search_fields = ['titulo']

    #Filtros exactos
    filterset_fields = {
        'idioma': ['exact'],
        'fecha_publicacion':['year','gte','lte'],
        'autores':['exact'], #por ID
    }

    ordering_fields = ['titulo', 'fecha_publicacion']
    ordering = ['titulo']



class UserPermissionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "permissions": list(request.user.get_all_permissions())
        })