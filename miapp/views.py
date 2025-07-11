import datetime
import io
import json
from decimal import Decimal
import os
from typing import Optional
from django.db import transaction
from django.db.models import Q, Sum
from django.forms import formset_factory, inlineformset_factory
from django.http import HttpRequest, HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.pdfgen import canvas
from django.utils.safestring import mark_safe
from .models import *
from .forms import *
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


#################################login y registro de usuarios##########################################


def index(request):
    cargos_permitidos = ['admin', 'gerente']
    return render(request, 'index.html',{'cargos_permitidos': cargos_permitidos})

def cargo_requerido(nombre_cargos):
    def decorador(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            try:
                empleado = Empleado.objects.get(user=request.user)
                if empleado.cargo.nombre.lower() in [c.lower() for c in nombre_cargos]:
                    return view_func(request, *args, **kwargs)
            except Empleado.DoesNotExist:
                pass

            return redirect('no_autorizado')
        return wrapper
    return decorador


@login_required
@cargo_requerido(['admin', 'gerente'])
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro_usuario/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # O donde quieras después del login
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'registro_usuario/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')
def no_autorizado(request):
    return render(request, 'registro_usuario/no_autorizado.html', {"mensaje": "No tienes permiso para acceder aquí."})

######################################### EMPLEADO ########################################

@login_required
@cargo_requerido(['admin', 'Gerente'])
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
 
@login_required
@cargo_requerido(['admin', 'Gerente'])   
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
@login_required
@cargo_requerido(['admin', 'Gerente'])
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
@login_required
@cargo_requerido(['admin', 'Gerente'])
def eliminar_empleado(request: HttpRequest, id: int) -> HttpResponse:
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == "POST":
        empleado.delete()
        return redirect("consultar_empleado")
    return render(request, "empleado/eliminar_empleado.html", {"empleado": empleado})



########################################## CLIENTE ########################################
@login_required
@cargo_requerido(['admin', 'gerente','cajero' ,])
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

@login_required
@cargo_requerido(['Admin', 'Gerente','cajero'])
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

@login_required
@cargo_requerido(['Admin', 'Gerente'])
def eliminar_cliente(request: HttpRequest, id: int) -> HttpResponse:
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == "POST":
        cliente.delete()
        return redirect("consultar_cliente")
    return render(request, "facturacion_cliente/cliente/eliminar_cliente.html", {"cliente": cliente})

############################################ PRODUCTO ########################################

@login_required
@cargo_requerido(['Admin', 'Gerente'])
def crear_producto(request):
    mensaje = ""
    stock_actual = None
    form = ProductoForm()

    # AJAX para autocompletar producto por número de serie
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        numero_serie = request.GET.get('numero_serie', '').strip()
        try:
            producto = Producto.objects.get(numero_serie__iexact=numero_serie)
            data = {
                'existe': True,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'stock': producto.stock,
                'modelo': producto.modelo,
                'color': producto.color,
                'categoria': producto.categoria,
            }
        except Producto.DoesNotExist:
            data = {'existe': False}
        return JsonResponse(data)

    # Cargar productos activos
    productos = list(Producto.objects.filter(estado=1).values('numero_serie', 'stock'))

    if request.method == 'POST':
            form = ProductoForm(request.POST)
            numero_serie = request.POST.get('numero_serie', '').strip()

            try:
                cantidad = int(request.POST.get('cantidad_ingresar', '0'))
            except (ValueError, TypeError):
                cantidad = 0

            if cantidad <= 0:
                mensaje = "❌ Ingresa una cantidad válida mayor a cero."
            else:
                try:
                    # ✅ Producto ya existe: actualiza solo el stock
                    producto = Producto.objects.get(numero_serie__iexact=numero_serie)
                    producto.stock += cantidad
                    producto.modificacion_usuario = request.user.username
                    producto.save()
                    mensaje = f"✅ Producto existente actualizado. Nuevo stock: {producto.stock}"
                    stock_actual = producto.stock
                    form = ProductoForm()  # Limpiar el formulario
                except Producto.DoesNotExist:
                    # 🆕 Producto nuevo: validamos y lo guardamos
                    if form.is_valid():
                        nuevo = form.save(commit=False)
                        nuevo.stock = cantidad
                        nuevo.creacion_usuario = request.user.username
                        nuevo.modificacion_usuario = request.user.username
                        nuevo.estado = 1
                        nuevo.save()
                        mensaje = "✅ Producto nuevo creado correctamente."
                        stock_actual = nuevo.stock
                        form = ProductoForm()
                    else:
                        mensaje = "❌ Formulario inválido. Revisa los datos."

    productos = list(Producto.objects.filter(estado=1).values('numero_serie', 'stock'))

    return render(request, 'facturacion_cliente/producto/crear_producto.html', {
        'form_Producto': form,
        'mensaje': mensaje,
        'stock_actual': stock_actual,
        'productos_json': json.dumps(productos, ensure_ascii=False),
    })
