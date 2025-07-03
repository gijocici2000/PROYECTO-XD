from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
import io
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.db import transaction
from decimal import Decimal
from .models import Factura
from .forms import FacturaForm, FacturaDetalleFormSet
from django.forms import inlineformset_factory


def index(request):
    return render(request, 'index.html', {})

def login(request):
    return render(request, 'login.html')
# ===================== CLIENTE =====================

def crear_cliente(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ClienteForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("consultar_cliente")
    else:
        form = ClienteForm()
    context = {"form_Cliente": form, "edit_mode": False}
    return render(request, "facturacion_cliente/cliente/crear_cliente.html", context)


def consultar_cliente(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if 'buscar_cliente' in request.POST:
            buscarClienteForm = BuscarClienteForm(request.POST)
            if buscarClienteForm.is_valid():
                nombre = buscarClienteForm.cleaned_data.get('nombre', '')
                apellido = buscarClienteForm.cleaned_data.get('apellido', '')
                cedula = buscarClienteForm.cleaned_data.get('cedula', '')
                fecha = buscarClienteForm.cleaned_data.get('fecha', None)

                clientes = Cliente.objects.filter(
                    Q(nombre__icontains=nombre) if nombre else Q(),
                    Q(apellido__icontains=apellido) if apellido else Q(),
                    Q(cedula__icontains=cedula) if cedula else Q(),
                    Q(fecha_creacion__lte=fecha) if fecha else Q(),
                )
                context = {'buscador_Cliente': buscarClienteForm, 'clientes': clientes}
                return render(request, "facturacion_cliente/cliente/consultar_cliente.html", context)

        
            return redirect("consultar_cliente")

    buscarClienteForm = BuscarClienteForm()
    clientes = None
    return render(request, "facturacion_cliente/cliente/consultar_cliente.html", {'buscador_Cliente': buscarClienteForm, 'clientes': clientes})


def modificar_cliente(request: HttpRequest, id: int) -> HttpResponse:
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == "POST":
        form = ClienteForm(data=request.POST, files=request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("consultar_cliente")
    else:
        form = ClienteForm(instance=cliente)
    context = {"form": form, "cliente": cliente, "edit_mode": True}
    return render(request, "facturacion_cliente/cliente/modificar_cliente.html", context)


def eliminar_cliente(request: HttpRequest, id: int) -> HttpResponse:
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == "POST":
        cliente.delete()
        return redirect("consultar_cliente")
    return render(request, "facturacion_cliente/cliente/eliminar_cliente.html", {"cliente": cliente})

# ===================== PRODUCTO =====================

def crear_producto(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("consultar_producto")
    else:
        form = ProductoForm()
    context = {"form_Producto": form, "edit_mode": False}
    return render(request, "facturacion_cliente/producto/crear_producto.html", context)


def consultar_producto(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if 'buscar_producto' in request.POST:
            buscarProductoForm = BuscarProductoForm(request.POST)
            if buscarProductoForm.is_valid():
                nombre = buscarProductoForm.cleaned_data['nombre']
                modelo = buscarProductoForm.cleaned_data['modelo']
                numero_serie = buscarProductoForm.cleaned_data['numero_serie']
                fecha = buscarProductoForm.cleaned_data['fecha']

                productos = Producto.objects.filter(
                    Q(nombre__icontains=nombre) if nombre else Q(),
                    Q(modelo__icontains=modelo) if modelo else Q(),
                    Q(numero_serie__icontains=numero_serie) if numero_serie else Q(),
                    Q(fecha_creacion__lte=fecha) if fecha else Q(),
                )
                context = {'buscador_Producto': buscarProductoForm, 'productos': productos}
                return render(request, "facturacion_cliente/producto/consultar_producto.html", context)

        elif 'exportar_producto' in request.POST:
            return exportar_pdf_producto(request)

    buscarProductoForm = BuscarProductoForm()
    productos = None
    return render(request, "facturacion_cliente/producto/consultar_producto.html", {'buscador_Producto': buscarProductoForm, 'productos': productos})


def exportar_pdf_producto(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="consultar_producto.pdf"'
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        rightMargin=inch / 4,
        leftMargin=inch / 4,
        topMargin=inch / 2,
        bottomMargin=inch / 4,
        pagesize=A4
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='RightAlign', alignment=TA_RIGHT))

    lista_producto = []
    header = Paragraph("Listado de productos", styles['Heading1'])
    lista_producto.append(header)

    buscarProductoForm = BuscarProductoForm(request.POST)
    if buscarProductoForm.is_valid():
        nombre = buscarProductoForm.cleaned_data['nombre']
        modelo = buscarProductoForm.cleaned_data['modelo']
        fecha = buscarProductoForm.cleaned_data['fecha']

        productos = Producto.objects.filter(
            Q(nombre__icontains=nombre) if nombre else Q(),
            Q(modelo__icontains=modelo) if modelo else Q(),
            Q(fecha_creacion__lte=fecha) if fecha else Q(),
        )
        headings = ('Id', 'Nombre', 'Modelo', 'Número de Serie', 'Categoría', 'Color', 'Unidad', 'Precio')
        allproductos = [( p.nombre, p.modelo, p.numero_serie, p.categoria, p.color, p.unidad, p.precio) for p in productos]

        t = Table([headings] + allproductos)
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.springgreen),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
            ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen),
        ]))
        lista_producto.append(t)

    doc.build(lista_producto)
    response.write(buffer.getvalue())
    buffer.close()
    return response


