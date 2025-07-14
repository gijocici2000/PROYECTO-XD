from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.db.models import Max, Sum, F
from django.contrib.auth.models import User


# ---------------------------administracion 
# SUCURSAL
# ---------------------------



class Sucursal(models.Model):
    nombre = models.CharField(max_length=30)
    ruc= models.CharField(max_length=13, default="",)
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
    Codigo_Cargo = models.CharField(max_length=50, unique=True)
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
    cedula = models.CharField(max_length=12, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT) 
    correo = models.EmailField(max_length=40, default="@" ,unique=True ) 
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
        username = self.user.username if self.user else "Sin usuario"
        return f"{username} - {self.cargo.nombre}"

# ---------------------------
# CLIENTES Y PROVEEDORES
# ---------------------------

class Cliente(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    cedula = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(max_length=40, default="@", unique=True)  
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
    ruc= models.CharField(max_length=13, default="",)
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
        return self.nombre\
        

# ---------------------------
# BODEGA
class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.nombre

# ---------------------------
# PRODUCTOS Y DESCUENTOS
# ---------------------------

class Producto(models.Model):
    numero_serie = models.CharField(max_length=100, unique=True,)
    lote = models.CharField(max_length=50)  # Nuevo campo
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    categoria = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default= Decimal('0.00'))  # Más seguro que Float
    stock = models.PositiveIntegerField( ) 
    
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    
    ESTADO_CHOICES = [
        (1, 'Activo'),
        (0, 'Inactivo'),
    ]
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=1)

    class Meta:
        db_table = "producto"
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return f"{self.nombre} - {self.numero_serie}"
    def precio_con_descuento(self):
        ahora = timezone.now()
        descuento_activo = Descuento.objects.filter(
            producto=self,
            estado=1,
            fecha_inicio__lte=ahora,
            fecha_final__gte=ahora
        ).order_by('-fecha_inicio').first()
        
        if descuento_activo and descuento_activo.descuento > 0:
            descuento_decimal = Decimal(descuento_activo.descuento) / Decimal('100')
            return (self.precio * (Decimal('1') - descuento_decimal)).quantize(Decimal('0.01'))
        return self.precio   

class HistorialProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=[('creación', 'Creación'), ('actualización', 'Actualización')])
    stock_anterior = models.PositiveIntegerField()
    cantidad_cambiada = models.IntegerField()  # Puede ser negativo
    stock_nuevo = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historial_producto'
        verbose_name = 'historial producto'
        verbose_name_plural = 'historial productos'

    def __str__(self):
        return f"{self.producto.nombre} ({self.tipo}) - {self.fecha.strftime('%Y-%m-%d %H:%M')}"

# ---------------------------
# DESCUENTOS
       

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


#iva###
class Iva(models.Model):
    nombre = models.CharField(max_length=50,default='iva', null=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2 ,null=False)  # Ejemplo: 12.00

    
    class Meta:
        db_table = "iva"
        verbose_name = "iva"
        verbose_name_plural = "ivas"

# ---------------------------
# COTIZACIÓN Y DETALLES
# ---------------------------
class Cotizacion(models.Model):
    id = models.AutoField(primary_key=True)
    numero_cotizacion = models.CharField(max_length=20, unique=True, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    empleado = models.ForeignKey(Empleado, on_delete=models.RESTRICT, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.RESTRICT)
    
    fecha_emision = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True)
    creacion_usuario = models.CharField(max_length=150)
    modificacion_usuario = models.CharField(max_length=150)

    def __str__(self):
        return f"Cotización {self.id} para {self.cliente.nombre}"

    def get_totales(self):
        detalles = self.detalles.all()  # type: ignore # Usamos related_name 'detalles'
        subtotal = Decimal('0.00')
        iva_total = Decimal('0.00')
        for d in detalles:
            subtotal += d.precio_cotizado * d.cantidad_producto
            if d.iva:
                iva_total += (d.precio_cotizado * d.cantidad_producto) * (d.iva.porcentaje / Decimal('100'))
        total = subtotal + iva_total
        return {
            'subtotal': subtotal.quantize(Decimal('0.01')),
            'iva_total': iva_total.quantize(Decimal('0.01')),
            'total': total.quantize(Decimal('0.01'))
        }

