from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = "Sistema de Gestión de Ventas"

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

