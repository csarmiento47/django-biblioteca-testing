import django_filters
from core.models import Libro

class LibroFilter(django_filters.FilterSet):
    autor = django_filters.CharFilter(
        field_name='autores__autor',
        lookup_expr='icontains'
    )

    class Meta:
        model = Libro
        fields = ['autor','idioma']