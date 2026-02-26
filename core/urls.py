from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(),name='home'),

    path('autores/', AutorListView.as_view(), name='autor_list'),
    path('autores/nuevo/', AutorCreateView.as_view(), name='autor_create'),
    path('autores/<int:pk>/editar/', AutorUpdateView.as_view(), name='autor_update'),
    path('autores/<int:pk>/eliminar/', AutorDeleteView.as_view(), name='autor_delete'),
    path('autores/<int:pk>/', AutorDetailView.as_view(), name='autor_detail'),
    path('autores/ajax/crear/',AutorCreateAjaxView.as_view(),name='autor_create_ajax'),
    
    path('libros/',LibroListView.as_view(),name='libro_list'),
    path('libros/nuevo/',LibroCreateView.as_view(),name='libro_create'),
    path('libros/<int:pk>/editar/',LibroUpdateView.as_view(),name='libro_update'),
    path('libros/<int:pk>/eliminar/',LibroDeleteView.as_view(),name='libro_delete'),
    path('libros/<int:pk>/', LibroDetailView.as_view(), name='libro_detail'),

    path('estadisticas/',EstadisticasView.as_view(),name='estadisticas'),

    path('registro/', RegistroView.as_view(), name='registro')
]