def modificar_producto(request: HttpRequest, id: int) -> HttpResponse:
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = ProductoForm(data=request.POST, files=request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("consultar_producto")
    else:
        form = ProductoForm(instance=producto)
    context = {"form": form, "producto": producto, "edit_mode": True}
    return render(request, "facturacion_cliente/producto/modificar_producto.html", context)



def eliminar_producto(request: HttpRequest, id: int) -> HttpResponse:
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.delete()
        return redirect("consultar_producto")
    return render(request, "facturacion_cliente/producto/eliminar_producto.html", {"producto": producto})

#############################################################################################################
# Funciones simples para renderizar templates sin lógica adicional

def crear_descuento(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DescuentoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("consultar_descuento")
    else:
        form = DescuentoForm()
    
    context = {"form": form, "edit_mode": False}  # Aquí debe ser "form", no "form_Descuento"
    return render(request, "facturacion_cliente/descuento/crear_descuento.html", context)


def consultar_descuento(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if 'buscar_descuento' in request.POST:
            buscarDescuentoForm = BuscarDescuentoForm(request.POST)
            if buscarDescuentoForm.is_valid():
                nombre = buscarDescuentoForm.cleaned_data.get('nombre', '')
                porcentaje = buscarDescuentoForm.cleaned_data.get('porcentaje', None)

                descuentos = Descuento.objects.filter(
                    Q(nombre__icontains=nombre) if nombre else Q(),
                    Q(porcentaje__gte=porcentaje) if porcentaje is not None else Q(),
                )
                context = {'buscador_Descuento': buscarDescuentoForm, 'descuentos': descuentos}
                return render(request, "facturacion_cliente/descuento/consultar_descuento.html", context)

        elif 'exportar_descuento' in request.POST:
            return exportar_pdf_descuento(request)
        
    buscarDescuentoForm = BuscarDescuentoForm()
    descuentos = None
    return render(request, "facturacion_cliente/descuento/consultar_descuento.html", {'buscador_Descuento': buscarDescuentoForm, 'descuentos': descuentos})

def exportar_pdf_descuento(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="consultar_descuento.pdf"'
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        rightMargin=inch / 4,
        leftMargin=inch / 4,
        topMargin=inch / 2,
        bottomMargin=inch / 4,
        pagesize=A4
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='RightAlign', alignment=TA_RIGHT))
    lista_descuento = []
    header = Paragraph("Listado de descuentos", styles['Heading1'])
    lista_descuento.append(header)
    buscarDescuentoForm = BuscarDescuentoForm(request.POST)
    if buscarDescuentoForm.is_valid():
        nombre = buscarDescuentoForm.cleaned_data.get('nombre', '')
        porcentaje = buscarDescuentoForm.cleaned_data.get('porcentaje', None)

        descuentos = Descuento.objects.filter(
            Q(nombre__icontains=nombre) if nombre else Q(),
            Q(porcentaje__gte=porcentaje) if porcentaje is not None else Q(),
        )
        headings = ('Id', 'Nombre', 'Porcentaje')
        alldescuentos = [(d.pk, getattr(d, 'nombre', ''), getattr(d, 'porcentaje', '')) for d in descuentos]

        t = Table([headings] + alldescuentos)
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.springgreen),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
            ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen),
        ]))
        lista_descuento.append(t)
    doc.build(lista_descuento)
    response.write(buffer.getvalue())
    buffer.close()
    return response