class Cotizacion_Detalle(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad_producto = models.IntegerField()
    precio_cotizado = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_total = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    iva = models.ForeignKey(Iva, on_delete=models.SET_NULL, null=True, blank=True)
    creacion_usuario = models.CharField(max_length=150)
    modificacion_usuario = models.CharField(max_length=150)
   

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad_producto}"
    

# ---------------------------
# FACTURA Y DETALLES
# ---------------------------

class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    numero_factura = models.CharField(max_length=20, unique=True, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.RESTRICT)
    empleado = models.ForeignKey(Empleado, on_delete=models.RESTRICT, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    tipo_pago = models.CharField(max_length=20, choices=[
        ('contado', 'Contado'),
        ('credito', 'Crédito'),
        ('transferencia', 'Transferencia Bancaria'), 
    ], default='contado')

    fecha_emision = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)  # 1=Activa, 0=Anulada

    class Meta:
        db_table = "factura"
        ordering = ["-fecha_creacion"]
  
    def __str__(self):
        return f"Factura {self.numero_factura or self.id} - {self.cliente}"

    def save(self, *args, **kwargs):
        if not self.numero_factura:
            max_id = Factura.objects.aggregate(max_id=Max('id'))['max_id'] or 0
            siguiente = max_id + 1
            self.numero_factura = f"F-{timezone.now().year}-{siguiente:05d}"
        super().save(*args, **kwargs)

   
    @property
    def get_totales(self):
        detalles = self.detalles.filter(estado=1) # type: ignore
        subtotal = detalles.aggregate(suma=Sum('subtotal'))['suma'] or Decimal('0.00')
        iva_total = sum(d.iva_total for d in detalles)
        total = subtotal + iva_total
        return {
            'subtotal': subtotal,
            'iva_total': iva_total,
            'total': total
        }
    


class Factura_Detalle(models.Model):
    id = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad_producto = models.PositiveIntegerField(default=1)
    precio_factura = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Precio congelado
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    descuento_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    iva = models.ForeignKey(Iva, on_delete=models.RESTRICT)
    total_factura_valor = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.00'))

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creacion_usuario = models.CharField(max_length=50)
    modificacion_usuario = models.CharField(max_length=50)
    estado = models.IntegerField(choices=[(1, 'Activo'), (0, 'Anulado')], default=1)

    class Meta:
        db_table = "factura_detalle"
        verbose_name = "Detalle de Factura"
        verbose_name_plural = "Detalles de Factura"

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_producto} unidades"
    

    @property
    def subtotal_calculado(self):
        return Decimal(str(self.precio_factura)) * self.cantidad_producto

    @property
    def iva_total(self):
        return Decimal(str(self.subtotal)) * Decimal(str(self.iva.porcentaje)) / 100

    @property
    def total_calculado(self):
        return Decimal(str(self.subtotal)) + self.iva_total

    def save(self, *args, **kwargs):
        # Actualiza subtotal y total antes de guardar
        self.subtotal = self.subtotal_calculado
        self.total_factura_valor = self.total_calculado
        super().save(*args, **kwargs)




# ---------------------------pagos
# class Pago(models.Model):
#     factura = models.OneToOneField('Factura', on_delete=models.CASCADE)
#     metodo = models.CharField(max_length=50, choices=[
#         ('efectivo', 'Efectivo'),
#         ('tarjeta', 'Tarjeta'),
#     ])
#     estado = models.CharField(max_length=20, choices=[
#         ('pendiente', 'Pendiente'),
#         ('pagado', 'Pagado'),
#         ('fallido', 'Fallido'),
#     ], default='pendiente')
#     transaccion_id = models.CharField(max_length=100, blank=True, null=True)
#     monto = models.DecimalField(max_digits=10, decimal_places=2)
#     fecha_pago = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.metodo} - {self.estado} - ${self.monto}"
