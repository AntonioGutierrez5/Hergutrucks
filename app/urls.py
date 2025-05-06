from django.urls import path, include
from . import views
from .views import RegisterView, CustomLoginView, profile_view, VehiculoDetailView, VehiculoListView


urlpatterns = [
    path('', views.index, name='index'),
    path('vehiculos/cabezas/', views.cabezas, name='cabezas'),
    path('vehiculos/cisterna/', views.cisterna, name='cisterna'),
    path('vehiculos/hormigonera/', views.hormigonera, name='hormigonera'),
    path('vehiculos/frigorifico/', views.frigorifico, name='frigorifico'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),  # Nueva ruta para cerrar sesión
    path('accounts/profile/', profile_view, name='profile'),
    path('vehiculos/', views.vehiculo_list, name='vehiculo-list'),  # Ruta para la lista de vehículos
    path('buscar/', views.buscar, name='buscar'),
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('comentarios/', views.lista_comentarios, name='lista_comentarios'),
    path('agregar_comentario/', views.agregar_comentario, name='agregar_comentario'),

]
