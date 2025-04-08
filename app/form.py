# reservas/forms.py
from django import forms
from .models import Reserva, Comentario, TipoVehiculo


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['vehiculo', 'fecha_inicio', 'fecha_fin', 'tipo_vehiculo']

    tipo_vehiculo = forms.ModelChoiceField(queryset=TipoVehiculo.objects.all(), required=True)


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nombre_cliente', 'mensaje']
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'mensaje': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu comentario aquí'}),
        }


class BuscarVehiculoForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=True,
        label='Buscar Vehículo',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por tipo de camión o estado'})
    )

