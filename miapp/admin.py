from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

# Personaliza el encabezado del admin
admin.site.site_header = "Sistema de Gestión de Ventas"

# --- Personalización del UserAdmin con datos desde Empleado ---

class EmpleadoInline(admin.StackedInline):
    model = Empleado
    can_delete = False
    verbose_name_plural = 'Empleado'
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (EmpleadoInline,)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Modifica la sección "Información personal" si el objeto ya existe
        if obj:
            personal_info = list(fieldsets[1][1]['fields'])
            for campo in ['first_name', 'last_name', 'email']:
                if campo in personal_info:
                    personal_info.remove(campo)
            fieldsets[1][1]['fields'] = tuple(personal_info)
        return fieldsets

    list_display = ('username', 'get_nombre', 'get_apellido', 'get_email', 'is_staff')

    @admin.display(description='Nombre')
    def get_nombre(self, obj):
        return obj.empleado.nombre if hasattr(obj, 'empleado') else ''

    @admin.display(description='Apellido')
    def get_apellido(self, obj):
        return obj.empleado.apellido if hasattr(obj, 'empleado') else ''

    @admin.display(description='Correo')
    def get_email(self, obj):
        return obj.empleado.correo if hasattr(obj, 'empleado') else ''

# Desregistramos el admin por defecto de User y registramos el nuevo
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# --- Registro de tus modelos personalizados ---
admin.site.register(Sucursal)
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Descuento)
admin.site.register(Cotizacion)
admin.site.register(Cotizacion_Detalle)
admin.site.register(Factura)
admin.site.register(Factura_Detalle)
admin.site.register(Cargo)
admin.site.register(Proveedor)
admin.site.register(Iva)
admin.site.register(Bodega)
