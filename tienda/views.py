from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Carrito, ItemCarrito, Venta, DetalleVenta, Accesorio, CategoriaAccesorio, CategoriaProducto
from django.contrib.auth import get_user_model, login
from .forms import RegistroForm
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

User = get_user_model()

def home(request):
    productos = Producto.objects.filter(activo=True)[:8]
    accesorios = Accesorio.objects.filter(activo=True)[:8]
    categorias = CategoriaAccesorio.objects.all()
    categorias_productos = CategoriaProducto.objects.all()
    return render(request, 'tienda/home.html', {
        'productos': productos,
        'accesorios': accesorios,
        'categorias': categorias,
        'categorias_productos': categorias_productos,
    })

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        item.cantidad += 1
    item.save()
    messages.success(request, f"{producto.nombre} agregado al carrito.")
    # Redirigir a la página anterior
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = sum(
        (item.producto.precio if item.producto else item.accesorio.precio) * item.cantidad
        for item in items if (item.producto or item.accesorio)
    )
    return render(request, 'tienda/carrito.html', {'items': items, 'total': total})

@login_required
def quitar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, "Ítem eliminado del carrito.")
    return redirect('ver_carrito')

@login_required
def realizar_compra(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = sum(
        (item.producto.precio if item.producto else item.accesorio.precio) * item.cantidad
        for item in items if (item.producto or item.accesorio)
    )
    if not items:
        messages.warning(request, "El carrito está vacío.")
        return redirect('ver_carrito')
    venta = Venta.objects.create(usuario=request.user, total=total)
    for item in items:
        DetalleVenta.objects.create(
            venta=venta,
            producto=item.producto if item.producto else None,
            accesorio=item.accesorio if item.accesorio else None,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio if item.producto else item.accesorio.precio
        )
        if item.producto:
            if item.producto.stock < item.cantidad:
                messages.error(request, f"No hay suficiente stock de {item.producto.nombre}.")
                venta.delete()
                return redirect('ver_carrito')
            item.producto.stock -= item.cantidad
            item.producto.save()
        if item.accesorio:
            if item.accesorio.stock < item.cantidad:
                messages.error(request, f"No hay suficiente stock de {item.accesorio.nombre}.")
                venta.delete()
                return redirect('ver_carrito')
            item.accesorio.stock -= item.cantidad
            item.accesorio.save()
    items.delete()
    messages.success(request, f"¡Compra realizada por ${total:.2f}!")
    return redirect('home')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a Petshop.')
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'tienda/registro.html', {'form': form})

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    return render(request, 'tienda/producto_detalle.html', {'producto': producto})

def productos(request):
    productos = Producto.objects.filter(activo=True)
    categorias = CategoriaProducto.objects.all()
    categoria_id = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    q = request.GET.get('q')

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))

    return render(request, 'tienda/productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_id': categoria_id,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'q': q,
    })

def accesorios(request):
    accesorios = Accesorio.objects.filter(activo=True)
    categorias = CategoriaAccesorio.objects.all()
    categoria_id = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    q = request.GET.get('q')

    if categoria_id:
        accesorios = accesorios.filter(categoria_id=categoria_id)
    if precio_min:
        accesorios = accesorios.filter(precio__gte=precio_min)
    if precio_max:
        accesorios = accesorios.filter(precio__lte=precio_max)
    if q:
        accesorios = accesorios.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))

    return render(request, 'tienda/accesorios.html', {
        'accesorios': accesorios,
        'categorias': categorias,
        'categoria_id': categoria_id,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'q': q,
    })

@login_required
def agregar_accesorio_al_carrito(request, accesorio_id):
    accesorio = get_object_or_404(Accesorio, id=accesorio_id)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, accesorio=accesorio)
    if not created:
        item.cantidad += 1
    item.save()
    messages.success(request, f"{accesorio.nombre} agregado al carrito.")
    # Redirigir a la página anterior
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def disminuir_cantidad_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
        messages.info(request, "Cantidad disminuida.")
    else:
        item.delete()
        messages.info(request, "Ítem eliminado del carrito.")
    return redirect('ver_carrito')

@login_required
def vaciar_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    carrito.items.all().delete()
    messages.success(request, "Carrito vaciado.")
    return redirect('ver_carrito')

def accesorio_detalle(request, accesorio_id):
    accesorio = get_object_or_404(Accesorio, id=accesorio_id, activo=True)
    return render(request, 'tienda/accesorio_detalle.html', {'accesorio': accesorio})

@staff_member_required
def historial_ventas_admin(request):
    ventas = Venta.objects.select_related('usuario').prefetch_related('detalles').order_by('-fecha')
    return render(request, 'tienda/historial_ventas_admin.html', {'ventas': ventas})

@login_required
def historial_compras_usuario(request):
    ventas = Venta.objects.filter(usuario=request.user).prefetch_related('detalles').order_by('-fecha')
    return render(request, 'tienda/historial_compras_usuario.html', {'ventas': ventas})

