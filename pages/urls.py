from django.urls import path
from pages.views import index, notificaciones_pagina, privacy_policy, refund_policy
from pages.views import delivery_policy, sucursales_empresa, acerca_de, cambiar_password
from pages.views import carrito, internal_error, terms_service, frecuency_partners, contactenos
from pages.views import without_permission, productos_inicio, faqs

urlpatterns = [
    path('', index, name='index'),

    # path('notificacionespagina/', notificaciones_pagina, name='notificaciones_pagina'),
    # path('notificacionespush/', notificaciones_push, name='notificaciones_push'),

    # links
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
    path('refund_policy/', refund_policy, name='refund_policy'),
    path('terms_service/', terms_service, name='terms_service'),
    path('delivery_policy/', delivery_policy, name='delivery_policy'),
    path('faqs/', faqs, name='faqs'),
    path('frecuency_partners/', frecuency_partners, name='frecuency_partners'),

    path('productosinicio/', productos_inicio, name='productos_inicio'),
    path('sucursalesempresa/', sucursales_empresa, name='sucursales_empresa'),
    path('acercade/', acerca_de, name='acerca_de'),
    path('contactenos/', contactenos, name='contactenos'),
    path('cambiarpassword/', cambiar_password, name='cambiar_password'),
    path('carrito/', carrito, name='carrito'),
    path('notificacionespagina/', notificaciones_pagina, name='notificaciones_pagina'),

    path('without_permission', without_permission, name='without_permission'),
    path('internal_error', internal_error, name='internal_error'),
]
