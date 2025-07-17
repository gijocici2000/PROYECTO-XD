from django import forms
from .models import Proveedor, Producto

class CompraForm(forms.Form):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        label='Proveedor',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_compra = forms.DateField(
        label='Fecha de Compra',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    numero_factura = forms.CharField(
        label='Número de Factura',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

class DetalleCompraForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        label='Producto',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cantidad = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    precio = forms.DecimalField(
        label='Precio Unitario',
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class BuscadorCompraForm(forms.Form):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        label='Proveedor',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    numero_factura = forms.CharField(
        label='Número de Factura',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por N° de Factura'
        })
    )

    fecha_inicio = forms.DateField(
        label='Desde',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    fecha_fin = forms.DateField(
        label='Hasta',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )