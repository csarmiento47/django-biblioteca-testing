from django.shortcuts import redirect
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Avg, Sum, Max, Min
from django.contrib.auth import login



from .models import *
from .forms import *
from .mixins import AuthRequiredMixin, AdminRequiredMixin, EditRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView


#Home
class HomeView(TemplateView):
    template_name = 'core/index.html'


# =========================
# AUTORES
# =========================
class AutorListView(ListView):
    model = Autor
    template_name = 'core/autor/autor_list.html'
    context_object_name = 'autores'
    
    def get_queryset(self):
        qs = super().get_queryset()
        nombre = self.request.GET.get('autor')
        pais = self.request.GET.get('pais')

        if nombre:
            qs = qs.filter(autor__icontains=nombre)
        if pais:
            qs = qs.filter(pais__icontains=pais)

        return qs

class AutorCreateView(AuthRequiredMixin, EditRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Autor
    form_class = AutorForm
    template_name = 'core/autor/autor_form.html'
    success_url = reverse_lazy('autor_list')
    permission_required = 'core.add_autor'
    raise_exception = True

    def form_valid(self, form):
        messages.success(self.request, 'Autor creado correctamente')
        return super().form_valid(form)

class AutorUpdateView(AuthRequiredMixin, EditRequiredMixin, UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'core/autor/autor_form.html'
    success_url = reverse_lazy('autor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Autor actualizado correctamente')
        return super().form_valid(form)

class AutorDeleteView(AuthRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, pk):
        autor = get_object_or_404(Autor, pk=pk)
        autor.delete()
        messages.success(request, 'Autor eliminado correctamente')
        return redirect('autor_list')


class AutorDetailView(DetailView):
    model = Autor
    template_name = 'core/autor/autor_detail.html'
    context_object_name = 'autor'


# =========================
# LIBROS
# =========================
class LibroListView(ListView):
    model = Libro
    template_name = 'core/libro/libro_list.html'
    context_object_name = 'libros'

    def get_queryset(self):
        qs = super().get_queryset()

        titulo = self.request.GET.get('titulo')
        idioma = self.request.GET.get('idioma')

        if titulo:
            qs = qs.filter(titulo__icontains=titulo)

        if idioma:
            qs = qs.filter(idioma=idioma)

        return qs
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = LibroForm()
        return context

class LibroCreateView(AuthRequiredMixin, EditRequiredMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'core/libro/libro_form.html'
    success_url = reverse_lazy('libro_list')

    def form_valid(self, form):
        messages.success(self.request,'Libro creado correctamente')
        return super().form_valid(form)

class LibroUpdateView(AuthRequiredMixin, EditRequiredMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'core/libro/libro_form.html'
    success_url = reverse_lazy('libro_list')

    def form_valid(self, form):
        messages.success(self.request,'Libro actualizado correctamente')
        return super().form_valid(form)

class LibroDeleteView(AuthRequiredMixin, AdminRequiredMixin, DeleteView):
    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        libro.delete()
        messages.success(request, 'Libro eliminado correctamente')
        return redirect('libro_list')

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'core/libro/libro_detail.html'
    context_object_name = 'libro'


# =========================
# ESTADISTICAS
# =========================
class EstadisticasView(AuthRequiredMixin, TemplateView):
    template_name = 'core/estadisticas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # =========================
        # Estadística general
        # =========================
        total_libros = Libro.objects.count()
        total_autores = Autor.objects.count()

        context['total_libros'] = total_libros
        context['total_autores'] = total_autores

        # =========================
        # Estadísticas Libros por autor
        # =========================
        libros_por_autor = (
            Autor.objects
            .annotate(total=Count('libros'))
            .order_by('-total', 'autor')
        )

        context['libros_por_autor'] = libros_por_autor

        # =========================
        # Estadísticas Libros por idioma
        # =========================
        libros_por_idioma = (
            Libro.objects
            .values('idioma')
            .annotate(total=Count('id'))
            .order_by('idioma')    
        )
        context['libros_por_idioma']  = libros_por_idioma


        # =========================
        # Estadísticas Autor con más libros
        # =========================
        autor_top = libros_por_autor.first() 
        context['autor_top'] = autor_top


        # =========================
        # Estadísticas Libros por año
        # =========================  
        libros_por_año = (
            Libro.objects
            .values('fecha_publicacion__year')
            .annotate(total=Count('id'))
            .order_by('fecha_publicacion__year')
        )    
        context['libros_por_año'] = libros_por_año


        # =========================
        # Estadísticas Autores sin libros
        # =========================     
        autores_sin_libros = (
            Autor.objects
            .annotate(total_libros=Count('libros'))
            .filter(total_libros=0)
        )
        context['autores_sin_libros'] = autores_sin_libros


        # =========================
        # Estadísticas por Autor
        # =========================  
        estadisticas_por_autor = (
            Autor.objects
            .annotate(promedio_paginas=Avg('libros__paginas'), total_libros=Count('libros'))
            .order_by('-promedio_paginas')
        )
        context['estadisticas_por_autor'] = estadisticas_por_autor

        return context
    

#Método para registrar a un autor mientras se realiza el registro de un libro vía AJAX
class AutorCreateAjaxView(AuthRequiredMixin, View):
    def post(self,request):
        form = AutorForm(request.POST)
        if form.is_valid():
            autor = form.save()
            return JsonResponse({
                'success': True,
                'id': autor.id,
                'nombre': str(autor)
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            },status=400)
        

class RegistroView(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'core/auth/registro.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect('home')
    

class CustomLoginView(LoginView):
    template_name = 'core/auth/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            next_url = request.GET.get('next')
            return redirect(next_url or 'home')
        return super().dispatch(request, *args, **kwargs)
    

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Sesión cerrada correctamente')
        return super().dispatch(request, *args, **kwargs)




