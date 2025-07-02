from django import template

register = template.Library()

@register.filter
def get_precio(queryset, producto_id):
    try:
        producto = queryset.get(pk=producto_id)
        return producto.precio
    except:
        return 0
