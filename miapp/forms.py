from django import forms
from .models import *
from django.forms import modelformset_factory
##hola##


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
        fields = [
            "cliente",
            "sucursal",
            "empleado",
            "tipo_pago",
            "fecha_emision",
            "fecha_vencimiento",
            "comentario",
            "cantidad_productos",
            "subtotal",
            "descuento_total",
            "iva",
            "total",
            "anulada",
            "motivo_anulacion",
            "creacion_usuario",
            "modificacion_usuario",
            "estado",
        ]
        widgets = {
            "fecha_emision": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fecha_vencimiento": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "comentario": forms.Textarea(attrs={"rows": 3}),
            "motivo_anulacion": forms.Textarea(attrs={"rows": 3}),
        }


#############################Factura Detalle Form
class FacturaDetalleForm(forms.ModelForm):
    class Meta:
        model = Factura_Detalle
        fields = [
            "producto",
            "cantidad",
            "subtotal",  # Opcional si quieres calcularlo automáticamente
            "creacion_usuario",
            "modificacion_usuario",
            "estado",
        ]

# Formset para manejar múltiples líneas de detalle de factura
FacturaDetalleFormSet = modelformset_factory(
    Factura_Detalle,
    form=FacturaDetalleForm,
    extra=1,       # Número de líneas vacías al iniciar
    can_delete=True  # Permite eliminar líneas si estás en modo edición
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
        model = Factura
        fields = ['cliente', 'sucursal', 'empleado', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'cliente': 'Cliente:',
            'sucursal': 'Sucursal:',
            'empleado': 'Empleado:',
            'comentario': 'Comentario:',
            
        }

class CotizacionDetalleForm(forms.ModelForm):
     class Meta:
        model = Cotizacion_Detalle
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
Cotizacion_DetalleFormSet = modelformset_factory(
    Cotizacion_Detalle,
    form=CotizacionDetalleForm,
    extra=1,       # Número de líneas vacías al iniciar
    can_delete=True  # Permite eliminar líneas si estás en modo edición
)

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