def modificar_descuento(request: HttpRequest, id: int) -> HttpResponse:
    descuento = get_object_or_404(Descuento, id=id)
    if request.method == "POST":
        form = DescuentoForm(request.POST, instance=descuento)
        if form.is_valid():
            form.save()
            return redirect("consultar_descuento")
    else:
        form = DescuentoForm(instance=descuento)
    context = {"form": form, "descuento": descuento, "edit_mode": True}
    return render(request, "facturacion_cliente/descuento/modificar_descuento.html", context)


def eliminar_descuento(request: HttpRequest, id: int) -> HttpResponse:
    descuento = get_object_or_404(Descuento, id=id)
    if request.method == "POST":
        descuento.delete()
        return redirect("consultar_descuento")
    return render(request, "facturacion_cliente/descuento/eliminar_descuento.html")



#############################################################################################################
# Funciones para manejar cotización

def crear_cotizacion(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CotizacionForm(request.POST)
        if form.is_valid():
            cotizacion = form.save(commit=False)
            cotizacion.creacion_usuario = request.user.username
            cotizacion.save()
            formset = CotizacionDetalleFormSet(request.POST)
            if formset.is_valid():
                for detalle_form in formset:
                    if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                        detalle = detalle_form.save(commit=False)
                        detalle.cotizacion = cotizacion
                        detalle.save()
                return redirect("consultar_cotizacion")
    return render(request, "facturacion_cliente/cotizacion/crear_cotizacion.html")



def consultar_cotizacion(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if 'buscar_cotizacion' in request.POST:
            buscarCotizacionForm = BuscarCotizacionForm(request.POST)
            if buscarCotizacionForm.is_valid():
                cliente = buscarCotizacionForm.cleaned_data.get('cliente', '')
                fecha = buscarCotizacionForm.cleaned_data.get('fecha', None)

                cotizaciones = Cotizacion.objects.filter(
                    Q(cliente__nombre__icontains=cliente) if cliente else Q(),
                    Q(fecha_creacion__lte=fecha) if fecha else Q(),
                )
                context = {'buscador_Cotizacion': buscarCotizacionForm, 'cotizaciones': cotizaciones}
                return render(request, "facturacion_cliente/cotizacion/consultar_cotizacion.html", context)

        elif 'exportar_cotizacion' in request.POST:
            return exportar_pdf_cotizacion(request)
    buscarCotizacionForm = BuscarCotizacionForm()
    cotizaciones = None
    return render(request, "facturacion_cliente/cotizacion/consultar_cotizacion.html", {'buscador_Cotizacion': buscarCotizacionForm, 'cotizaciones': cotizaciones})
def exportar_pdf_cotizacion(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="consultar_cotizacion.pdf"'
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        rightMargin=inch / 4,
        leftMargin=inch / 4,
        topMargin=inch / 2,
        bottomMargin=inch / 4,
        pagesize=A4
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='RightAlign', alignment=TA_RIGHT))

    lista_cotizacion = []
    header = Paragraph("Listado de cotizaciones", styles['Heading1'])
    lista_cotizacion.append(header)

    buscarCotizacionForm = BuscarCotizacionForm(request.POST)
    if buscarCotizacionForm.is_valid():
        cliente = buscarCotizacionForm.cleaned_data.get('cliente', '')
        fecha = buscarCotizacionForm.cleaned_data.get('fecha', None)

        cotizaciones = Cotizacion.objects.filter(
            Q(cliente__nombre__icontains=cliente) if cliente else Q(),
            Q(fecha_creacion__lte=fecha) if fecha else Q(),
        )
        headings = ('Id', 'Cliente', 'Fecha de Creación')
        allcotizaciones = [(c.pk, c.cliente.nombre, c.fecha_creacion.strftime('%Y-%m-%d')) for c in cotizaciones]

        t = Table([headings] + allcotizaciones)
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.springgreen),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
            ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen),
        ]))
        lista_cotizacion.append(t)

    doc.build(lista_cotizacion)
    response.write(buffer.getvalue())
    buffer.close()
    return response