@login_required
@cargo_requerido(['Admin', 'Gerente','cajero'])
def consultar_producto(request):
    productos = None
    buscarProductoForm = BuscarProductoForm(request.POST or None)

    if request.method == "POST" and 'buscar_producto' in request.POST and buscarProductoForm.is_valid():
        nombre = buscarProductoForm.cleaned_data.get('nombre')
        modelo = buscarProductoForm.cleaned_data.get('modelo')
        numero_serie = buscarProductoForm.cleaned_data.get('numero_serie')
        fecha = buscarProductoForm.cleaned_data.get('fecha')

        filtros = Q()
        if nombre:
            filtros &= Q(nombre__icontains=nombre)
        if modelo:
            filtros &= Q(modelo__icontains=modelo)
        if numero_serie:
            filtros &= Q(numero_serie__icontains=numero_serie)
        if fecha:
            filtros &= Q(fecha_creacion__lte=fecha)

        productos = Producto.objects.filter(filtros)

    context = {
        'buscador_Producto': buscarProductoForm,
        'productos': productos,
    }
    return render(request, "facturacion_cliente/producto/consultar_producto.html", context)

@login_required
@cargo_requerido(['Admin', 'Gerente','cajero'])
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
        allproductos = [( p.nombre, p.modelo, p.numero_serie, p.categoria, p.color, p.stock, p.precio) for p in productos]

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

@login_required
@cargo_requerido(['Admin', 'Gerente'])
def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.modificacion_usuario = request.user.username
            producto.save()
            return redirect('consultar_producto')  # o a donde quieras redirigir
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'facturacion_cliente/producto/modificar_producto.html', {
        'form_Producto': form,
        'producto': producto
    })


@login_required
@cargo_requerido(['admin', 'Gerente'])
def eliminar_producto(request: HttpRequest, id: int) -> HttpResponse:
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.delete()
        return redirect("consultar_producto")
    return render(request, "facturacion_cliente/producto/eliminar_producto.html", {"producto": producto})

######################################################################
# Funciones simples para renderizar templates sin lógica adicional

def filtrar_descuentos(nombre: str = '', porcentaje: Optional[float] = None):
    filtros = Q()
    if nombre:
        filtros &= Q(nombre__icontains=nombre)
    if porcentaje is not None:
        filtros &= Q(porcentaje__gte=porcentaje)
    return Descuento.objects.filter(filtros)

