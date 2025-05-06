from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Vehiculo, TipoVehiculo, Carrito, ClienteComentario, ItemCarrito
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .form import FormularioComentario
from rest_framework import generics
from .serializer import VehiculoSerializer
from django.contrib.auth import logout, get_user_model
from datetime import date


def index(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'index.html', {'vehiculos': vehiculos})



# Vistas de Autenticación
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, '¡Cuenta creada con éxito!')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"Error en {field.label}: {error}")
        return super().form_invalid(form)

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    success_url = reverse_lazy('vehiculo-list')

def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile_view(request):
    return redirect(reverse('index'))


# Página principal
def index(request):
    return render(request, 'app/index.html')

# Listado de vehículos
@login_required
def vehiculo_list(request):
    vehiculos = Vehiculo.objects.all()
    tipos_vehiculo = TipoVehiculo.objects.all()
    context = {
        'vehiculos': vehiculos,
        'tipos_vehiculo': tipos_vehiculo,
    }
    return render(request, 'app/vehiculo_list.html', context)





# Filtrado por tipo de vehículo
@login_required
def tipo_vehiculo_view(request, tipo):
    vehiculos = Vehiculo.objects.filter(tipo__tipo=tipo)
    return render(request, f'app/{tipo.lower()}.html', {'vehiculos': vehiculos})


@login_required
def cabezas(request):
    vehiculos = Vehiculo.objects.filter(tipo__nombre="Cabeza Tractora")
    return render(request, 'app/cabezas.html', {'vehiculos': vehiculos})

@login_required
def hormigonera(request):
    vehiculos = Vehiculo.objects.filter(tipo__nombre="Hormigonera")
    return render(request, 'app/hormigonera.html', {'vehiculos': vehiculos})

@login_required
def cisterna(request):
    vehiculos = Vehiculo.objects.filter(tipo__nombre="Cisterna")
    return render(request, 'app/cisterna.html', {'vehiculos': vehiculos})

@login_required
def frigorifico(request):
    vehiculos = Vehiculo.objects.filter(tipo__nombre="Frigorifico")
    return render(request, 'app/frigorifico.html', {'vehiculos': vehiculos})




# Carrito de compras
@login_required
def agregar_al_carrito(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    # Verificar si el vehiculo ya está en el carrito
    item_carrito, created = ItemCarrito.objects.get_or_create(carrito=carrito, vehiculo=vehiculo)
    
    if not created:
        item_carrito.cantidad += 1  # Incrementar la cantidad si ya está en el carrito
        item_carrito.save()
    
    return redirect('ver_carrito')

@login_required
def eliminar_del_carrito(request, producto_id):
    # Suponiendo que el carrito está almacenado en la sesión
    carrito = request.session.get('carrito', [])
    
    # Eliminamos el producto del carrito
    carrito = [producto for producto in carrito if producto['id'] != producto_id]
    
    # Volvemos a guardar el carrito en la sesión
    request.session['carrito'] = carrito
    
    return redirect('carrito')  # Redirigir al carrito después de eliminar el producto




# Comentarios
def lista_comentarios(request):
    comentarios = ClienteComentario.objects.all().order_by('-fecha_creacion')  # Cambié 'fecha' por 'fecha_creacion'
    return render(request, 'app/lista_comentarios.html', {'comentarios': comentarios})

def agregar_comentario(request):
    if request.method == 'POST':
        formulario = FormularioComentario(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Comentario enviado correctamente.')
            return redirect('lista_comentarios')
    else:
        formulario = FormularioComentario()
    
    return render(request, 'app/agregar_comentario.html', {'formulario': formulario})

def mostrar_comentarios_pagina_principal(request):
    comentarios = ClienteComentario.objects.filter(aprobado=True).order_by('-fecha_creacion')[:2] # Muestra los 2 comentarios más recientes
    return render(request, 'index.html', {'comentarios_principales': comentarios})

def index_view(request):
    comentarios_principales = ClienteComentario.objects.filter(aprobado=True).order_by('-fecha_creacion')[:2]
    return render(request, 'index.html', {'comentarios_principales': comentarios_principales})



# Búsqueda de vehículos
@login_required
def buscar(request):
    consulta = request.GET.get('q', '').lower()

    # Diccionario de palabras clave y sus respectivas URLs
    paginas = {
        "cabezas": "cabezas",
        "frigorifico": "frigorifico",
        "cisterna": "cisterna",
        "hormigonera": "hormigonera"
    }

    # Buscar si la consulta coincide con alguna clave
    for palabra, url_name in paginas.items():
        if palabra in consulta:
            return redirect(reverse(url_name))  # Redirige a la página encontrada

    # Si no hay coincidencias, mostrar un mensaje
    return render(request, "app/busqueda_no_encontrada.html", {"consulta": consulta})




# API REST
class VehiculoListView(generics.ListCreateAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class VehiculoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
