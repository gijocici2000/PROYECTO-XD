from django import forms
from .models import *
from django.forms import modelformset_factory



class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre','apellido', 'cedula', 'cargo']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'apellido': 'Apellido:',
            'nombre': 'Nombre:',
            'cedula': 'Cédula:',
            'cargo': 'Cargo:',
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre :',
            'apellido': 'Apellido:',
            'cedula': 'Cédula:',
            'correo': 'Correo electrónico:',
            'telefono': 'Teléfono:',
            'direccion': 'Dirección:',
        
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'modelo',
            'color',
            'numero_serie',
            'categoria',
            'unidad',
            'precio',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'nombre': 'Nombre:',
            'modelo': 'Modelo:',
            'color': 'Color:',
            'numero_serie': 'Número de serie:',
            'categoria': 'Categoría:',
            'unidad': 'Unidades:',
            'precio': 'Precio unitario:',
        }



#########################Factura y Factura Detalle#########################



class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['sucursal', 'empleado', 'cliente', 'tipo_pago', 'fecha_emision', 'fecha_vencimiento', 'comentario']
        widgets = {
            'sucursal': forms.Select(attrs={'class': 'form-select'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-select'}),
            'fecha_emision': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

#############################Factura Detalle Form
class FacturaDetalleForm(forms.ModelForm):
    class Meta:
        model = Factura_Detalle
        fields = ['producto', 'cantidad', 'precio_factura', 'subtotal', 'descuento_total', 'iva', 'total_factura_valor']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_factura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'descuento_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'iva': forms.Select(attrs={'class': 'form-select'}),
            'total_factura_valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
        }

FacturaDetalleFormSet = modelformset_factory(
    Factura_Detalle,
    form=FacturaDetalleForm,
    extra=1,  # Número de filas vacías iniciales
    can_delete=True
)

###########################factura_detalle_formset#########################



##########################Proveedor#########################


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'marca', 'ruc', 'correo', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'producto': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre :',
            'marca': 'Marca:',
            'producto': 'Producto:',
            'ruc': 'RUC:',
            'correo': 'Correo electrónico:',
            'telefono': 'Teléfono:',
            'direccion': 'Dirección:',
        
        }

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = Descuento
        fields = ['producto', 'descripcion', 'descuento', 'fecha_inicio', 'fecha_final']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'producto': 'Producto:',
            'descripcion': 'Descripción:',
            'descuento': 'Descuento:',
            'fecha_inicio': 'Fecha de inicio:',
            'fecha_final': 'Fecha final:',
        } 
    

##########################Cotización y Cotización Detalle#########################

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['sucursal', 'empleado', 'cliente', 'fecha_emision', 'fecha_vencimiento', 'comentario']
        widgets = {
            'sucursal': forms.Select(attrs={'class': 'form-select'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha_emision': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CotizacionDetalleForm(forms.ModelForm):
    class Meta:
        model = Cotizacion_Detalle
        fields = ['producto', 'cantidad', 'precio_cotizacion', 'subtotal', 'descuento_total', 'iva', 'total_cotizacion_valor']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_cotizacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'descuento_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'iva': forms.Select(attrs={'class': 'form-select'}),
            'total_cotizacion_valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
        }

CotizacionDetalleFormSet = modelformset_factory(
    Cotizacion_Detalle,
    form=CotizacionDetalleForm,
    extra=1,
    can_delete=True
)




###########################Buscar Formularios#########################


class BuscarProveedorForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=False)
    ruc = forms.CharField(max_length=15, required=False)
    fecha = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Seleccione la fecha de creación',
                'type': 'date'
            }
        )
    )

class BuscarDescuentoForm(forms.Form):
    producto = forms.CharField(max_length=50, required=False)
    descuento = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    fecha = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Seleccione la fecha de creación',
                'type': 'date'
            }
        )
    )

class BuscarEmpleadoForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=False)
    apellido = forms.CharField(max_length=50, required=False)
    cedula = forms.CharField(max_length=15, required=False)
    fecha = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Seleccione la fecha de creación',
                'type': 'date'
            }
        )
    )

class BuscarCotizacionForm(forms.Form):
    cliente_cedula = forms.CharField(max_length=50, required=False)
    desde = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Desde',
                'type': 'date'
            }
        )
    )
    hasta = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Hasta',
                'type': 'date'
            }
        )
    )

class BuscarFacturaForm(forms.Form):
    cliente_cedula = forms.CharField(max_length=50, required=False)
    desde = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Desde',
                'type': 'date'
            }
        )
    )
    hasta = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Hasta',
                'type': 'date'
            }
        )
    )

class BuscarFacturaDetalleForm(forms.Form):
    factura_codigo = forms.CharField(max_length=50, required=False)
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Seleccione la fecha de creación',
                'type': 'date'
            }
        )
    )   


class BuscarClienteForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=False)
    apellido = forms.CharField(max_length=50, required=False)
    cedula = forms.CharField(max_length=15, required=False)
    fecha = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Seleccione la fecha de creación',
                'type': 'date'
            }
        )
    )

class BuscarProductoForm(forms.Form):
    nombre = forms.CharField(max_length=20, required=False)
    modelo = forms.CharField(max_length=40, required=False)
    numero_serie = forms.CharField(max_length=20, required=False)
    fecha = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Seleccione la fecha de creación',
                'type': 'date'
            }
        )
    )

class BuscarCotizacionDetalleForm(forms.Form):
    cotizacion_codigo = forms.CharField(max_length=50, required=False)
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Seleccione la fecha de creación',
                'type': 'date'
            }
        )
    )
