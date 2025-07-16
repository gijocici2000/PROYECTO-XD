from django.db import models
from miapp.models import Proveedor, Producto
from decimal import Decimal

class Compra(models.Model):
    proveedor = models.ForeignKey(
        Proveedor, 
        on_delete=models.CASCADE, 
        related_name='compras_compras'
    )
    fecha_compra = models.DateField()
    numero_factura = models.CharField(max_length=20)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra {self.numero_factura} - {self.proveedor.nombre}"

class Detalle_Compra(models.Model):
    compra = models.ForeignKey(
        Compra, 
        on_delete=models.CASCADE, 
        related_name="detalles_compras"
    )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE, 
        related_name='detallecompras_compras'
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    iva_aplicado = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('12.00'))

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    @property
    def valor_iva(self):
        return self.subtotal * (self.iva_aplicado / 100)

    @property
    def total(self):
        return self.subtotal + self.valor_iva

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"