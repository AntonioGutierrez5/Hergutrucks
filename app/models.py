from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy

class TipoVehiculo(models.Model):
    TIPO_CAMION = [
        ('cabezas', 'Cabezas Tractoras'),
        ('hormigonera', 'Hormigonera'),
        ('cisterna', 'Cisterna'),
        ('frigorifico', 'Frigorífico'),
        ('remolque', 'Remolque'),
    ]
    nombre = models.CharField(max_length=50, choices=TIPO_CAMION, unique=True)

    def __str__(self):
        return self.get_nombre_display()

class Vehiculo(models.Model):
    tipo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)  # Relación con TipoVehiculo
    disponible = models.BooleanField(default=True)  
    estado = models.CharField(
        max_length=10,
        choices=[('Disponible', 'Disponible'), ('Ocupado', 'Ocupado')],
        default='Disponible'
    )

    def __str__(self):
        return f"{self.tipo} - {self.estado}"



class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Modificación aquí
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)  # Añadir tipo_vehiculo
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Reserva de {self.usuario} para {self.vehiculo} del {self.fecha_inicio} al {self.fecha_fin}"

    class Meta:
        unique_together = ('vehiculo', 'fecha_inicio', 'fecha_fin')

    def clean(self):
        if self.fecha_inicio >= self.fecha_fin:
            raise ValidationError('La fecha de inicio debe ser anterior a la fecha de fin.')
        if Reserva.objects.filter(
            vehiculo=self.vehiculo,
            fecha_inicio__lte=self.fecha_fin,
            fecha_fin__gte=self.fecha_inicio
        ).exists():
            raise ValidationError("El vehículo ya está reservado en esas fechas.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vehiculo.estado = "Ocupado"
        self.vehiculo.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if not Reserva.objects.filter(vehiculo=self.vehiculo).exists():
            self.vehiculo.estado = "Disponible"
            self.vehiculo.save()

    def __str__(self):
        return f"Reserva de {self.vehiculo.tipo} para {self.cliente.username}"



class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carrito')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def total(self):
        return sum(item.precio for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.vehiculo.tipo}"

    @property
    def precio(self):
        return (getattr(self.vehiculo, 'precio_venta', 0) or 0) * self.cantidad

class Comentario(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, related_name='comentarios', on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=200, default='Nombre desconocido')
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f"Comentario de {self.nombre_cliente} sobre {self.vehiculo.tipo}"

class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('index')


class ClienteComentario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(default='example@ejemplo.com')  # Valor por defecto
    comentario = models.TextField()
    aprobado = models.BooleanField(default=False)  # Campo booleano para aprobación
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación


    def __str__(self):
        return self.nombre
