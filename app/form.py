# reservas/forms.py
from django import forms
from .models import ClienteComentario



class FormularioComentario(forms.ModelForm):
    class Meta:
        model = ClienteComentario  # Usa el nombre correcto del modelo
        fields = ['nombre', 'email', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }



class BuscarVehiculoForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=True,
        label='Buscar Vehículo',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por tipo de camión o estado'})
    )