def modificar_cotizacion(request: HttpRequest, id: int) -> HttpResponse:
    cotizacion = get_object_or_404(Cotizacion, id=id)
    if request.method == "POST":
        form = CotizacionForm(request.POST, instance=cotizacion)
        formset = CotizacionDetalleFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            cotizacion = form.save(commit=False)
            cotizacion.creacion_usuario = request.user.username
            cotizacion.save()
            for detalle_form in formset:
                if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                    detalle = detalle_form.save(commit=False)
                    detalle.cotizacion = cotizacion
                    detalle.save()
            return redirect("consultar_cotizacion")
    else:
        form = CotizacionForm(instance=cotizacion)
        formset = CotizacionDetalleFormSet()
    context = {"form": form, "formset": formset, "cotizacion": cotizacion, "edit_mode": True}
    return render(request, "facturacion_cliente/cotizacion/modificar_cotizacion.html")



def eliminar_cotizacion(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        cotizacion_id = request.POST.get('cotizacion_id')
        if cotizacion_id:
            cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
            cotizacion.delete()
            return redirect("consultar_cotizacion")
    return render(request, "facturacion_cliente/cotizacion/eliminar_cotizacion.html")



#############################################################################################################
# Funciones para manejar cotización detalle

def crear_cotizacion_detalle(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CotizacionDetalleForm(request.POST)
        if form.is_valid():
            cotizacion_detalle = form.save(commit=False)
            cotizacion_detalle.creacion_usuario = request.user.username
            cotizacion_detalle.save()
            return redirect("consultar_cotizacion_detalle")
    else:
        form = CotizacionDetalleForm()
    return render(request, "facturacion_cliente/cotizacion_detalle/crear_cotizacion_detalle.html")

def consultar_cotizacion_detalle(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if 'buscar_cotizacion_detalle' in request.POST:
            buscarCotizacionDetalleForm = BuscarCotizacionDetalleForm(request.POST)
            if buscarCotizacionDetalleForm.is_valid():
                cotizacion = buscarCotizacionDetalleForm.cleaned_data.get('cotizacion', '')
                fecha = buscarCotizacionDetalleForm.cleaned_data.get('fecha', None)

                cotizaciones_detalle = Cotizacion_Detalle.objects.filter(
                    Q(cotizacion__id=cotizacion) if cotizacion else Q(),
                    Q(fecha_creacion__lte=fecha) if fecha else Q(),
                )
                context = {'buscador_Cotizacion_Detalle': buscarCotizacionDetalleForm, 'cotizaciones_detalle': cotizaciones_detalle}
                return render(request, "facturacion_cliente/cotizacion_detalle/consultar_cotizacion_detalle.html", context)

    buscarCotizacionDetalleForm = BuscarCotizacionDetalleForm()
    cotizaciones_detalle = None
    return render(request, "facturacion_cliente/cotizacion_detalle/consultar_cotizacion_detalle.html", {'buscador_Cotizacion_Detalle': buscarCotizacionDetalleForm, 'cotizaciones_detalle': cotizaciones_detalle})

   


def eliminar_cotizacion_detalle(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        cotizacion_detalle_id = request.POST.get('cotizacion_detalle_id')
        if cotizacion_detalle_id:
            cotizacion_detalle = get_object_or_404(Cotizacion_Detalle, id=cotizacion_detalle_id)
            cotizacion_detalle.delete()
            return redirect("consultar_cotizacion_detalle")
    return render(request, "facturacion_cliente/cotizacion_detalle/eliminar_cotizacion_detalle.html")

def modificar_cotizacion_detalle(request: HttpRequest, id: int) -> HttpResponse:
    cotizacion_detalle = get_object_or_404(Cotizacion_Detalle, id=id)
    if request.method == "POST":
        form = CotizacionDetalleForm(request.POST, instance=cotizacion_detalle)
        if form.is_valid():
            cotizacion_detalle = form.save(commit=False)
            cotizacion_detalle.modificacion_usuario = request.user.username
            cotizacion_detalle.save()
            return redirect("consultar_cotizacion_detalle")
    else:
        form = CotizacionDetalleForm(instance=cotizacion_detalle)
    return render(request, "cotizacion_detalle/modificar_cotizacion_detalle.html")


######################################## Facturación Cliente ########################################


def crear_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        formset = FacturaDetalleFormSet(request.POST, queryset=Factura_Detalle.objects.none())

        if form.is_valid() and formset.is_valid():
            factura = form.save(commit=False)
            factura.creacion_usuario = request.user.username
            factura.fecha_emision = timezone.now()
            factura.subtotal = Decimal('0.00')
            factura.descuento_total = Decimal('0.00')
            factura.total = Decimal('0.00')
            factura.cantidad_productos = 0
            factura.save()

            subtotal_general = Decimal('0.00')
            total_descuento = Decimal('0.00')
            cantidad_productos = 0

            for detalle_form in formset:
                if detalle_form.cleaned_data:
                    producto = detalle_form.cleaned_data['producto']
                    cantidad = detalle_form.cleaned_data['cantidad']

                    precio_unitario = Decimal(producto.precio)
                    descuento_unitario = precio_unitario * Decimal('0.10')
                    precio_final = precio_unitario - descuento_unitario

                    subtotal = precio_final * cantidad

                    Factura_Detalle.objects.create(
                        factura=factura,
                        producto=producto,
                        cantidad=cantidad,
                        subtotal=subtotal,
                        creacion_usuario=request.user.username
                    )

                    subtotal_general += precio_unitario * cantidad
                    total_descuento += descuento_unitario * cantidad
                    cantidad_productos += cantidad

            iva = (subtotal_general - total_descuento) * Decimal('0.12')
            total_final = (subtotal_general - total_descuento) + iva

            factura.subtotal = subtotal_general
            factura.descuento_total = total_descuento
            factura.iva = iva
            factura.total = total_final
            factura.cantidad_productos = cantidad_productos
            factura.save()

            return redirect('ver_factura', factura_id=factura.factura_codigo)

    else:
        form = FacturaForm()
        formset = FacturaDetalleFormSet(queryset=Factura_Detalle.objects.none())

    productos = Producto.objects.all()

    return render(request, 'facturacion_cliente/factura/crear_factura.html', {
        'form': form,
        'formset': formset,
        'productos': productos
    })

def consultar_factura(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if 'buscar_factura' in request.POST:
            buscarFacturaForm = BuscarFacturaForm(request.POST)
            if buscarFacturaForm.is_valid():
                cedula = buscarFacturaForm.cleaned_data.get('cliente_cedula', '')
                desde = buscarFacturaForm.cleaned_data.get('desde')
                hasta = buscarFacturaForm.cleaned_data.get('hasta')

                facturas = Factura.objects.filter(
                    Q(cliente__cedula__icontains=cedula) if cedula else Q(),
                    Q(fecha_creacion__range=(desde, hasta)) if desde and hasta else Q(),
                    Q(fecha_creacion__gte=desde) if desde else Q(),
                    Q(fecha_creacion__lte=hasta) if hasta else Q(),
                )
                context = {'buscador_factura': buscarFacturaForm, 'facturas': facturas}
                return render(request, "facturacion_cliente/factura/consultar_factura.html", context)

        elif 'exportar_factura' in request.POST:
            return exportar_pdf_factura(request)

    buscarFacturaForm = BuscarFacturaForm()
    facturas = None
    return render(request, "facturacion_cliente/factura/consultar_factura.html", {'buscador_factura': buscarFacturaForm, 'facturas': facturas})    

def modificar_factura(request: HttpRequest, id: int) -> HttpResponse:
    factura = get_object_or_404(Factura, factura_codigo=id)
    facturaForm = FacturaForm(request.POST or None, instance=factura)
    if request.method == "POST" and facturaForm.is_valid():
        facturaForm.save()
        return redirect('consultar_factura')
    return render(request, "facturacion_cliente/factura/modificar_factura.html", {'facturaform': facturaForm})

def eliminar_factura(request, id):
    factura = get_object_or_404(Factura, factura_codigo=id)
    if request.method == "POST":
        factura.estado = 0
        factura.save()
        return redirect('consultar_factura')

    return render(request, "facturacion_cliente/factura/eliminar_factura.html", {"factura": factura})


def exportar_pdf_factura(request):
    """
    Exporta a PDF el listado de facturas filtradas por cédula de cliente y rango de fechas.
    """
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="consultar_facturas.pdf"'
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        rightMargin=inch / 4,
        leftMargin=inch / 4,
        topMargin=inch / 2,
        bottomMargin=inch / 4,
        pagesize=A4
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='RightAlign', alignment=TA_RIGHT))
    lista_facturas = []
    header = Paragraph("Listado de Facturas", styles['Heading1'])
    lista_facturas.append(header)
    buscarFacturaForm = BuscarFacturaForm(request.POST or None)
    if buscarFacturaForm.is_valid():
        cedula = buscarFacturaForm.cleaned_data.get('cliente_cedula', '')
        desde = buscarFacturaForm.cleaned_data.get('desde')
        hasta = buscarFacturaForm.cleaned_data.get('hasta')
        filtros = Q()
        if cedula:
            filtros &= Q(cliente__cedula__icontains=cedula)
        if desde and hasta:
            filtros &= Q(fecha_creacion__range=(desde, hasta))
        elif desde:
            filtros &= Q(fecha_creacion__gte=desde)
        elif hasta:
            filtros &= Q(fecha_creacion__lte=hasta)
        facturas = Factura.objects.filter(filtros)
        headings = ('Fecha', 'Cliente', 'Cod Factura', 'Total')
        allfacturas = [
            (f.fecha_creacion.strftime('%Y-%m-%d'), str(f.cliente), f.factura_codigo, f.total)
            for f in facturas
        ]
        t = Table([headings] + allfacturas)
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.springgreen),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
            ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
        ]))
        lista_facturas.append(t)
    doc.build(lista_facturas)
    response.write(buffer.getvalue())
    buffer.close()
    return response


