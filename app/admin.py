from django.contrib import admin
from .models import TipoVehiculo, Vehiculo, Comentario, ClienteComentario
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin




@admin.register(TipoVehiculo)
class TipoVehiculoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Cambié 'tipo' por 'nombre' para que coincida con el campo en el modelo
    search_fields = ('nombre',)  # Cambié 'tipo' por 'nombre' para que coincida con el campo en el modelo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'estado', 'disponible')  # Asegúrate de que 'disponible' está en el modelo
    ordering = ('tipo',)  # No uses 'disponible' aquí
    list_filter = ('estado',)  # No uses 'disponible' aquí


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'nombre_cliente', 'mensaje', 'aprobado', 'fecha_creacion')  # 'vehiculo' y 'nombre_cliente' son atributos del modelo Comentario
    list_filter = ('aprobado', 'fecha_creacion')  # 'aprobado' y 'fecha_creacion' son atributos del modelo Comentario
    search_fields = ('vehiculo__tipo__nombre', 'nombre_cliente', 'mensaje')  # Se cambió 'vehiculo__tipo__tipo' por 'vehiculo__tipo__nombre'
    ordering = ('-fecha_creacion',)
    actions = ['aprobar_comentarios']

    def aprobar_comentarios(self, request, queryset):
        queryset.update(aprobado=True)
        self.message_user(request, "Comentarios aprobados exitosamente.")
    aprobar_comentarios.short_description = "Aprobar comentarios seleccionados"



@admin.register(ClienteComentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'get_aprobado', 'get_fecha_creacion')
    list_filter = ('aprobado',)
    search_fields = ('nombre', 'comentario')

    def get_aprobado(self, obj):
        return obj.aprobado
    get_aprobado.admin_order_field = 'aprobado'  # Permite ordenar por este campo

    def get_fecha_creacion(self, obj):
        return obj.fecha_creacion
    get_fecha_creacion.admin_order_field = 'fecha_creacion'
