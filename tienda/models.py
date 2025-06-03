from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
import os
from django.conf import settings

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('usuario', 'Usuario'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='usuario')

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.imagen:
            orig_path = self.imagen.path
            thumb_dir = os.path.join(settings.MEDIA_ROOT, 'productos', 'thumbnails')
            os.makedirs(thumb_dir, exist_ok=True)
            filename = os.path.basename(orig_path)
            thumb_path = os.path.join(thumb_dir, filename)
            if not os.path.exists(thumb_path):
                try:
                    with Image.open(orig_path) as img:
                        img.thumbnail((320, 320))
                        img.save(thumb_path, format=img.format, quality=80)
                except Exception:
                    pass

    @property
    def thumbnail_url(self):
        if self.imagen:
            return self.imagen.url.replace('/media/productos/', '/media/productos/thumbnails/')
        return ''

class Venta(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta #{self.id} - {self.usuario} - {self.fecha:%Y-%m-%d %H:%M}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey('Venta', related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', null=True, blank=True, on_delete=models.SET_NULL)
    accesorio = models.ForeignKey('Accesorio', null=True, blank=True, on_delete=models.SET_NULL)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        if self.producto:
            return f"{self.producto.nombre} x{self.cantidad}"
        elif self.accesorio:
            return f"{self.accesorio.nombre} x{self.cantidad}"
        return f"Detalle x{self.cantidad}"

class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, null=True, blank=True, on_delete=models.CASCADE)
    accesorio = models.ForeignKey('Accesorio', null=True, blank=True, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.producto:
            return f"{self.producto.nombre} x{self.cantidad}"
        elif self.accesorio:
            return f"{self.accesorio.nombre} x{self.cantidad}"
        return f"Item x{self.cantidad}"

class CategoriaAccesorio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Accesorio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='accesorios/', blank=True, null=True)
    categoria = models.ForeignKey(CategoriaAccesorio, on_delete=models.CASCADE, related_name='accesorios')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.imagen:
            orig_path = self.imagen.path
            thumb_dir = os.path.join(settings.MEDIA_ROOT, 'accesorios', 'thumbnails')
            os.makedirs(thumb_dir, exist_ok=True)
            filename = os.path.basename(orig_path)
            thumb_path = os.path.join(thumb_dir, filename)
            if not os.path.exists(thumb_path):
                try:
                    with Image.open(orig_path) as img:
                        img.thumbnail((320, 320))
                        img.save(thumb_path, format=img.format, quality=80)
                except Exception:
                    pass

    @property
    def thumbnail_url(self):
        if self.imagen:
            return self.imagen.url.replace('/media/accesorios/', '/media/accesorios/thumbnails/')
        return ''
