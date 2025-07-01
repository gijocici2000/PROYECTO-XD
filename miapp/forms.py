from django import forms
from .models import *
from django.forms import modelformset_factory


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['apellido', 'nombre', 'cedula', 'cargo']
        widgets = {
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
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
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'nombre': 'Nombre:',
            'modelo': 'Modelo:',
            'color': 'Color:',
            'numero_serie': 'Número de serie:',
            'categoria': 'Categoría:',
            'unidad': 'Unidad de medida:',
            'precio': 'Precio unitario:',
        }



#########################Factura y Factura Detalle#########################


from django import forms
from .models import Factura

class FacturaForm(forms.ModelForm):
    
    class Meta:
        model = Factura
        fields = ['cliente', 'sucursal', 'empleado', 'comentario', 'descuento']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'cliente': 'Cliente:',
            'sucursal': 'Sucursal:',
            'empleado': 'Empleado:',
            'comentario': 'Comentario:',
            'descuento': 'Descuento:',
        }


#############################Factura Detalle Form
class FacturaDetalleForm(forms.ModelForm):
    class Meta:
        model = Factura_Detalle
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
        }
        labels = {
            'producto': 'Producto:',
            'cantidad': 'Cantidad:',
        }


# Formset para manejar múltiples líneas de detalle de factura
FacturaDetalleFormSet = modelformset_factory(
    Factura_Detalle,
    form=FacturaDetalleForm,
    extra=1,       # Número de líneas vacías al iniciar
    can_delete=True  # Permite eliminar líneas si estás en modo edición
)
###########################factura_detalle_formset#########################



##########################Proveedor#########################

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
        fields = ['codigo_producto', 'descripcion', 'porcentaje']
        widgets = {
            'codigo_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'codigo_producto': 'Código_producto:',
            'descripcion': 'Descripción:',
            'porcentaje': 'Porcentaje de descuento:',
        }   
    
###########################Bodega y Bodega Detalle#########################
class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ['nombre', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre :',
            'direccion': 'Dirección:',
        }
class BodegaDetalleForm(forms.ModelForm):
    class Meta:
        model = Bodega_Detalle
        fields = ['bodega', 'producto', 'cantidad']
        widgets = {
            'bodega': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
        }
        labels = {
            'bodega': 'Bodega:',
            'producto': 'Producto:',
            'cantidad': 'Cantidad:',
        }

##########################Cotización y Cotización Detalle#########################

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = [
            'cotizacion_codigo',
            'cliente',
            'contacto',
            'correo',
            'comentario'
        ]
        widgets = {
            'fecha_cotizacion': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Seleccione una fecha',
                    'type': 'date',
                    'size': 30
                }
            ),
        }
class CotizacionDetalleForm(forms.ModelForm):
    class Meta:
        model = Cotizacion_Detalle
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-control',
                'id': 'cotizacion_detalle_producto',
            }),
            'cantidad': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'cotizacion_detalle_cantidad',
                'placeholder': '0',
                'type': 'number',
            }),
        }   
class CotizacionDetalleFormSet(forms.BaseFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        total = 0
        for form in self.forms:
            if form.cleaned_data and 'cantidad' in form.cleaned_data:
                cantidad = form.cleaned_data['cantidad']
                if cantidad <= 0:
                    raise forms.ValidationError("La cantidad debe ser mayor que cero.")
                total += cantidad

        if total <= 0:
            raise forms.ValidationError("Debe haber al menos un producto con cantidad mayor que cero.")



###########################Buscar Formularios#########################


class BuscarDescuentoForm(forms.Form):
    codigo = forms.CharField(max_length=50, required=False)
    descripcion = forms.CharField(max_length=100, required=False)
    porcentaje = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
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

class BuscarBodegaDetalleForm(forms.Form):

    bodega = forms.ModelChoiceField(
        queryset=Bodega.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
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

class BuscarBodegaForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=False)
    direccion = forms.CharField(max_length=100, required=False)
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