from django.db import models
from django.utils import timezone
from decimal import Decimal

# ---------------------------administracion 
# SUCURSAL
# ---------------------------



class Sucursal(models.Model):
    nombre = models.CharField(max_length=30)
    ruc= models.CharField(max_length=13, default="")
    local = models.CharField(max_length=50)
    telefono = models.CharField(max_length=12)
    correo= models.EmailField(max_length=40, default="@")
    direccion = models.CharField(max_length=200)

    fecha_creacion = models.DateTimeField(auto_now_add=True , )
    fecha_modificacion = models.DateTimeField(auto_now=True , )
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "sucursal"
        verbose_name = "sucursal"
        verbose_name_plural = "sucursales"

    def __str__(self):
        return f'{self.nombre} {self.local} {self.direccion}'


# ---------------------------
# CARGOS Y EMPLEADOS
# ---------------------------

class Cargo(models.Model):
    nombre = models.CharField(max_length=50)
    Codigo_Cargo = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True , )
    fecha_modificacion = models.DateTimeField(auto_now=True , )
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "cargo"
        verbose_name = "cargo"
        verbose_name_plural = "cargos"

    def __str__(self):
        return f'{self.nombre} {self.Codigo_Cargo}'


class Empleado(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    cedula = models.CharField(max_length=12)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    correo = models.EmailField(max_length=40, default="@") 
    telefono = models.CharField(max_length=12) 
    fecha_creacion = models.DateTimeField(auto_now_add=True , )
    fecha_modificacion = models.DateTimeField(auto_now=True , )
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "empleado"
        verbose_name = "empleado"
        verbose_name_plural = "empleados"

    def __str__(self):
        return f'{self.nombre} {self.apellido} {self.cargo}'


# ---------------------------
# CLIENTES Y PROVEEDORES
# ---------------------------

class Cliente(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    cedula = models.CharField(max_length=12)
    correo = models.EmailField(max_length=40, default="@")
    telefono = models.CharField(max_length=12, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True , )
    fecha_modificacion = models.DateTimeField(auto_now=True , )
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "cliente"
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return f'{self.nombre} {self.cedula}'


class Proveedor(models.Model):
    nombre = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    producto = models.CharField(max_length=30)
    ruc= models.CharField(max_length=13, default="")
    telefono = models.CharField(max_length=12)
    correo = models.EmailField(max_length=40, default="@")
    direccion = models.CharField(max_length=200, blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True , )
    fecha_modificacion = models.DateTimeField(auto_now=True , )
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "proveedor"
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"

    def __str__(self):
        return self.nombre


# ---------------------------
# PRODUCTOS Y DESCUENTOS
# ---------------------------

class Producto(models.Model):
    nombre = models.CharField(max_length=20)
    modelo = models.CharField(max_length=40)
    color = models.CharField(max_length=20)
    numero_serie = models.CharField(max_length=20)
    categoria = models.CharField(max_length=20)
    unidad = models.CharField(max_length=255)
    precio = models.FloatField(default=0)

    fecha_creacion = models.DateTimeField(auto_now_add=True , )
    fecha_modificacion = models.DateTimeField(auto_now=True , )
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "producto"
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.nombre


class Descuento(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    descuento = models.FloatField(default=0)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_final = models.DateTimeField(default=timezone.now)

    fecha_creacion = models.DateTimeField(auto_now_add=True , )
    fecha_modificacion = models.DateTimeField(auto_now=True , )
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "descuento"
        verbose_name = "descuento"
        verbose_name_plural = "descuentos"

    def __str__(self):
        return f'{self.descuento} {self.fecha_inicio} {self.fecha_final}'




# ---------------------------
# COTIZACIÓN Y DETALLES
# ---------------------------

class Cotizacion(models.Model):
    cotizacion_codigo = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.RESTRICT)
    empleado = models.ForeignKey(Empleado, on_delete=models.RESTRICT, blank=True, null=True)

    comentario = models.TextField(blank=True, null=True)
    cantidad_productos = models.PositiveIntegerField(default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, blank=True, null=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)  # 1=Activa, 0=Anulada
    class Meta: 
        db_table = "cotizacion"
        verbose_name = "cotizacion"
        verbose_name_plural = "cotizaciones"
        ordering = ["fecha_creacion"]        

class Cotizacion_Detalle(models.Model):
    id = models.AutoField(primary_key=True)
    Cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    fecha_creacion = models.DateTimeField(auto_now_add=True , )
    fecha_modificacion = models.DateTimeField(auto_now=True , )
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)

    class Meta:
        db_table = "cotizacion_detalle"
        verbose_name = "cotizacion detalle"
        verbose_name_plural = "cotizacion detalles"
        ordering = ["fecha_creacion"]

# ---------------------------
# FACTURA Y DETALLES
# ---------------------------

class Factura(models.Model):
    factura_codigo = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.RESTRICT)
    empleado = models.ForeignKey(Empleado, on_delete=models.RESTRICT, blank=True, null=True)

    comentario = models.TextField(blank=True, null=True)
    cantidad_productos = models.PositiveIntegerField(default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, blank=True, null=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)  # 1=Activa, 0=Anulada

    class Meta:
        db_table = "factura"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Factura #{self.factura_codigo} - {self.cliente}"


class FacturaDetalle(models.Model):
    id = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(choices=[(1, 'Activo'), (0, 'Anulado')], default=1)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.factura.actualizar_totales()

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"


