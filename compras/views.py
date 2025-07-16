from django.shortcuts import render, get_object_or_404, redirect

from miapp.views import cargo_requerido
from .models import *
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum



@transaction.atomic
def crear_compra(request):
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        productos_ids = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')

        if not (proveedor_id and productos_ids and cantidades and precios):
            messages.error(request, "❌ Todos los campos son obligatorios.")
            return redirect('crear_compra')

        try:
            proveedor = get_object_or_404(Proveedor, id=proveedor_id)
            fecha_compra = request.POST.get('fecha_compra') or timezone.now().date()
            numero_factura = request.POST.get('numero_factura', '').strip()

            detalles = []
            subtotal = iva = total = 0

            for i in range(len(productos_ids)):
                producto = get_object_or_404(Producto, id=productos_ids[i])
                cantidad = int(cantidades[i])
                precio = float(precios[i])

                sub = cantidad * precio
                iva_item = sub * 0.12
                total_item = sub + iva_item

                detalles.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': sub,
                    'iva': iva_item,
                    'total': total_item,
                })

                subtotal += sub
                iva += iva_item
                total += total_item

            compra = Compra.objects.create(
                proveedor=proveedor,
                fecha_compra=fecha_compra,
                numero_factura=numero_factura,
                subtotal=subtotal,
                iva=iva,
                total=total
            )

            for d in detalles:
                Detalle_Compra.objects.create(
                    compra=compra,
                    producto=d['producto'],
                    cantidad=d['cantidad'],
                    precio_unitario=d['precio'],
                    iva_aplicado=12.00
                )

            messages.success(request, "✅ Compra registrada exitosamente.")
            return redirect('consultar_compras')

        except Exception as e:
            messages.error(request, f"❌ Error al registrar la compra: {e}")
            return redirect('crear_compra')

    return render(request, 'administrativo/compra/crear_compras.html', {
        'proveedores': proveedores,
        'productos': productos
    })


from django.shortcuts import render, get_object_or_404

def consultar_compra(request, id):
    compra = get_object_or_404(Compra, id=id)
    detalles = compra.detalles_compras.all()  # type: ignore # Usa related_name definido
    return render(request, 'administrativo/compra/detalle_compra.html', {
        'compra': compra,
        'detalles': detalles,
    })




def exportar_pdf_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    detalles = compra.detalles.all() # type: ignore

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Compra_{compra.numero_factura}.pdf"'

    c = canvas.Canvas(response, pagesize=letter) # type: ignore
    width, height = letter
    x_margin = 0.75 * inch
    y = height - inch

    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_margin, y, f"Factura de Compra N° {compra.numero_factura}")
    y -= 0.4 * inch

    c.setFont("Helvetica", 12)
    c.drawString(x_margin, y, f"Proveedor: {compra.proveedor.nombre}")
    y -= 0.25 * inch
    c.drawString(x_margin, y, f"Fecha: {compra.fecha_compra.strftime('%d/%m/%Y')}")
    y -= 0.25 * inch
    c.drawString(x_margin, y, f"Subtotal: ${compra.subtotal:.2f}")
    y -= 0.25 * inch
    c.drawString(x_margin, y, f"IVA (12%): ${compra.iva:.2f}")
    y -= 0.25 * inch
    c.drawString(x_margin, y, f"Total: ${compra.total:.2f}")
    y -= 0.5 * inch

    # Encabezado tabla
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, "Producto")
    c.drawString(x_margin + 2.5 * inch, y, "Cantidad")
    c.drawString(x_margin + 4 * inch, y, "P. Unitario")
    c.drawString(x_margin + 5.5 * inch, y, "IVA %")
    c.drawString(x_margin + 6.5 * inch, y, "Total")
    y -= 0.2 * inch

    # Detalles de productos
    c.setFont("Helvetica", 10)
    for detalle in detalles:
        if y < inch:
            c.showPage()
            y = height - inch

        subtotal_detalle = detalle.cantidad * detalle.precio_unitario
        iva_valor = subtotal_detalle * (detalle.iva_aplicado / 100)
        total_detalle = subtotal_detalle + iva_valor

        c.drawString(x_margin, y, detalle.producto.nombre)
        c.drawString(x_margin + 2.5 * inch, y, str(detalle.cantidad))
        c.drawString(x_margin + 4 * inch, y, f"${detalle.precio_unitario:.2f}")
        c.drawString(x_margin + 5.5 * inch, y, f"{detalle.iva_aplicado:.2f}%")
        c.drawString(x_margin + 6.5 * inch, y, f"${total_detalle:.2f}")
        y -= 0.2 * inch

    c.showPage()
    c.save()
    return response

@login_required
@cargo_requerido('admin' )
def reporte_compras_sri(request):
    # Valores por defecto al mes y año actual
    hoy = timezone.now()
    mes = request.GET.get('mes', str(hoy.month))
    anio = request.GET.get('anio', str(hoy.year))

    # Filtrar compras por mes y año
    compras = Compra.objects.filter(
        fecha_compra__year=anio,
        fecha_compra__month=mes
    ).order_by('fecha_compra')

    resumen = compras.aggregate(
        subtotal=Sum('subtotal'),
        iva=Sum('iva'),
        total=Sum('total')
    )

    # Si no hay compras, evitar None en el template
    resumen = {
        'subtotal': resumen['subtotal'] or 0,
        'iva': resumen['iva'] or 0,
        'total': resumen['total'] or 0,
    }

    context = {
        'compras': compras,
        'mes': int(mes),
        'anio': int(anio),
        'resumen': resumen,
    }
    return render(request, 'administrativo/compra/reporte_sri.html', context)