from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),

    # Cliente
    path('cliente/crear/', views.crear_cliente, name='crear_cliente'),
    path('cliente/consultar/', views.consultar_cliente, name='consultar_cliente'),
    path('cliente/modificar/<int:id>/', views.modificar_cliente, name='modificar_cliente'),
    path('cliente/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

    # Producto
    path('producto/crear/', views.crear_producto, name='crear_producto'),
    path('producto/consultar/', views.consultar_producto, name='consultar_producto'),
    path('producto/modificar/<int:id>/', views.modificar_producto, name='modificar_producto'),
    path('producto/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # Descuento
    path('descuento/consultar/', views.consultar_descuento, name='consultar_descuento'),
    path('descuento/crear/', views.crear_descuento, name='crear_descuento'),
    path('descuento/eliminar/', views.eliminar_descuento, name='eliminar_descuento'),
    path('descuento/modificar/', views.modificar_descuento, name='modificar_descuento'),

   
  

    # Proveedor
    path('proveedor/consultar/', views.consultar_proveedor, name='consultar_proveedor'),
    path('proveedor/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedor/eliminar/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('proveedor/modificar/', views.modificar_proveedor, name='modificar_proveedor'),

    # Bodega
    path('bodega/consultar/', views.consultar_bodega, name='consultar_bodega'),
    path('bodega/crear/', views.crear_bodega, name='crear_bodega'),
    path('bodega/eliminar/', views.eliminar_bodega, name='eliminar_bodega'),
    path('bodega/modificar/', views.modificar_bodega, name='modificar_bodega'),

    # Bodega Detalle
    path('bodega_detalle/consultar/', views.consultar_bodega_detalle, name='consultar_bodega_detalle'),
    path('bodega_detalle/crear/', views.crear_bodega_detalle, name='crear_bodega_detalle'),
    path('bodega_detalle/eliminar/', views.eliminar_bodega_detalle, name='eliminar_bodega_detalle'),
    path('bodega_detalle/modificar/', views.modificar_bodega_detalle, name='modificar_bodega_detalle'),

    # Empleado
    path('empleado/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleado/modificar/', views.modificar_empleado, name='modificar_empleado'),
    path('empleado/consultar/', views.consultar_empleado, name='consultar_empleado'),
    path('empleado/eliminar/', views.eliminar_empleado, name='eliminar_empleado'),

    # Factura
    path('factura/crear/', views.crear_factura, name='crear_factura'),
    path('factura/consultar/', views.consultar_factura, name='consultar_factura'),
    path('factura/modificar/<int:id>/', views.modificar_factura, name='modificar_factura'),
    path('factura/eliminar/<int:id>/', views.eliminar_factura, name='eliminar_factura'),
    
    #factura_detalle
   

    # Cotización
    path('cotizacion/consultar/', views.consultar_cotizacion, name='consultar_cotizacion'),
    path('cotizacion/crear/', views.crear_cotizacion, name='crear_cotizacion'),
    path('cotizacion/eliminar/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
    path('cotizacion/modificar/', views.modificar_cotizacion, name='modificar_cotizacion'),

    #cotizacion_detalle

]
