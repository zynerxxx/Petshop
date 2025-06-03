from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/quitar/<int:item_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('carrito/comprar/', views.realizar_compra, name='realizar_compra'),
    path('registro/', views.registro, name='registro'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('productos/', views.productos, name='productos'),
    path('accesorios/', views.accesorios, name='accesorios'),
    path('agregar-accesorio/<int:accesorio_id>/', views.agregar_accesorio_al_carrito, name='agregar_accesorio_al_carrito'),
    path('carrito/disminuir/<int:item_id>/', views.disminuir_cantidad_carrito, name='disminuir_cantidad_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('accesorio/<int:accesorio_id>/', views.accesorio_detalle, name='accesorio_detalle'),
    path('historial-ventas/', views.historial_ventas_admin, name='historial_ventas_admin'),
    path('mis-compras/', views.historial_compras_usuario, name='historial_compras_usuario'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='tienda/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='tienda/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='tienda/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='tienda/password_reset_complete.html'), name='password_reset_complete'),
    path('accesorios/ajax/', views.accesorios_ajax, name='accesorios_ajax'),
    path('productos/ajax/', views.productos_ajax, name='productos_ajax'),
    path('carrito/ajax/actualizar-cantidad/', views.ajax_actualizar_cantidad_carrito, name='ajax_actualizar_cantidad_carrito'),
    path('carrito/ajax/eliminar-item/', views.ajax_eliminar_item_carrito, name='ajax_eliminar_item_carrito'),
    path('carrito/ajax/vaciar/', views.ajax_vaciar_carrito, name='ajax_vaciar_carrito'),
    path('carrito/ajax/agregar/', views.ajax_agregar_al_carrito, name='ajax_agregar_al_carrito'),
]
