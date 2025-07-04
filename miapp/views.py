import io
import json
from decimal import Decimal
from django.db import transaction
from django.db.models import Q, Sum
from django.forms import inlineformset_factory
from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.pdfgen import canvas
from django.shortcuts import redirect



from .models import *
from .forms import *





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



def consultar_cotizacion(request):
    cotizaciones = None
    buscar_form = BuscarCotizacionForm()  # Debes crear este formulario similar a BuscarFacturaForm

    if request.method == "POST":
        if 'buscar_cotizacion' in request.POST:
            buscar_form = BuscarCotizacionForm(request.POST)
            if buscar_form.is_valid():
                cedula = buscar_form.cleaned_data.get('cliente_cedula')
                desde = buscar_form.cleaned_data.get('desde')
                hasta = buscar_form.cleaned_data.get('hasta')

                filtros = Q()
                if cedula:
                    filtros &= Q(cliente__cedula__icontains=cedula)
                if desde and hasta:
                    filtros &= Q(fecha_creacion__range=(desde, hasta))
                elif desde:
                    filtros &= Q(fecha_creacion__gte=desde)
                elif hasta:
                    filtros &= Q(fecha_creacion__lte=hasta)

                cotizaciones = Cotizacion.objects.filter(filtros).order_by('-fecha_creacion')

        elif 'exportar_cotizacion' in request.POST:
            return exportar_pdf_cotizacion(request)

    context = {
        'buscador_cotizacion': buscar_form,
        'cotizaciones': cotizaciones
    }
    return render(request, "cotizacion/consultar_cotizacion.html", context)


