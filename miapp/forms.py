from django import forms
from .models import *
from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
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
        fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono', 'direccion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select', 'choices': ESTADO_CHOICES, 'placeholder': 'Seleccione un estado',
                                          }),
        }

        labels = {
            'nombre': 'Nombre :',
            'apellido': 'Apellido:',
            'cedula': 'Cédula:',
            'correo': 'Correo electrónico:',
            'telefono': 'Teléfono:',
            'direccion': 'Dirección:',
            'estado': 'Estado:',
        }


class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor
        fields = ['nombre', 'marca', 'ruc', 'correo', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre :',
            'marca': 'Marca:',
            'ruc': 'RUC:',
            'correo': 'Correo electrónico:',
            'telefono': 'Teléfono:',
            'direccion': 'Dirección:',
        }

class ProductoForm(forms.ModelForm):
    cantidad_ingresar = forms.IntegerField(
        required=False,
        label='Cantidad a Ingresar:',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cantidad a agregar al stock',
        })
    )

    class Meta:
        model = Producto
        fields = [
            'numero_serie', 'lote', 'bodega', 'imagen', 'nombre', 'modelo',
            'color', 'categoria', 'precio', 'stock'
        ]
        widgets = {
            'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de serie',
                'maxlength': '100'
            }),
            'lote': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lote del producto',
                'maxlength': '50'
            }),
            'bodega': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Seleccione una bodega'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'placeholder': 'Seleccione una imagen del producto'
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
                'maxlength': '100'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Precio en dólares'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Stock disponible'
            }),
        }
        labels = {
            'numero_serie': 'Número de Serie:',
            'lote': 'Lote:',
            'bodega': 'Bodega:',
            'imagen': 'Imagen del Producto:',
            'nombre': 'Nombre:',
            'modelo': 'Modelo:',
            'color': 'Color:',
            'categoria': 'Categoría:',
            'precio': 'Precio Unitario ($):',
            'stock': 'Stock:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Siempre marcar stock como NO obligatorio
        self.fields['stock'].required = False

        if not self.instance.pk:
            # Producto nuevo → ocultar campo stock
            self.fields['stock'].widget = forms.HiddenInput()
        else:
            # Producto existente → campo stock solo lectura
            self.fields['stock'].widget.attrs['readonly'] = False

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'fecha_compra', 'numero_factura', 'subtotal', 'iva', 'total']  # sin estado

        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'fecha_compra': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control'}),
            'iva': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BuscadorCompraForm(forms.Form):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        label='Proveedor',
        required=False,
        empty_label="-- Seleccione proveedor --",
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
        }),
        input_formats=['%Y-%m-%d'],  # Formato estándar HTML date input
    )

    fecha_fin = forms.DateField(
        label='Hasta',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        input_formats=['%Y-%m-%d'],
    )



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




##########################Proveedor#########################




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
    id = forms.CharField(max_length=50, required=False)
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




ESTADO_CHOICES = [
    ('', 'Todos'),
    ('1', 'Activo'),
    ('0', 'Inactivo'),
]

class BuscarClienteForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=False)
    apellido = forms.CharField(max_length=50, required=False)
    cedula = forms.CharField(max_length=15, required=False)

    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    fecha = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Seleccione la fecha de creación',
                'type': 'date',
                'class': 'form-control'
            }
        )
    )


class BuscarProductoForm(forms.Form):
    nombre = forms.CharField(max_length=20, required=False)
    categoria = forms.CharField(max_length=40, required=False)
    numero_serie = forms.CharField(max_length=20, required=False)
    estado = forms.ChoiceField(
        choices=[('', 'Todos'), ('1', 'Activo'), ('0', 'Inactivo')],
        required=False
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

class RegistroUsuarioForm(UserCreationForm):
    nombre = forms.CharField(max_length=50, label="Nombre")
    apellido = forms.CharField(max_length=50, label="Apellido")
    cedula = forms.CharField(max_length=12, label="Cédula")
    correo = forms.EmailField(label="Correo electrónico")
    telefono = forms.CharField(max_length=15, label="Teléfono")
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.filter(estado=1), label="Cargo")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nombre', 'apellido', 'cedula', 'correo', 'telefono', 'cargo']

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            Empleado.objects.create(
                user=user,
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                cedula=self.cleaned_data['cedula'],
                correo=self.cleaned_data['correo'],
                telefono=self.cleaned_data['telefono'],
                cargo=self.cleaned_data['cargo'],
                creacion_usuario=user.username,
                modificacion_usuario=user.username,
            )
        return user



class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(max_length=20, label="Nombre")
    apellido = forms.CharField(max_length=20, label="Apellido")
    cedula = forms.CharField(max_length=12)
    correo = forms.EmailField()
    telefono = forms.CharField(max_length=12)
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all(), label="Cargo")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'nombre', 'apellido', 'cedula', 'correo', 'telefono', 'cargo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if Empleado.objects.filter(correo=correo).exists():
            raise ValidationError("Ya existe un empleado con este correo electrónico.")
        return correo

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Empleado.objects.create(
                user=user,
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                cedula=self.cleaned_data['cedula'],
                correo=self.cleaned_data['correo'],
                telefono=self.cleaned_data['telefono'],
                cargo=self.cleaned_data['cargo'],
                creacion_usuario=user.username,
                modificacion_usuario=user.username
            )
        return user