##########################-------------------DESCUEENTO-------------##########################################
@login_required
@cargo_requerido(['admin', 'Gerente'])
def crear_descuento(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DescuentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("consultar_descuento")
    else:
        form = DescuentoForm()
    
    return render(request, "facturacion_cliente/descuento/crear_descuento.html", {
        "form": form,
        "edit_mode": False
    })

@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
def consultar_descuento(request: HttpRequest) -> HttpResponse:
    descuentos = None
    buscarDescuentoForm = BuscarDescuentoForm(request.POST or None)
    
    if request.method == "POST":
        if 'buscar_descuento' in request.POST and buscarDescuentoForm.is_valid():
            nombre = buscarDescuentoForm.cleaned_data.get('nombre', '')
            porcentaje = buscarDescuentoForm.cleaned_data.get('porcentaje', None)
            descuentos = filtrar_descuentos(nombre, porcentaje)

        elif 'exportar_descuento' in request.POST:
            return exportar_pdf_descuento(request)

    return render(request, "facturacion_cliente/descuento/consultar_descuento.html", {
        'buscador_Descuento': buscarDescuentoForm,
        'descuentos': descuentos
    })

@login_required
@cargo_requerido(['admin', 'Gerente'])
def exportar_pdf_descuento(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="listado_descuentos.pdf"'
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=inch / 2,
        leftMargin=inch / 2,
        topMargin=inch / 2,
        bottomMargin=inch / 2
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenteredTitle', alignment=TA_CENTER, fontSize=16, spaceAfter=12))
    styles.add(ParagraphStyle(name='RightAlign', alignment=TA_RIGHT, fontSize=10))

    elementos = []

    # Título
    titulo = Paragraph("Listado de Descuentos", styles['CenteredTitle'])
    elementos.append(titulo)

    # Fecha de emisión
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos.append(Paragraph(f"Fecha de emisión: {fecha}", styles['RightAlign']))
    elementos.append(Spacer(1, 12))

    # Obtener todos los descuentos
    descuentos = Descuento.objects.all()

    if not descuentos.exists():
        elementos.append(Paragraph("No hay descuentos registrados.", styles['Normal']))
    else:
        headings = ['ID', 'producto', 'descuento (%)']

        # ⚠️ Asegúrate que tu modelo tenga el campo "nombre"
        datos = [[d.pk, d.producto, f"{d.descuento:.2f} ,"] for d in descuentos]

        tabla = Table([headings] + datos, colWidths=[50, 250, 100])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#308a9e")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        elementos.append(tabla)

    doc.build(elementos)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
@login_required
@cargo_requerido(['admin', 'Gerente'])
def modificar_descuento(request: HttpRequest, id: int) -> HttpResponse:
    descuento = get_object_or_404(Descuento, id=id)
    if request.method == "POST":
        form = DescuentoForm(request.POST, instance=descuento)
        if form.is_valid():
            form.save()
            return redirect("consultar_descuento")
    else:
        form = DescuentoForm(instance=descuento)
    
    return render(request, "facturacion_cliente/descuento/modificar_descuento.html", {
        "form": form,
        "descuento": descuento,
        "edit_mode": True
    })

@login_required
@cargo_requerido(['admin', 'Gerente'])
def eliminar_descuento(request: HttpRequest, id: int) -> HttpResponse:
    descuento = get_object_or_404(Descuento, id=id)
    if request.method == "POST":
        descuento.delete()
        return redirect("consultar_descuento")
    return render(request, "facturacion_cliente/descuento/eliminar_descuento.html", {
        "descuento": descuento
    })


####################################### ------cotización -------------------    ############################
@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
def crear_cotizacion(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        empleado_id = request.POST.get('empleado_id')
        sucursal_id = request.POST.get('sucursal_id')
        comentario = request.POST.get('comentario', '')
        productos_json = request.POST.get('productos_json')

        if not cliente_id or not productos_json:
            return HttpResponse("Datos incompletos.", status=400)

        try:
            productos = json.loads(productos_json)
        except json.JSONDecodeError:
            return HttpResponse("Error en el formato de productos.", status=400)

        try:
            with transaction.atomic():
                cotizacion = Cotizacion.objects.create(
                    cliente_id=cliente_id,
                    empleado_id=empleado_id if empleado_id else None,
                    sucursal_id=sucursal_id,
                    fecha_emision=timezone.now(),
                    comentario=comentario,
                    creacion_usuario=request.user.username,
                    modificacion_usuario=request.user.username,
                )

                ahora = timezone.now()

                for p in productos:
                    producto = Producto.objects.get(id=p['id'])
                    cantidad = int(p['cantidad'])
                    iva = Iva.objects.get(id=p['iva_id']) if p.get('iva_id') else None

                    descuento_activo = Descuento.objects.filter(
                        producto=producto,
                        estado=1,
                        fecha_inicio__lte=ahora,
                        fecha_final__gte=ahora
                    ).order_by('-fecha_inicio').first()

                    precio_base = producto.precio
                    if descuento_activo and descuento_activo.descuento > 0:
                        descuento_decimal = Decimal(descuento_activo.descuento) / Decimal('100')
                        precio_desc = (precio_base * (Decimal('1') - descuento_decimal)).quantize(Decimal('0.01'))
                        descuento_total = Decimal(descuento_activo.descuento)
                    else:
                        precio_desc = precio_base
                        descuento_total = Decimal('0')

                    Cotizacion_Detalle.objects.create(
                        cotizacion=cotizacion,
                        producto=producto,
                        cantidad_producto=cantidad,
                        precio_cotizado=precio_desc,
                        descuento_total=descuento_total,
                        iva=iva,
                        creacion_usuario=request.user.username,
                        modificacion_usuario=request.user.username
                    )

                totales = cotizacion.get_totales()
                cotizacion.comentario = (cotizacion.comentario or "") + f" | Subtotal: {totales['subtotal']}, IVA: {totales['iva_total']}, Total: {totales['total']}"
                cotizacion.save()

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return HttpResponse(f"Error al procesar la cotización: {str(e)}", status=500)

        pdf_url = reverse('exportar_pdf_cotizacion', kwargs={'cotizacion_id': cotizacion.id})
        return JsonResponse({'success': True, 'pdf_url': pdf_url})

    # Datos para el formulario
    productos = list(Producto.objects.values('id', 'nombre', 'numero_serie', 'precio', 'stock'))
    clientes = list(Cliente.objects.values('id', 'nombre', 'cedula'))
    empleados = list(Empleado.objects.values('id', 'nombre', 'cargo'))
    sucursales = list(Sucursal.objects.values('id', 'nombre', 'direccion'))
    ivas = Iva.objects.all()

    for p in productos:
        if isinstance(p['precio'], Decimal):
            p['precio'] = float(p['precio'])

    context = {
        'productos_json': json.dumps(productos, ensure_ascii=False),
        'clientes_json': json.dumps(clientes, ensure_ascii=False),
        'empleados_json': json.dumps(empleados, ensure_ascii=False),
        'sucursales_json': json.dumps(sucursales, ensure_ascii=False),
        'ivas': ivas,
    }
    return render(request, 'facturacion_cliente/cotizacion/crear_cotizacion.html', context)


@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
def consultar_cotizacion(request):
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    filtros = Q()

    if desde and hasta:
        filtros &= Q(fecha_emision__range=[desde, hasta])
    elif desde:
        filtros &= Q(fecha_emision__gte=desde)
    elif hasta:
        filtros &= Q(fecha_emision__lte=hasta)

    cotizaciones = Cotizacion.objects.filter(filtros).order_by('-fecha_emision')

    # Calcular total para mostrar en la tabla
    for c in cotizaciones:
        totales = c.get_totales()
        c.total_calculado = totales['total'] # type: ignore

    context = {
        'cotizaciones': cotizaciones,
        'desde': desde or '',
        'hasta': hasta or '',
    }
    return render(request, 'facturacion_cliente/cotizacion/consultar_cotizacion.html', context)


@login_required 
@cargo_requerido(['admin', 'Gerente','cajero'])
def exportar_pdf_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cotizacion_{cotizacion_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter, # type: ignore
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)

    styles = getSampleStyleSheet()
    style_title = styles['Heading1']
    style_title.alignment = TA_CENTER
    style_normal = styles['Normal']

    elements = []

    # Título
    elements.append(Paragraph(f"COTIZACIÓN #{cotizacion.id}", style_title))
    elements.append(Spacer(1, 12))

    # Info Cliente
    info = f"""
    <b>Cliente:</b> {cotizacion.cliente.nombre}<br/>
    <b>Fecha:</b> {cotizacion.fecha_emision.strftime('%Y-%m-%d %H:%M')}<br/>
    <b>Comentario:</b> {cotizacion.comentario or 'N/A'}
    """
    elements.append(Paragraph(info, style_normal))
    elements.append(Spacer(1, 20))

    # Tabla de Productos
    data = [['Producto', 'Cantidad', 'Precio Unitario', 'Descuento', 'IVA %', 'Total']]

    for det in cotizacion.detalles.all(): # type: ignore
        subtotal = det.precio_cotizado * det.cantidad_producto
        descuento = det.descuento_total
        iva_pct = det.iva.porcentaje if det.iva else 0
        total_desc = subtotal * (1 - descuento / 100)
        iva_valor = total_desc * iva_pct / 100
        total_final = total_desc + iva_valor

        data.append([
            det.producto.nombre,
            str(det.cantidad_producto),
            f"${det.precio_cotizado:.2f}",
            f"{descuento:.2f}%",
            f"{iva_pct}%",
            f"${total_final:.2f}"
        ])

    totales = cotizacion.get_totales()
    data.append(['', '', '', '', 'Subtotal', f"${totales['subtotal']:.2f}"])
    data.append(['', '', '', '', 'IVA', f"${totales['iva_total']:.2f}"])
    data.append(['', '', '', '', 'Total', f"${totales['total']:.2f}"])

    table = Table(data, colWidths=[2.5*inch, inch, inch, inch, inch, inch])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4F81BD')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('FONTNAME', (-2,-3), (-1,-1), 'Helvetica-Bold'),
    ]))

    elements.append(table)
    doc.build(elements)

    return response

