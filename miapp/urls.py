from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
        
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('no-autorizado/', views.no_autorizado, name='no_autorizado'),

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
    path('producto/exportar/', views.exportar_excel_producto, name='exportar_excel_producto'),

    #compra
    path('compra/crear/', views.crear_compra, name='crear_compra'),
    path('compra/consultar/', views.consultar_compra, name='consultar_compra'),
    path('compra/exportar/', views.exportar_pdf_compra, name='exportar_pdf_compra'),
    path('compra/modificar/<int:id>/', views.modificar_compra, name='modificar_compra'),
    path('compra/anular/<int:id>/', views.anular_compra, name='anular_compra'),
    path('compra/eliminar/<int:id>/', views.eliminar_compra, name='eliminar_compra'),
    path('compra/reporte-sri/', views.reporte_compras_sri, name='reporte_compras_sri'),
   

    # Descuento
    path('descuento/consultar/', views.consultar_descuento, name='consultar_descuento'),
    path('descuento/crear/', views.crear_descuento, name='crear_descuento'),
    path('descuento/eliminar/<int:id>/', views.eliminar_descuento, name='eliminar_descuento'),
    path('descuento/modificar/<int:id>/', views.modificar_descuento, name='modificar_descuento'),

    # Proveedor
    path('proveedor/consultar/', views.consultar_proveedor, name='consultar_proveedor'),
    path('proveedor/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedor/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('proveedor/modificar/<int:id>/', views.modificar_proveedor, name='modificar_proveedor'),

    # Empleado
    path('empleado/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleado/consultar/', views.consultar_empleado, name='consultar_empleado'),
    path('empleado/modificar/<int:id>/', views.modificar_empleado, name='modificar_empleado'),
    path('empleado/eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),

    # Factura
    path('factura/crear/', views.crear_factura, name='crear_factura'),
    path('factura/consultar/', views.consultar_factura, name='consultar_factura'),
    path('factura/modificar/<int:id>/', views.modificar_factura, name='modificar_factura'),
    path('factura/anular/<int:id>/', views.anular_factura, name='anular_factura'),
    path('factura/eliminar/<int:id>/', views.eliminar_factura, name='eliminar_factura'),
    path('factura_detalle/crear/', views.crear_factura_detalle, name='crear_factura_detalle'),
    path('exportacion_pdf_factura/<int:factura_id>', views.exportar_pdf_factura, name='exportar_pdf_factura'),
    #path('iniciar-pago-tarjeta/', views.iniciar_pago_tarjeta, name='iniciar_pago_tarjeta'),#



    # Cotización
    path('cotizacion/consultar/', views.consultar_cotizacion, name='consultar_cotizacion'),
    path('cotizacion/crear/', views.crear_cotizacion, name='crear_cotizacion'),
    path('cotizacion/eliminar/<int:cotizacion_id>/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
    path('cotizacion/modificar/<int:id>/', views.modificar_cotizacion, name='modificar_cotizacion'),
    path('exportar_pdf_cotizacion/<int:cotizacion_id>/', views.exportar_pdf_cotizacion, name='exportar_pdf_cotizacion'),

    # Cotización Detalle
    path('cotizacion_detalle/consultar/', views.consultar_cotizacion_detalle, name='consultar_cotizacion_detalle'),
    path('cotizacion_detalle/crear/', views.crear_cotizacion_detalle, name='crear_cotizacion_detalle'),
    path('cotizacion_detalle/eliminar/<int:id>/', views.eliminar_cotizacion_detalle, name='eliminar_cotizacion_detalle'),
    path('cotizacion_detalle/modificar/<int:id>/', views.modificar_cotizacion_detalle, name='modificar_cotizacion_detalle'),
]  