def exportar_pdf_cotizacion(request):
    cotizacion_id = request.POST.get('cotizacion_id')

    if not cotizacion_id:
        return HttpResponse("ID de cotización no proporcionado.", status=400)

    try:
        cotizacion = Cotizacion.objects.get(pk=cotizacion_id)
    except Cotizacion.DoesNotExist:
        return HttpResponse("Cotización no encontrada.", status=404)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "COTIZACIÓN")

    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Número: {cotizacion.numero_cotizacion}")
    p.drawString(50, height - 85, f"Cliente: {cotizacion.cliente}")
    p.drawString(50, height - 100, f"Sucursal: {cotizacion.sucursal}")
    p.drawString(50, height - 115, f"Fecha Emisión: {cotizacion.fecha_emision.strftime('%d/%m/%Y %H:%M')}")

    # Línea separadora
    p.line(50, height - 130, width - 50, height - 130)

    # Tabla de productos (detalles)
    detalles = cotizacion.detalles.all()  # related_name en el modelo CotizacionDetalle

    data = [["Producto", "Cantidad", "Precio Unitario", "Subtotal", "IVA", "Total"]]

    for d in detalles:
        data.append([
            str(d.producto),
            str(d.cantidad),
            f"{d.precio_cotizacion:.2f}",
            f"{d.subtotal:.2f}",
            f"{d.iva_total:.2f}",
            f"{d.total_calculado:.2f}",
        ])

    # Totales generales
    subtotal_general = sum(d.subtotal for d in detalles)
    iva_general = sum(d.iva_total for d in detalles)
    total_general = sum(d.total_calculado for d in detalles)

    table = Table(data, colWidths=[120, 60, 80, 80, 60, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    table.wrapOn(p, width, height)
    table_height = 200
    table.drawOn(p, 50, height - 150 - table_height)

    # Totales
    y = height - 150 - table_height - 30
    p.setFont("Helvetica-Bold", 10)
    p.drawString(400, y, f"Subtotal: {subtotal_general:.2f}")
    p.drawString(400, y - 15, f"IVA Total: {iva_general:.2f}")
    p.drawString(400, y - 30, f"TOTAL: {total_general:.2f}")

    # Footer
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(50, 30, "Gracias por cotizar con nosotros.")

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'Cotizacion_{cotizacion.numero_cotizacion}.pdf')




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


def consultar_cotizacion_detalle(request):
    detalles = None
    buscar_form = BuscarCotizacionDetalleForm()

    if request.method == "POST":
        if 'buscar_cotizacion_detalle' in request.POST:
            buscar_form = BuscarCotizacionDetalleForm(request.POST)
            if buscar_form.is_valid():
                producto_nombre = buscar_form.cleaned_data.get('producto_nombre')
                cotizacion_numero = buscar_form.cleaned_data.get('cotizacion_numero')
                desde = buscar_form.cleaned_data.get('desde')
                hasta = buscar_form.cleaned_data.get('hasta')

                filtros = Q()
                if producto_nombre:
                    filtros &= Q(producto__nombre__icontains=producto_nombre)
                if cotizacion_numero:
                    filtros &= Q(cotizacion__numero_cotizacion__icontains=cotizacion_numero)
                if desde and hasta:
                    filtros &= Q(fecha_creacion__range=(desde, hasta))
                elif desde:
                    filtros &= Q(fecha_creacion__gte=desde)
                elif hasta:
                    filtros &= Q(fecha_creacion__lte=hasta)

                detalles = Cotizacion_Detalle.objects.filter(filtros).order_by('-fecha_creacion')

    context = {
        'buscador_detalle': buscar_form,
        'detalles': detalles
    }
    return render(request, "facturacion_cliente/cotizacion_detalle/consultar_cotizacion_detalle.html", context)

def eliminar_cotizacion_detalle(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        cotizacion_detalle_id = request.POST.get('cotizacion_detalle_id')
        if cotizacion_detalle_id:
            cotizacion_detalle = get_object_or_404(Cotizacion_Detalle, id=cotizacion_detalle_id)
            cotizacion_detalle.delete()
            messages.success(request, "Detalle de cotización eliminado correctamente.")
            # Aquí redirige a la vista que muestra los detalles de la cotización relacionada
            return redirect("consultar_cotizacion_detalle")  
        else:
            messages.error(request, "No se proporcionó el ID del detalle.")
            return redirect("consultar_cotizacion_detalle")

    # Si no es POST, puedes mostrar una confirmación o redirigir
    return render(request, "facturacion_cliente/cotizacion_detalle/eliminar_cotizacion_detalle.html")

def modificar_cotizacion_detalle(request: HttpRequest, id: int) -> HttpResponse:
    cotizacion_detalle = get_object_or_404(Cotizacion_Detalle, id=id)
    
    if request.method == "POST":
        form = CotizacionDetalleForm(request.POST, instance=cotizacion_detalle)
        if form.is_valid():
            detalle_modificado = form.save(commit=False)
            detalle_modificado.modificacion_usuario = request.user.username
            detalle_modificado.save()
            messages.success(request, "Detalle de cotización modificado correctamente.")
            return redirect("consultar_cotizacion_detalle")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CotizacionDetalleForm(instance=cotizacion_detalle)
    
    return render(request, "facturacion_cliente/cotizacion_detalle/modificar_cotizacion_detalle.html", {
        'form': form,
        'cotizacion_detalle': cotizacion_detalle,
    })




######################################## Facturación Cliente ########################################


from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.db import transaction
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from decimal import Decimal
import io
import json

# Tus imports y modelos aquí (Factura, Producto, Iva, Factura_Detalle, etc.)

def crear_factura(request):
    productos = Producto.objects.filter(estado=1)
    ivas = Iva.objects.all()

    if request.method == 'POST':
        form = FacturaForm(request.POST)
        productos_json = request.POST.get('productos_json')

        if form.is_valid() and productos_json:
            factura = form.save(commit=False)
            factura.creacion_usuario = request.user.username
            factura.modificacion_usuario = request.user.username
            factura.save()

            productos_data = json.loads(productos_json)

            for item in productos_data:
                producto = Producto.objects.get(id=item['id'])
                iva_obj = Iva.objects.get(id=item['iva_id'])

                detalle = Factura_Detalle(
                    factura=factura,
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio_factura=Decimal(item['precio']),
                    subtotal=Decimal(item['subtotal']),
                    descuento_total=Decimal(item['descuento']),
                    iva=iva_obj,
                    total_factura_valor=Decimal(item['total']),
                    creacion_usuario=request.user.username,
                    modificacion_usuario=request.user.username
                )
                detalle.save()

            messages.success(request, "Factura creada correctamente.")
            return redirect('consultar_factura')  # Aquí usas el nombre de la URL

        else:
            messages.error(request, "Verifica los datos del formulario.")

    else:
        form = FacturaForm()

    return render(request, 'facturacion_cliente/factura/crear_factura.html', {
        'form': form,
        'productos': productos,
        'ivas': ivas,
    })


def crear_factura_detalle(request):
    if request.method == 'POST':
        factura_form = FacturaForm(request.POST)
        detalle_formset = FacturaDetalleFormSet(request.POST)
        if factura_form.is_valid() and detalle_formset.is_valid():
            with transaction.atomic():
                factura = factura_form.save()
                detalles = detalle_formset.save(commit=False)
                for detalle in detalles:
                    detalle.factura = factura
                    detalle.save()
            return redirect('consultar_factura')  # Cambiado a nombre de URL
    else:
        factura_form = FacturaForm()
        detalle_formset = FacturaDetalleFormSet()

    context = {
        'factura_form': factura_form,
        'detalle_formset': detalle_formset,
    }
    return render(request, "facturacion_cliente/factura/consultar_factura.html", context)


def consultar_factura(request):
    facturas = None
    buscar_form = BuscarFacturaForm(request.POST or None)
    filtros = Q()

    if request.method == "POST":
        if 'buscar_factura' in request.POST and buscar_form.is_valid():
            cedula = buscar_form.cleaned_data.get('cliente_cedula')
            desde = buscar_form.cleaned_data.get('desde')
            hasta = buscar_form.cleaned_data.get('hasta')

            if cedula:
                filtros &= Q(cliente__cedula__icontains=cedula)
            if desde and hasta:
                filtros &= Q(fecha_creacion__range=(desde, hasta))
            elif desde:
                filtros &= Q(fecha_creacion__gte=desde)
            elif hasta:
                filtros &= Q(fecha_creacion__lte=hasta)

            facturas = Factura.objects.filter(filtros).order_by('-fecha_creacion')

            # Calcular total para cada factura
            for f in facturas:
                total = f.detalles.aggregate(total=Sum('total_factura_valor'))['total'] or 0
                f.total_calculado = total

        elif 'exportar_factura' in request.POST:
            return exportar_pdf_factura(request)

    context = {
        'buscador_factura': buscar_form,
        'facturas': facturas,
    }
    return render(request, "facturacion_cliente/factura/consultar_factura.html", context)


def exportar_pdf_factura(request):
    
    factura_id = request.GET.get('factura_id') or request.POST.get('factura_id')
    
    if not factura_id:
        return HttpResponse("ID de factura no proporcionado.", status=400)
    try:
        factura = Factura.objects.get(pk=factura_id)
    except Factura.DoesNotExist:
        return HttpResponse("Factura no encontrada.", status=404)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "FACTURA ELECTRÓNICA")

    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Número: {factura.numero_factura}")
    p.drawString(50, height - 85, f"Cliente: {factura.cliente}")
    p.drawString(50, height - 100, f"Sucursal: {factura.sucursal}")
    p.drawString(50, height - 115, f"Fecha Emisión: {factura.fecha_emision.strftime('%d/%m/%Y %H:%M')}")

    # Línea separadora
    p.line(50, height - 130, width - 50, height - 130)

    # Tabla de Productos
    detalles = factura.detalles.all()

    data = [["Producto", "Cantidad", "Precio Unitario", "Subtotal", "IVA", "Total"]]

    for d in detalles:
        data.append([
            str(d.producto),
            str(d.cantidad),
            f"{d.precio_factura:.2f}",
            f"{d.subtotal:.2f}",
            f"{d.iva_total:.2f}",
            f"{d.total_calculado:.2f}",
        ])

    # Calcular Totales
    subtotal_general = sum(d.subtotal for d in detalles)
    iva_general = sum(d.iva_total for d in detalles)
    total_general = sum(d.total_calculado for d in detalles)

    table = Table(data, colWidths=[120, 60, 80, 80, 60, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    table.wrapOn(p, width, height)
    table_height = 200
    table.drawOn(p, 50, height - 150 - table_height)

    # Totales
    y = height - 150 - table_height - 30
    p.setFont("Helvetica-Bold", 10)
    p.drawString(400, y, f"Subtotal: {subtotal_general:.2f}")
    p.drawString(400, y - 15, f"IVA Total: {iva_general:.2f}")
    p.drawString(400, y - 30, f"TOTAL: {total_general:.2f}")

    # Footer
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(50, 30, "Gracias por su compra.")

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'Factura_{factura.numero_factura}.pdf')


def modificar_factura(request, id):
    factura = get_object_or_404(Factura, factura_codigo=id)
    if request.method == "POST":
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            factura_modificada = form.save(commit=False)
            factura_modificada.modificacion_usuario = request.user.username
            factura_modificada.save()
            messages.success(request, "Factura modificada correctamente.")
            return redirect('consultar_factura')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = FacturaForm(instance=factura)

    context = {
        'form': form,
        'factura': factura,
    }
    return render(request, "facturacion_cliente/factura/modificar_factura.html", context)


def eliminar_factura(request, id):
    factura = get_object_or_404(Factura, factura_codigo=id)
    if request.method == "POST":
        factura.estado = 0  # Marcar como anulado
        factura.save()
        messages.success(request, "Factura anulada correctamente.")
        return redirect('consultar_factura')

    context = {
        'factura': factura,
    }
    return render(request, "facturacion_cliente/factura/eliminar_factura.html", context)



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