@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
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


@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
def eliminar_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)

    if request.method == "POST":
        cotizacion.delete()
        return redirect("consultar_cotizacion")

    # Enviar cotización al template para mostrar info y confirmar
    context = {
        'cotizacion': cotizacion
    }
    return render(request, "facturacion_cliente/cotizacion/eliminar_cotizacion.html", context)



########################################### Cotización Detalle ########################################
# Funciones para manejar cotización detalle\


@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
def crear_cotizacion_detalle(request):
    if request.method == "POST":
        form = CotizacionDetalleForm(request.POST)
        if form.is_valid():
            cotizacion_detalle = form.save(commit=False)
            cotizacion_detalle.creacion_usuario = request.user.username
            cotizacion_detalle.modificacion_usuario = request.user.username
            cotizacion_detalle.save()
            messages.success(request, "Detalle de cotización creado correctamente.")
            return redirect("consultar_cotizacion_detalle")  # Cambia esto por la vista donde quieres redirigir
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = CotizacionDetalleForm()
    
    context = {
        'form': form,
    }
    return render(request, "facturacion_cliente/cotizacion_detalle/crear_cotizacion_detalle.html", context)

@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
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
@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
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
@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
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



# Tus imports y modelos aquí (Factura, Producto, Iva, Factura_Detalle, etc.)
@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
def crear_factura(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        empleado_id = request.POST.get('empleado_id')
        sucursal_id = request.POST.get('sucursal_id')
        tipo_pago = request.POST.get('tipo_pago')
        comentario = request.POST.get('comentario', '')
        productos_json = request.POST.get('productos_json')

        if not cliente_id or not productos_json:
            return HttpResponse("Datos incompletos.", status=400)

        try:
            productos = json.loads(productos_json)
        except json.JSONDecodeError:
            return HttpResponse("Error en el formato de productos.", status=400)

        try:
            with transaction.atomic():
                factura = Factura.objects.create(
                    cliente_id=cliente_id,
                    empleado_id=empleado_id if empleado_id else None,
                    sucursal_id=sucursal_id,
                    tipo_pago=tipo_pago,
                    fecha_emision=timezone.now(),
                    comentario=comentario,
                    creacion_usuario=request.user.username,
                    modificacion_usuario=request.user.username,
                )

                ahora = timezone.now()

                for p in productos:
                    producto = Producto.objects.get(id=p['id'])
                    cantidad = int(p['cantidad'])
                    iva = Iva.objects.get(id=p['iva_id']) if p.get('iva_id') else None

                    if producto.stock < cantidad:
                        return HttpResponse(f"Stock insuficiente para {producto.nombre}", status=400)

                    descuento_activo = Descuento.objects.filter(
                        producto=producto,
                        estado=1,
                        fecha_inicio__lte=ahora,
                        fecha_final__gte=ahora
                    ).order_by('-fecha_inicio').first()

                    precio_base = producto.precio
                    if descuento_activo and descuento_activo.descuento > 0:
                        descuento_decimal = Decimal(descuento_activo.descuento) / Decimal('100')
                        precio_desc = (precio_base * (Decimal('1') - descuento_decimal)).quantize(Decimal('0.01'))
                        descuento_total = Decimal(descuento_activo.descuento)
                    else:
                        precio_desc = precio_base
                        descuento_total = Decimal('0')

                    producto.stock -= cantidad
                    producto.save()

                    Factura_Detalle.objects.create(
                        factura=factura,
                        producto=producto,
                        cantidad_producto=cantidad,
                        precio_factura=precio_desc,
                        descuento_total=descuento_total,
                        iva=iva,
                        creacion_usuario=request.user.username,
                        modificacion_usuario=request.user.username
                    )

                totales = factura.get_totales
                factura.comentario = (factura.comentario or "") + f" | Subtotal: {totales['subtotal']}, IVA: {totales['iva_total']}, Total: {totales['total']}"
                factura.save()

        except Exception as e:
            return HttpResponse(f"Error al procesar la factura: {str(e)}", status=500)

        return redirect(f"{reverse('crear_factura')}?pdf_factura={factura.pk}")




    # Si no es POST, se asume GET y se preparan datos para el formulario:
    productos = list(Producto.objects.values('id', 'nombre', 'numero_serie', 'precio', 'stock'))
    clientes = list(Cliente.objects.values('id', 'nombre', 'cedula'))
    empleados = list(Empleado.objects.values('id', 'nombre', 'cargo'))
    sucursales = list(Sucursal.objects.values('id', 'nombre', 'direccion'))
    ivas = Iva.objects.all()

    # Convertir Decimal a float para evitar problemas con JSON
    for p in productos:
        if isinstance(p['precio'], Decimal):
            p['precio'] = float(p['precio'])

    context = {
        'productos_json': json.dumps(productos, ensure_ascii=False),
        'clientes_json': json.dumps(clientes, ensure_ascii=False),
        'empleados_json': json.dumps(empleados, ensure_ascii=False),
        'sucursales_json': json.dumps(sucursales, ensure_ascii=False),
        'ivas': ivas,
    }

    return render(request, 'facturacion_cliente/factura/crear_factura.html', context)


@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
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

@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
def consultar_factura(request, id=None):
    factura = None
    if id is not None:
        factura = get_object_or_404(Factura, pk=id)
    
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
                total = f.detalles.aggregate(total=Sum('total_factura_valor'))['total'] or 0  # type: ignore
                f.total_calculado = total  # type: ignore

        elif 'exportar_factura' in request.POST:
            return exportar_pdf_factura(request)

    context = {
        'buscador_factura': buscar_form,
        'facturas': facturas,
        'factura': factura,
    }
    return render(request, 'facturacion_cliente/factura/consultar_factura.html', context)



@login_required
@cargo_requerido(['admin', 'Gerente','cajero'])
def exportar_pdf_factura(request):
    factura_id = request.GET.get('factura_id') or request.POST.get('factura_id')

    if not factura_id:
        return HttpResponse("ID de factura no proporcionado.", status=400)

    try:
        factura = Factura.objects.get(pk=factura_id)
    except Factura.DoesNotExist:
        return HttpResponse("Factura no encontrada.", status=404)

    sucursal = factura.sucursal  # Relación directa desde Factura

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    left_margin = 50
    top = height - 50

    # --- ENCABEZADO EMPRESA Y FACTURA ---
    p.setFont("Helvetica-Bold", 10)
    p.drawString(left_margin, top - 15, f"R.U.C.: {sucursal.ruc}")
    p.setFont("Helvetica", 9)
    p.drawString(left_margin, top - 30, sucursal.nombre.upper())
    p.drawString(left_margin, top - 45, f"Local: {sucursal.local}")
    p.drawString(left_margin, top - 60, f"Dirección: {sucursal.direccion}")
    p.drawString(left_margin, top - 75, f"Teléfono: {sucursal.telefono}")
    p.drawString(left_margin, top - 90, f"Correo: {sucursal.correo}")
    p.drawString(left_margin, top - 105, "Obligado a llevar contabilidad: SI")
    p.drawString(left_margin, top - 120, "Emisión: NORMAL")

    # 🔶 Factura (derecha)
    right_x = width - 250
    p.setFont("Helvetica-Bold", 10)
    p.drawString(right_x, top - 15, f"FACTURA No.: {factura.numero_factura or 'N/A'}")
    p.setFont("Helvetica", 9)
    p.drawString(right_x, top - 30, "AUTORIZACIÓN:")
    p.setFont("Helvetica", 7)
    p.drawString(right_x, top - 45, getattr(factura, 'numero_autorizacion', '000000000000000'))
    p.setFont("Helvetica", 9)
    p.drawString(right_x, top - 60, f"Fecha Emisión: {factura.fecha_emision.strftime('%d/%m/%Y')}")
    
    fecha_pago = getattr(factura, 'fecha_pago_limite', None)
    if fecha_pago:
        p.drawString(right_x, top - 75, f"Fecha Máx. de Pago: {fecha_pago.strftime('%d/%m/%Y')}")

    # Línea separadora
    p.line(left_margin, top - 135, width - left_margin, top - 135)

    # --- INFORMACIÓN DEL CLIENTE ---
    p.setFont("Helvetica-Bold", 10)
    p.drawString(left_margin, top - 150, "CLIENTE:")
    p.setFont("Helvetica", 9)
    cliente = factura.cliente
    p.drawString(left_margin + 70, top - 150, f"{cliente.nombre} {cliente.apellido}   C.I.: {cliente.cedula}")
    p.drawString(left_margin + 70, top - 165, f"Dirección: {cliente.direccion or 'No disponible'}")
    p.drawString(left_margin + 70, top - 180, f"Teléfono: {cliente.telefono or 'N/A'}")
    p.drawString(left_margin + 70, top - 195, f"Email: {cliente.correo or 'N/A'}")

    # --- DETALLES DE PRODUCTOS ---
    detalles = factura.detalles.filter(estado=1) # type: ignore
    data = [["Producto", "Cantidad", "Precio Unitario", "Subtotal", "IVA", "Total"]]

    subtotal_general, iva_general, total_general = 0, 0, 0

    for d in detalles:
        subtotal_general += d.subtotal or 0
        iva_general += d.iva_total or 0
        total_general += d.total_calculado or 0

        data.append([
            str(d.producto),
            str(d.cantidad_producto),
            f"{d.precio_factura:.2f}",
            f"{d.subtotal:.2f}",
            f"{d.iva_total:.2f}",
            f"{d.total_calculado:.2f}",
        ])

    table = Table(data, colWidths=[140, 60, 70, 70, 60, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#dbe5f1")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
    ]))

    table_width, table_height = table.wrap(0, 0)
    table_y = top - 230 - table_height
    if table_y < 100:
        p.showPage()
        table_y = height - 100

    table.drawOn(p, left_margin, table_y)

    # --- TOTALES ---
    y_totales = table_y - 40
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.black)
    p.drawRightString(width - 60, y_totales, f"Subtotal: {subtotal_general:.2f}")
    p.drawRightString(width - 60, y_totales - 15, f"IVA Total: {iva_general:.2f}")
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#003366"))
    p.drawRightString(width - 60, y_totales - 35, f"TOTAL A PAGAR: {total_general:.2f}")

    # --- FOOTER ---
    p.setFont("Helvetica-Oblique", 8)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, 30, "Gracias por su compra. Documento generado electrónicamente.")

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f'Factura_{factura.numero_factura or factura.pk}.pdf', content_type='application/pdf')

