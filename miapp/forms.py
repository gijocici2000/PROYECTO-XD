from django import forms
from .models import *
from django.forms import modelformset_factory
from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm 

from django.contrib.auth.models import User


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
    cantidad_ingresar = forms.IntegerField(
        min_value=1,
        label="Cantidad a ingresar:",
        error_messages={
            'required': "Este campo es obligatorio.",
            'min_value': "Debe ser al menos 1."
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la cantidad a agregar al stock',
            'min': '1'
        })
    )

    class Meta:
        model = Producto
        fields = [
            'numero_serie', 'nombre', 'modelo', 'color',
            'categoria', 'precio'
        ]
        widgets = {
            'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de serie',
                'maxlength': '100'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto',
                'maxlength': '100'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo del producto',
                'maxlength': '100'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Color',
                'maxlength': '50'
            }),
            'categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Categoría',
                'maxlength': '20'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Precio en dólares'
            }),
        }
        labels = {
            'numero_serie': 'Número de Serie:',
            'nombre': 'Nombre:',
            'modelo': 'Modelo:',
            'color': 'Color:',
            'categoria': 'Categoría:',
            'precio': 'Precio Unitario ($):',
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_cantidad_ingresar(self):
        cantidad = self.cleaned_data.get('cantidad_ingresar')
        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError("La cantidad a ingresar debe ser mayor que cero.")
        return cantidad
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
        fields = ['producto', 'cantidad_producto', 'precio_factura', 'subtotal', 'descuento_total', 'iva', 'total_factura_valor']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_producto': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
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
        fields = ['sucursal', 'empleado', 'cliente', 'comentario']  # Quité fecha_emision y fecha_vencimiento
        widgets = {
            'sucursal': forms.Select(attrs={'class': 'form-select'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CotizacionDetalleForm(forms.ModelForm):
    class Meta:
        model = Cotizacion_Detalle
        fields = ['producto', 'cantidad_producto', 'precio_cotizado', 'descuento_total', 'iva']  # Corrigí nombre campos según modelo
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_producto': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_cotizado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'descuento_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'iva': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'producto': 'Producto:',
            'cantidad_producto': 'Cantidad:',
            'precio_cotizado': 'Precio Cotizado ($):',
            'descuento_total': 'Descuento Total ($):',
            'iva': 'IVA:',
        }


CotizacionDetalleFormSet = inlineformset_factory(
    Cotizacion,
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

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ['username' , 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email