#############################################################################################################

#############################################################################################################


# ===================== PROVEEDOR =====================
def crear_proveedor(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProveedorForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("consultar_proveedor")
    else:
        form = ProveedorForm()
    context = {"form_Proveedor": form, "edit_mode": False}
    return render(request, "administrativo/proveedor/crear_proveedor.html", context)

def consultar_proveedor(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if 'buscar_proveedor' in request.POST:
            buscarProveedorForm = BuscarProveedorForm(request.POST)
            if buscarProveedorForm.is_valid():
                nombre = buscarProveedorForm.cleaned_data.get('nombre', '')
                ruc = buscarProveedorForm.cleaned_data.get('ruc', '')
                fecha = buscarProveedorForm.cleaned_data.get('fecha', None)

                proveedores = Proveedor.objects.filter(
                    Q(nombre__icontains=nombre) if nombre else Q(),
                    Q(ruc__icontains=ruc) if ruc else Q(),
                    Q(fecha_creacion__lte=fecha) if fecha else Q(),
                )
                context = {'buscador_Proveedor': buscarProveedorForm, 'proveedores': proveedores}
                return render(request, "administrativo/proveedor/consultar_proveedor.html", context)

        elif 'exportar_proveedor' in request.POST:
            return exportar_pdf_proveedor(request)
        
    buscarProveedorForm = BuscarProveedorForm()
    proveedores = None
    return render(request, "administrativo/proveedor/consultar_proveedor.html", {'buscador_Proveedor': buscarProveedorForm, 'proveedores': proveedores})


        
def exportar_pdf_proveedor(request: HttpRequest) -> HttpResponse:
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="consultar_proveedor.pdf"'
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            rightMargin=inch / 4,
            leftMargin=inch / 4,
            topMargin=inch / 2,
            bottomMargin=inch / 4,
            pagesize=A4
        )
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', alignment=TA_RIGHT))

        lista_proveedor = []
        header = Paragraph("Listado de Proveedores", styles['Heading1'])
        lista_proveedor.append(header)

        buscarProveedorForm = BuscarProveedorForm(request.POST)
        if buscarProveedorForm.is_valid():
            nombre = buscarProveedorForm.cleaned_data.get('nombre', '')
            ruc = buscarProveedorForm.cleaned_data.get('ruc', '')
            fecha = buscarProveedorForm.cleaned_data.get('fecha', None)

            proveedores = Proveedor.objects.filter(
                Q(nombre__icontains=nombre) if nombre else Q(),
                Q(ruc__icontains=ruc) if ruc else Q(),
                Q(fecha_creacion__lte=fecha) if fecha else Q(),
            )
            headings = ('Id', 'Nombre', 'RUC', 'Teléfono', 'Correo')
            allproveedores = [(p.pk, p.nombre, p.ruc, p.telefono, p.correo) for p in proveedores]

            t = Table([headings] + allproveedores)
            t.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.springgreen),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen),
            ]))
            lista_proveedor.append(t)

        doc.build(lista_proveedor)
        response.write(buffer.getvalue())
        buffer.close()
        return response

   