@login_required
@cargo_requerido(['admin', 'Gerente'])
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
@login_required
@cargo_requerido(['Admin', 'Gerente'])
def anular_factura(request, id):
    factura = get_object_or_404(Factura, pk=id)

    if request.method == 'POST':
        factura.estado = 0
        factura.save()
        return redirect('consultar_factura')

    return render(request, 'factura/anular.html', {'factura': factura})
@login_required
@cargo_requerido(['admin', 'Gerente'])


def eliminar_factura(request, id):
    factura = get_object_or_404(Factura, factura_codigo=id)

    if request.method == "POST":
        detalles = Factura_Detalle.objects.filter(factura=factura)

        for detalle in detalles:
            producto = detalle.producto
            producto.stock += detalle.cantidad_producto
            producto.save()

        # Primero eliminamos los detalles y luego la factura
        detalles.delete()
        factura.delete()

        messages.success(request, "Factura eliminada correctamente y stock restaurado.")
        return redirect('consultar_factura')

    context = {
        'factura': factura,
    }
    return render(request, "facturacion_cliente/factura/eliminar_factura.html", context)


######################################### Proveedor#########################################
@login_required
@cargo_requerido(['admin', 'Gerente'])
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
@login_required
@cargo_requerido(['admin', 'Gerente'])
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


@login_required
@cargo_requerido(['admin', 'Gerente'])        
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

   
@login_required
@cargo_requerido(['admin', 'Gerente'])
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

@login_required
@cargo_requerido(['admin', 'Gerente'])
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
