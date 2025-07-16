from django.urls import path
from . import views

urlpatterns = [
    path('compras/crear/', views.crear_compra, name='crear_compra'),
    path('compras/consultar/', views.consultar_compra, name='consultar_compra'),
    path('compras/exportar/<int:compra_id>/', views.exportar_pdf_compra, name='exportar_pdf_compra'),
    path('compras/reporte-sri/', views.reporte_compras_sri, name='reporte_compras_sri'),
]
