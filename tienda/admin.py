from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Producto, Venta, DetalleVenta, Carrito, ItemCarrito, CategoriaAccesorio, Accesorio, CategoriaProducto

admin.site.register(Usuario, UserAdmin)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(CategoriaAccesorio)
admin.site.register(Accesorio)
admin.site.register(CategoriaProducto)
