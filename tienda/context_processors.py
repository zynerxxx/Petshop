from tienda.models import Carrito

def carrito_cantidad(request):
    cantidad = 0
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        cantidad = sum(item.cantidad for item in carrito.items.all())
    if cantidad > 9:
        cantidad = '+9'
    return {'carrito_cantidad': cantidad}