def accesorios_ajax(request):
    accesorios = Accesorio.objects.select_related('categoria').only(
        'id', 'nombre', 'descripcion', 'precio', 'imagen', 'categoria__nombre', 'activo'
    ).filter(activo=True)
    categoria_id = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    q = request.GET.get('q')
    page = int(request.GET.get('page', 1))
    if categoria_id:
        accesorios = accesorios.filter(categoria_id=categoria_id)
    if precio_min:
        accesorios = accesorios.filter(precio__gte=precio_min)
    if precio_max:
        accesorios = accesorios.filter(precio__lte=precio_max)
    if q:
        accesorios = accesorios.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
    paginator = Paginator(accesorios, 8)
    page_obj = paginator.get_page(page)
    data = {
        'accesorios': [
            {
                'id': a.id,
                'nombre': a.nombre,
                'descripcion': a.descripcion,
                'precio': str(a.precio),
                'imagen': a.thumbnail_url,
                'categoria': a.categoria.nombre if a.categoria else '',
                'authenticated': request.user.is_authenticated,
            } for a in page_obj.object_list
        ],
        'has_next': page_obj.has_next(),
    }
    return JsonResponse(data)

def productos_ajax(request):
    productos = Producto.objects.select_related('categoria').only(
        'id', 'nombre', 'descripcion', 'precio', 'imagen', 'categoria__nombre', 'activo'
    ).filter(activo=True)
    categoria_id = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    q = request.GET.get('q')
    page = int(request.GET.get('page', 1))
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
    paginator = Paginator(productos, 8)
    page_obj = paginator.get_page(page)
    data = {
        'productos': [
            {
                'id': p.id,
                'nombre': p.nombre,
                'descripcion': p.descripcion,
                'precio': str(p.precio),
                'imagen': p.thumbnail_url,
                'categoria': p.categoria.nombre if p.categoria else '',
                'authenticated': request.user.is_authenticated,
            } for p in page_obj.object_list
        ],
        'has_next': page_obj.has_next(),
    }
    return JsonResponse(data)

@login_required
@require_POST
def ajax_actualizar_cantidad_carrito(request):
    item_id = request.POST.get('item_id')
    cantidad = request.POST.get('cantidad')
    try:
        cantidad = int(cantidad)
        item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
        if cantidad < 1:
            item.delete()
            msg = 'Ítem eliminado del carrito.'
        else:
            item.cantidad = cantidad
            item.save()
            msg = 'Cantidad actualizada.'
        # Recalcular total
        carrito = item.carrito
        items = carrito.items.all()
        total = sum((i.producto.precio if i.producto else i.accesorio.precio) * i.cantidad for i in items if (i.producto or i.accesorio))
        # Devolver datos actualizados
        return JsonResponse({
            'ok': True,
            'msg': msg,
            'item_id': item_id,
            'cantidad': cantidad if cantidad > 0 else 0,
            'total': f'{total:.2f}',
        })
    except Exception as e:
        return JsonResponse({'ok': False, 'msg': 'Error al actualizar el carrito.'}, status=400)

@login_required
@require_POST
def ajax_eliminar_item_carrito(request):
    item_id = request.POST.get('item_id')
    try:
        item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
        item.delete()
        carrito = item.carrito
        items = carrito.items.all()
        total = sum((i.producto.precio if i.producto else i.accesorio.precio) * i.cantidad for i in items if (i.producto or i.accesorio))
        return JsonResponse({'ok': True, 'msg': 'Ítem eliminado.', 'item_id': item_id, 'total': f'{total:.2f}'})
    except Exception as e:
        return JsonResponse({'ok': False, 'msg': 'Error al eliminar el ítem.'}, status=400)

@login_required
@require_POST
def ajax_vaciar_carrito(request):
    try:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        carrito.items.all().delete()
        return JsonResponse({'ok': True, 'msg': 'Carrito vaciado.', 'total': '0.00'})
    except Exception as e:
        return JsonResponse({'ok': False, 'msg': 'Error al vaciar el carrito.'}, status=400)

@login_required
@require_POST
def ajax_agregar_al_carrito(request):
    producto_id = request.POST.get('producto_id')
    accesorio_id = request.POST.get('accesorio_id')
    try:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        if producto_id:
            producto = get_object_or_404(Producto, id=producto_id)
            item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
            if not created:
                item.cantidad += 1
            item.save()
            nombre = producto.nombre
        elif accesorio_id:
            accesorio = get_object_or_404(Accesorio, id=accesorio_id)
            item, created = ItemCarrito.objects.get_or_create(carrito=carrito, accesorio=accesorio)
            if not created:
                item.cantidad += 1
            item.save()
            nombre = accesorio.nombre
        else:
            return JsonResponse({'ok': False, 'msg': 'No se especificó producto o accesorio.'}, status=400)
        cantidad_total = sum(i.cantidad for i in carrito.items.all())
        return JsonResponse({'ok': True, 'msg': f'{nombre} agregado al carrito.', 'carrito_cantidad': cantidad_total})
    except Exception as e:
        return JsonResponse({'ok': False, 'msg': 'Error al agregar al carrito.'}, status=400)