def modificar_proveedor(request: HttpRequest, id: int) -> HttpResponse:
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == "POST":
        form = ProveedorForm(data=request.POST, files=request.FILES, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect("consultar_proveedor")
    else:
        form = ProveedorForm(instance=proveedor)
    context = {"form": form, "proveedor": proveedor, "edit_mode": True}
    return render(request, "administrativo/proveedor/modificar_proveedor.html", context)


def eliminar_proveedor(request: HttpRequest, id: int) -> HttpResponse:
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == "POST":
        proveedor.delete()
        return redirect("consultar_proveedor")
    return render(request, "administrativo/proveedor/eliminar_proveedor.html", {"proveedor": proveedor})




##############################################################################################################
##############################################################################################################
#############################################################################################################
###############################################################################################################
#############################################################################################################





# EMPLEADO
def crear_empleado(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.creacion_usuario = request.user.username
            empleado.save()
            return redirect("consultar_empleado")
    else:
        form = EmpleadoForm()
    return render(request, "empleado/crear_empleado.html", {"form": form, "edit_mode": False})
   
   
def modificar_empleado(request: HttpRequest, id: int) -> HttpResponse:
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == "POST":
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.modificacion_usuario = request.user.username
            empleado.save()
            return redirect("consultar_empleado")
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, "empleado/modificar_empleado.html", {"form": form, "empleado": empleado, "edit_mode": True})

def consultar_empleado(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if 'buscar_empleado' in request.POST:
            buscarEmpleadoForm = BuscarEmpleadoForm(request.POST)
            if buscarEmpleadoForm.is_valid():
                nombre = buscarEmpleadoForm.cleaned_data.get('nombre', '')
                apellido = buscarEmpleadoForm.cleaned_data.get('apellido', '')
                cedula = buscarEmpleadoForm.cleaned_data.get('cedula', '')
                fecha = buscarEmpleadoForm.cleaned_data.get('fecha', None)

                empleados = Empleado.objects.filter(
                    Q(nombre__icontains=nombre) if nombre else Q(),
                    Q(apellido__icontains=apellido) if apellido else Q(),
                    Q(cedula__icontains=cedula) if cedula else Q(),
                    Q(fecha_creacion__lte=fecha) if fecha else Q(),
                )
                context = {'buscador_Empleado': buscarEmpleadoForm, 'empleados': empleados}
                return render(request, "empleado/consultar_empleado.html", context)

    buscarEmpleadoForm = BuscarEmpleadoForm()
    empleados = None
    return render(request, "empleado/consultar_empleado.html", {'buscador_Empleado': buscarEmpleadoForm, 'empleados': empleados})

def eliminar_empleado(request: HttpRequest, id: int) -> HttpResponse:
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == "POST":
        empleado.delete()
        return redirect("consultar_empleado")
    return render(request, "empleado/eliminar_empleado.html", {"empleado": empleado})
#############################################################################################################