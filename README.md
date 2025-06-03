# Petshop Django

Este proyecto es una tienda de mascotas (Petshop) desarrollada con Django.

## Características
- Autenticación de usuarios y roles (admin, empleado, usuario)
- Carrito de compras
- Gestión de productos y ventas
- Interfaz responsiva con Bootstrap y Bootstrap Icons
- Sistema de plantillas de Django
- Mensajes y notificaciones

## Instalación
1. Crear entorno virtual:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```cmd
   pip install -r requirements.txt
   ```
3. Migrar la base de datos:
   ```cmd
   python manage.py migrate
   ```
4. Crear superusuario:
   ```cmd
   python manage.py createsuperuser
   ```
5. Ejecutar el servidor:
   ```cmd
   python manage.py runserver
   ```

## Estructura
- `petshop/` - Configuración principal del proyecto
- `tienda/` - Aplicación principal (productos, ventas, usuarios)

## Personalización
- Los estilos y plantillas se encuentran en `tienda/static/` y `tienda/templates/`
- Configura los roles y permisos en `tienda/models.py` y `tienda/admin.py`

---

Este README se actualizará conforme avance el desarrollo.
