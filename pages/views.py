from datetime import datetime
from django.shortcuts import render
from django.conf import settings

# configuraciones
from src.configuraciones.configuraciones import configuraciones_index
from src.configuraciones.lineas import lineas_index
from src.configuraciones.materiales import materiales_index
from src.configuraciones.tipos_montura import tipos_montura_index
from src.configuraciones.tecnicos import tecnicos_index
from src.configuraciones.sucursales import sucursales_index
from src.configuraciones.puntos import puntos_index
from src.configuraciones.laboratorios import laboratorios_index
from src.configuraciones.oftalmologos import oftalmologos_index
from src.configuraciones.proveedores import proveedores_index
from src.configuraciones.usuarios import usuarios_index

# clientes
from src.clientes.clientes import clientes_index

# cajas
from src.cajas.cajas_iniciar import cajas_iniciar_index
from src.cajas.cajas_iniciar_recibir import cajas_iniciar_recibir_index
from src.cajas.cajas_entregar import cajas_entregar_index
from src.cajas.cajas_entregar_recibir import cajas_entregar_recibir_index
from src.cajas.cajas_movimientos import cajas_movimientos_index
from src.cajas.cajas_ingresos import cajas_ingresos_index
from src.cajas.cajas_egresos import cajas_egresos_index

# productos
from src.productos.productos import productos_index
# inventarios
from src.inventarios.ingresos_almacen import ingresos_almacen_index
from src.inventarios.salidas_almacen import salidas_almacen_index
from src.inventarios.movimientos_almacen import movimientos_almacen_index

# ventas
from src.ventas.ventas import ventas_index
from src.ventas.pendientes import pendientes_index
from src.ventas.reservas import reservas_index
from src.ventas.pedidos import pedidos_cliente_index
# reportes
from src.reportes.reportes import reportes_index

# password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from decimal import Decimal

# fechas
from utils.dates_functions import fecha_periodo, get_date_to_db, get_date_show, get_date_system, get_calendario_actividades
from utils.dates_functions import next_periodo, previous_periodo
from utils.permissions import get_system_settings, get_user_permission_operation

# mensaje html
import smtplib
from django.apps import apps
# reverse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
# cursor
from django.db import connection

# xls
import openpyxl
import os
import zipfile
from django.http import FileResponse

from pages.utils import reemplazar_codigo_html, get_lista_session, get_lista_cuadros, link_linea, lista_productos


def index(request):
    """pagina index"""

    if 'module_x' in request.POST.keys():
        module_id = int(request.POST['module_x'])

        # cambiar password
        if module_id == 1000:
            return cambiar_password(request)

        if module_id == settings.MOD_CONFIGURACIONES_SISTEMA:
            return configuraciones_index(request)

        if module_id == settings.MOD_LINEAS:
            return lineas_index(request)

        if module_id == settings.MOD_MATERIALES:
            return materiales_index(request)

        if module_id == settings.MOD_TIPOS_MONTURA:
            return tipos_montura_index(request)

        if module_id == settings.MOD_LABORATORIOS:
            return laboratorios_index(request)

        if module_id == settings.MOD_TECNICOS:
            return tecnicos_index(request)

        if module_id == settings.MOD_OFTALMOLOGOS:
            return oftalmologos_index(request)

        if module_id == settings.MOD_PROVEEDORES:
            return proveedores_index(request)

        if module_id == settings.MOD_SUCURSALES:
            return sucursales_index(request)

        if module_id == settings.MOD_PUNTOS:
            return puntos_index(request)

        if module_id == settings.MOD_USUARIOS:
            return usuarios_index(request)

        # cajas
        # cajas
        if module_id == settings.MOD_INICIAR_CAJA:
            return cajas_iniciar_index(request)

        if module_id == settings.MOD_INICIAR_CAJA_RECIBIR:
            return cajas_iniciar_recibir_index(request)

        if module_id == settings.MOD_ENTREGAR_CAJA:
            return cajas_entregar_index(request)

        if module_id == settings.MOD_ENTREGAR_CAJA_RECIBIR:
            return cajas_entregar_recibir_index(request)

        if module_id == settings.MOD_CAJAS_INGRESOS:
            return cajas_ingresos_index(request)

        if module_id == settings.MOD_CAJAS_EGRESOS:
            return cajas_egresos_index(request)

        if module_id == settings.MOD_CAJAS_MOVIMIENTOS:
            return cajas_movimientos_index(request)

        # clientes
        if module_id == settings.MOD_CLIENTES:
            return clientes_index(request)

        # productos
        if module_id == settings.MOD_PRODUCTOS:
            return productos_index(request)

        # ingresos almacen
        if module_id == settings.MOD_INGRESOS_ALMACEN:
            return ingresos_almacen_index(request)

        # salidas almacen
        if module_id == settings.MOD_SALIDAS_ALMACEN:
            return salidas_almacen_index(request)

        # movimientos almacen
        if module_id == settings.MOD_MOVIMIENTOS_ALMACEN:
            return movimientos_almacen_index(request)

        # ventas
        if module_id == settings.MOD_VENTAS:
            return ventas_index(request)

        if module_id == settings.MOD_RESERVAS:
            return reservas_index(request)

        if module_id == settings.MOD_PEDIDOS:
            return pedidos_cliente_index(request)

        # pendientes
        if module_id == settings.MOD_PENDIENTES:
            return pendientes_index(request)

        # reportes
        if module_id == settings.MOD_REPORTES:
            return reportes_index(request)

        # backup
        if module_id == settings.MOD_TABLAS_BACKUP:
            return backup(request)

        context = {
            'module_id': module_id,
        }

        return render(request, 'pages/nada.html', context)

    # cliente
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'
        usuario = {}

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    # webpush
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')

    # url_productos = settings.SUB_URL_EMPRESA
    url_productos = '/productosinicio/'
    if settings.SUB_URL_EMPRESA == 'optica':
        url_productos = '/' + settings.SUB_URL_EMPRESA + '/productosinicio/'

    # lista de lineas
    status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    lista_lineas = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_principal=1).order_by('posicion')
    listado_lineas = []
    listado_lineas_ids = ''
    for linea in lista_lineas:
        listado_lineas.append(linea)
        listado_lineas_ids += str(linea.linea_id) + ','
        # verficamos sus sublineas
        listado2 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea.linea_id).order_by('posicion')
        for linea2 in listado2:
            listado_lineas.append(linea2)
            listado_lineas_ids += str(linea2.linea_id) + ','
            # tercer nivel
            listado3 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea2.linea_id).order_by('posicion')
            for linea3 in listado3:
                listado_lineas.append(linea3)
                listado_lineas_ids += str(linea3.linea_id) + ','

    listado = []
    cant_fila = 3
    cant_actual = 0
    lista_fila = []
    contador = 0

    for linea_mostrar in listado_lineas:

        if cant_actual < cant_fila:
            dato_linea = {}
            dato_linea['linea'] = reemplazar_codigo_html(linea_mostrar.linea)
            dato_linea['linea_id'] = linea_mostrar.linea_id
            dato_linea['descripcion'] = reemplazar_codigo_html(linea_mostrar.descripcion)
            dato_linea['imagen'] = linea_mostrar.imagen
            dato_linea['imagen_thumb'] = linea_mostrar.imagen_thumb
            lista_fila.append(dato_linea)

        # aumentamos la columna
        cant_actual += 1

        if cant_actual == cant_fila:
            listado.append(lista_fila)
            cant_actual = 0
            lista_fila = []

        contador += 1

    # termina los productos
    if cant_actual > 0:
        # no termino de llenarse los datos de la fila
        for i in range(cant_actual, cant_fila):
            dato_linea = {}
            dato_linea['linea'] = ''
            dato_linea['linea_id'] = ''
            dato_linea['descripcion'] = ''
            dato_linea['imagen'] = ''
            dato_linea['imagen_thumb'] = ''
            lista_fila.append(dato_linea)

        # aniadimos a la lista principal
        listado.append(lista_fila)

    # listado de ofertas
    #productos_ofertas = []
    productos_ofertas = lista_productos(request=request, oferta='1')

    # listado de mas vendidos
    #productos_mas_vendidos = []
    productos_mas_vendidos = lista_productos(request=request, mas_vendido='1')

    # listado de novedades
    #productos_novedades = []
    productos_novedades = lista_productos(request=request, novedad='1')

    context = {
        'autenticado': autenticado,
        'cantidad_cart': cantidad_cart,
        'url_carrito': reverse('carrito'),
        'pagina_actual': 'index',
        'user': usuario,
        'vapid_key': vapid_key,
        'url_productos': url_productos,
        'lista_lineas': listado,

        'productos_ofertas': productos_ofertas,
        'productos_mas_vendidos': productos_mas_vendidos,
        'productos_novedades': productos_novedades,
    }

    return render(request, 'pages/index.html', context)


def productos_inicio(request):
    """productos de la pagina de inicio"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    url_main = reverse('productos_inicio')
    url_carrito = reverse('carrito')

    if 'showpid' in request.GET.keys():
        show_pid = request.GET['showpid'].strip()
        try:
            producto = apps.get_model('productos', 'Productos').objects.get(pk=int(show_pid))
            productos_imagenes = apps.get_model('productos', 'ProductosImagenes').objects.filter(producto_id=producto).order_by('posicion')

            context_p = {
                'imagen': productos_imagenes.first().imagen,
                'producto': producto.producto,
            }

            return render(request, 'pages/productos_solo_imagen.html', context_p)

        except Exception as ex:
            context_p = {
                'imagen': '',
                'producto': ''
            }

            return render(request, 'pages/productos_solo_imagen.html', context_p)

    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']

        if operation == 'img_producto':
            p_id = request.POST['id']
            # recuperamos la lista de imagenes
            producto = apps.get_model('productos', 'Productos').objects.get(pk=int(p_id))
            productos_imagenes = apps.get_model('productos', 'ProductosImagenes').objects.filter(producto_id=producto).order_by('posicion')

            context_p = {
                'autenticado': autenticado,
                'productos_imagenes': productos_imagenes,
            }

            return render(request, 'pages/productos_inicio_imagenes.html', context_p)

        if operation == 'add_cart':
            p_id = request.POST['producto']
            cantidad = request.POST['cantidad']
            producto = apps.get_model('productos', 'Productos').objects.get(pk=int(p_id))

            # verificamos la session
            if not 'productos_cart' in request.session.keys():
                request.session['productos_cart'] = []
                request.session.modified = True

            # verificamos si existe el producto
            existe_producto = 'no'
            nueva_cantidad = Decimal(cantidad)
            lista_session = request.session['productos_cart']
            #print('session: ', request.session['productos_cart'])

            for producto in lista_session:
                if p_id == producto['producto']:
                    existe_producto = 'si'
                    nueva_cantidad += Decimal(producto['cantidad'])
                    # actualizamos la cantidad
                    producto['cantidad'] = str(nueva_cantidad)

            # aniadimos en caso que no exista
            if existe_producto == 'no':
                dato = {}
                dato['producto'] = p_id
                dato['cantidad'] = str(nueva_cantidad)
                lista_session.append(dato)

            # actualizamos variables de session
            request.session['productos_cart'] = lista_session
            request.session.modified = True

            context_p = {
                'autenticado': autenticado,
                'cantidad_cart': len(lista_session),
                'url_carrito': reverse('carrito'),
            }

            return render(request, 'pages/productos_inicio_cart.html', context_p)

    # session
    if not 'productosinicio' in request.session.keys():
        request.session['productosinicio'] = {}
        request.session['productosinicio']['producto'] = ''
        request.session['productosinicio']['linea'] = 0

        request.session['productosinicio']['tipos_montura_select'] = ''
        request.session['productosinicio']['materiales_select'] = ''

        request.session['productosinicio']['oferta'] = '0'
        request.session['productosinicio']['mas_vendido'] = '0'
        request.session['productosinicio']['novedad'] = '0'

        # pagina
        request.session['productosinicio']['pagina'] = 1
        request.session['productosinicio']['pages_list'] = []

        request.session.modified = True

    if 'search_linea_x' in request.POST.keys():
        request.session['productosinicio']['linea'] = int(request.POST['linea'].strip())
        request.session['productosinicio']['producto'] = request.POST['producto'].strip()

        request.session['productosinicio']['tipos_montura_select'] = request.POST['tipos_montura_select'].strip()
        request.session['productosinicio']['materiales_select'] = request.POST['materiales_select'].strip()

        request.session['productosinicio']['oferta'] = request.POST['oferta'].strip()
        request.session['productosinicio']['mas_vendido'] = request.POST['mas_vendido'].strip()
        request.session['productosinicio']['novedad'] = request.POST['novedad'].strip()

        # pagina
        request.session['productosinicio']['pagina'] = 1
        request.session.modified = True

    # si seleccionana una pagina
    if 'pagina' in request.POST.keys():
        request.session['productosinicio']['pagina'] = int(request.POST['pagina'])

    # guardamos datos de session
    request.session.modified = True
    # print('session: ', request.session['productosinicio'])

    producto_busqueda = request.session['productosinicio']['producto']
    linea_id = request.session['productosinicio']['linea']
    pagina = request.session['productosinicio']['pagina']

    # lista de productos por proveedor y linea
    status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    lista_lineas_aux = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_principal=1).order_by('posicion')
    # linea1
    linea1 = lista_lineas_aux.first()
    lista_lineas = []
    lista_lineas_ids = ''
    for linea in lista_lineas_aux:
        linea_obj = {}
        linea_obj['linea_id'] = linea.linea_id
        linea_obj['linea'] = linea.linea
        linea_obj['espacios'] = ''
        lista_lineas.append(linea_obj)
        lista_lineas_ids += str(linea.linea_id) + ','

        # verificamos si tiene lineas inferiores
        lineas_inf1 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea.linea_id).order_by('posicion')

        for linea_dato_inf1 in lineas_inf1:
            linea_obj = {}
            linea_obj['linea_id'] = linea_dato_inf1.linea_id
            linea_obj['linea'] = linea_dato_inf1.linea
            linea_obj['espacios'] = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
            lista_lineas.append(linea_obj)
            lista_lineas_ids += str(linea_dato_inf1.linea_id) + ','

            # verificamos lineas inferiores nivel2
            lineas_inf2 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea_dato_inf1.linea_id).order_by('posicion')
            for linea_dato_inf2 in lineas_inf2:
                linea_obj2 = {}
                linea_obj2['linea_id'] = linea_dato_inf2.linea_id
                linea_obj2['linea'] = linea_dato_inf2.linea
                linea_obj2['espacios'] = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' * 2
                lista_lineas.append(linea_obj2)
                lista_lineas_ids += str(linea_dato_inf2.linea_id) + ','

                # verificamos lineas inferiores nivel3
                lineas_inf3 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea_dato_inf2.linea_id).order_by('posicion')
                for linea_dato_inf3 in lineas_inf3:
                    linea_obj3 = {}
                    linea_obj3['linea_id'] = linea_dato_inf3.linea_id
                    linea_obj3['linea'] = linea_dato_inf3.linea
                    linea_obj3['espacios'] = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' * 3
                    lista_lineas.append(linea_obj3)
                    lista_lineas_ids += str(linea_dato_inf3.linea_id) + ','

    # descripcion del producto
    txt_producto = ''
    if len(lista_lineas_ids) > 0:
        lista_lineas_ids = lista_lineas_ids[0:len(lista_lineas_ids)-1]

    tipos_montura_select = request.session['productosinicio']['tipos_montura_select']
    materiales_select = request.session['productosinicio']['materiales_select']
    oferta = request.session['productosinicio']['oferta']
    mas_vendido = request.session['productosinicio']['mas_vendido']
    novedad = request.session['productosinicio']['novedad']

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    # detalle del producto
    if 'id' in request.GET.keys() and 'producto' in request.GET.keys():
        p_id = request.GET['id']
        # recuperamos datos del producto y sus imagenes
        producto_aux = apps.get_model('productos', 'Productos').objects.get(pk=int(p_id))
        productos_imagenes = apps.get_model('productos', 'ProductosImagenes').objects.filter(producto_id=producto_aux).order_by('posicion')

        producto = {}
        producto['producto_id'] = producto_aux.producto_id
        producto['producto'] = reemplazar_codigo_html(producto_aux.producto)
        producto['codigo'] = producto_aux.codigo

        producto['descripcion'] = reemplazar_codigo_html(producto_aux.descripcion1)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion2)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion3)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion4)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion5)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion6)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion7)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion8)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion9)
        producto['descripcion'] += ' ' + reemplazar_codigo_html(producto_aux.descripcion10)
        producto['descripcion'] = producto['descripcion'].strip()

        producto['descripcion1'] = reemplazar_codigo_html(producto_aux.descripcion1)
        producto['descripcion2'] = reemplazar_codigo_html(producto_aux.descripcion2)
        producto['descripcion3'] = reemplazar_codigo_html(producto_aux.descripcion3)
        producto['descripcion4'] = reemplazar_codigo_html(producto_aux.descripcion4)
        producto['descripcion5'] = reemplazar_codigo_html(producto_aux.descripcion5)
        producto['descripcion6'] = reemplazar_codigo_html(producto_aux.descripcion6)
        producto['descripcion7'] = reemplazar_codigo_html(producto_aux.descripcion7)
        producto['descripcion8'] = reemplazar_codigo_html(producto_aux.descripcion8)
        producto['descripcion9'] = reemplazar_codigo_html(producto_aux.descripcion9)
        producto['descripcion10'] = reemplazar_codigo_html(producto_aux.descripcion10)

        producto['precio'] = producto_aux.precio
        producto['oferta'] = producto_aux.oferta
        producto['precio_oferta'] = producto_aux.precio_oferta

        imagen1 = ''
        if productos_imagenes:
            primera = productos_imagenes.first()
            imagen1 = primera.imagen

        # productos relacionados
        lista_relacionados = apps.get_model('productos', 'ProductosRelacionados').objects.filter(producto_id=producto_aux).order_by('producto_id__producto')

        # listado de retorno
        listado = []
        cant_fila = 3
        cant_actual = 0
        lista_fila = []
        contador = 0

        for producto_r in lista_relacionados:
            #print('producto: ', producto_r.producto_relacion_id.tallas)

            if cant_actual < cant_fila:
                dato_producto = {}
                dato_producto['linea'] = producto_r.producto_relacion_id.linea_id.linea
                dato_producto['producto'] = reemplazar_codigo_html(producto_r.producto_relacion_id.producto)
                dato_producto['codigo'] = producto_r.producto_relacion_id.codigo
                dato_producto['precio'] = producto_r.producto_relacion_id.precio
                dato_producto['producto_id'] = producto_r.producto_relacion_id.producto_id

                dato_producto['tipo_montura_id'] = producto_r.producto_relacion_id.tipo_montura_id
                dato_producto['material_id'] = producto_r.producto_relacion_id.material_id
                dato_producto['novedad'] = producto_r.producto_relacion_id.novedad
                dato_producto['mas_vendido'] = producto_r.producto_relacion_id.mas_vendido
                dato_producto['oferta'] = producto_r.producto_relacion_id.oferta
                dato_producto['precio_oferta'] = producto_r.producto_relacion_id.precio_oferta

                pi_relacion = apps.get_model('productos', 'ProductosImagenes').objects.filter(producto_id=producto_r.producto_relacion_id).order_by('posicion')
                if pi_relacion:
                    primera_imagen = pi_relacion.first()
                    dato_producto['imagen'] = primera_imagen.imagen
                    dato_producto['imagen_thumb'] = primera_imagen.imagen_thumb
                else:
                    dato_producto['imagen'] = ''
                    dato_producto['imagen_thumb'] = ''

                lista_fila.append(dato_producto)

            # aumentamos la columna
            cant_actual += 1

            if cant_actual == cant_fila:
                listado.append(lista_fila)
                cant_actual = 0
                lista_fila = []

            contador += 1

        # termina los productos
        if cant_actual > 0:
            # no termino de llenarse los datos de la fila
            for i in range(cant_actual, cant_fila):
                dato_producto = {}
                dato_producto['linea'] = ''
                dato_producto['producto'] = ''
                dato_producto['codigo'] = ''
                dato_producto['precio'] = 0
                dato_producto['producto_id'] = 0
                dato_producto['imagen'] = ''
                dato_producto['imagen_thumb'] = ''
                lista_fila.append(dato_producto)

            # aniadimos a la lista principal
            listado.append(lista_fila)

        # devolvemos los productos
        # return listado

        context_p = {
            'detalle_producto': 1,

            'autenticado': autenticado,
            'url_main': url_main,
            'url_carrito': url_carrito,
            'url_index': reverse('index'),
            'cantidad_cart': cantidad_cart,

            'productos_relacionados': listado,

            'producto': producto,
            'imagen1': imagen1,
            'productos_imagenes': productos_imagenes,
        }

        return render(request, 'pages/productos_inicio_detalle.html', context_p)

    if producto_busqueda == '':
        if linea_id == 0:
            lista_pro = lista_productos(request, linea_id=linea1.linea_id, producto_nombre='', oferta=oferta, mas_vendido=mas_vendido, novedad=novedad,
                                        tipo_montura=tipos_montura_select, material=materiales_select)
            # txt_producto = linea1.proveedor_id.proveedor + ' - ' + linea1.linea
            txt_producto = '<span class="link_lineas pointer" onclick="paginaInicio();">Inicio</span>' + link_linea(linea1.linea_id)
        else:
            lista_pro = lista_productos(request, linea_id=linea_id, producto_nombre='', oferta=oferta, mas_vendido=mas_vendido, novedad=novedad, tipo_montura=tipos_montura_select,
                                        material=materiales_select)
            linea_actual = apps.get_model('configuraciones', 'Lineas').objects.get(pk=int(linea_id))
            #txt_producto = linea_actual.proveedor_id.proveedor + ' - ' + linea_actual.linea
            txt_producto = '<span class="link_lineas pointer" onclick="paginaInicio();">Inicio</span>' + link_linea(linea_actual.linea_id)
    else:
        lista_pro = lista_productos(request, linea_id=0, producto_nombre=producto_busqueda, oferta=oferta, mas_vendido=mas_vendido, novedad=novedad,
                                    tipo_montura=tipos_montura_select, material=materiales_select)
        txt_producto = '<span class="link_lineas pointer" onclick="paginaInicio();">Inicio</span>' + ' / ' + producto_busqueda

    # listado por defecto
    lista_tipos_montura_select = get_lista_session(request.session['productosinicio']['tipos_montura_select'])
    lista_materiales_select = get_lista_session(request.session['productosinicio']['materiales_select'])

    color_borde_resaltado = '#46107F'
    color_borde_normal = '#FFFFFF'

    p_lista_tipos_montura = ''
    p_lista_materiales = ''

    # tipos de montura
    # de la funcion buscar_producto, utils.py
    lista_tipos_montura = request.session['productosinicio']['lista_tipos_montura']

    # materiales
    # de la funcion buscar_producto, utils.py
    lista_materiales = request.session['productosinicio']['lista_materiales']

    # ajax para la busqueda de productos
    # si no viene del index
    if 'from_index' not in request.POST.keys():
        if 'search_producto_x' in request.POST.keys() or 'search_linea_x' in request.POST.keys() or 'pagina' in request.POST.keys():
            context2 = {
                'autenticado': autenticado,
                'lista_lineas': lista_lineas,
                'lista_lineas_ids': lista_lineas_ids,
                'listado_productos': lista_pro,

                'lista_tipos_montura': lista_tipos_montura,
                'lista_materiales': lista_materiales,

                'oferta': oferta,
                'mas_vendido': mas_vendido,
                'novedad': novedad,

                'color_borde_normal': color_borde_normal,
                'color_borde_resaltado': color_borde_resaltado,

                'tipos_montura_select': tipos_montura_select,
                'materiales_select': materiales_select,

                'linea_session': request.session['productosinicio']['linea'],
                'producto_session': request.session['productosinicio']['producto'],
                'url_main': url_main,
                'url_carrito': url_carrito,
                'url_index': reverse('index'),
                'pages_list': request.session['productosinicio']['pages_list'],
                'pagina_actual': request.session['productosinicio']['pagina'],
                'cantidad_cart': cantidad_cart,
                'txt_producto': txt_producto,
            }

            if 'parte_form' in request.POST.keys():
                # de javascript, parte superior de busqueda o listado
                parte_form = request.POST['parte_form'].strip()
                if parte_form == 'superior':
                    return render(request, 'pages/productos_inicio_superior.html', context2)

            return render(request, 'pages/productos_inicio_listado.html', context2)

    # datos por defecto productosinicio
    # datos por defecto productosinicio
    context = {
        'autenticado': autenticado,
        'lista_lineas': lista_lineas,
        'lista_lineas_ids': lista_lineas_ids,
        'listado_productos': lista_pro,

        'lista_tipos_montura': lista_tipos_montura,
        'lista_materiales': lista_materiales,

        # 'p_lista_tipos_montura': p_lista_tipos_montura,
        # 'p_lista_materiales': p_lista_materiales,

        'oferta': oferta,
        'mas_vendido': mas_vendido,
        'novedad': novedad,

        'color_borde_normal': color_borde_normal,
        'color_borde_resaltado': color_borde_resaltado,

        'tipos_montura_select': lista_tipos_montura_select,
        'materiales_select': lista_materiales_select,

        'linea_session': request.session['productosinicio']['linea'],
        'producto_session': request.session['productosinicio']['producto'],
        'url_main': url_main,
        'url_carrito': url_carrito,
        'url_index': reverse('index'),
        'pages_list': request.session['productosinicio']['pages_list'],
        'pagina_actual': request.session['productosinicio']['pagina'],
        'cantidad_cart': cantidad_cart,
        'txt_producto': txt_producto,
    }

    return render(request, 'pages/productos_inicio.html', context)


def without_permission(request):
    return render(request, 'pages/without_permission.html')


def internal_error(request):
    context = {
        'error': request.session['internal_error'],
    }
    return render(request, 'pages/internal_error.html', context)


def sucursales_empresa(request):
    """sucursales de la empresa"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    context = {
        'autenticado': autenticado,
        'cantidad_cart': cantidad_cart,
        'url_carrito': reverse('carrito'),
    }

    return render(request, 'pages/sucursales_empresa.html', context)


def acerca_de(request):
    """acerca la empresa"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    context = {
        'autenticado': autenticado,
        'cantidad_cart': cantidad_cart,
        'url_carrito': reverse('carrito'),
    }

    return render(request, 'pages/acerca_de.html', context)


def materiales_home(request):
    """acerca la empresa"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    context = {
        'autenticado': autenticado,
        'cantidad_cart': cantidad_cart,
        'url_carrito': reverse('carrito'),
        'pagina_actual': 'materiales',
    }

    return render(request, 'pages/materiales.html', context)


def disenios_home(request):
    """acerca la empresa"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    context = {
        'autenticado': autenticado,
        'cantidad_cart': cantidad_cart,
        'url_carrito': reverse('carrito'),
        'pagina_actual': 'disenio_lentes',
    }

    return render(request, 'pages/disenios.html', context)


def contactenos(request):
    """formulario de contacto"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    url_main = reverse('contactenos')

    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if operation == 'contacto':
            error = 0
            try:
                nombres = request.POST['nombres'].strip()
                apellidos = request.POST['apellidos'].strip()
                telefonos = request.POST['telefonos'].strip()
                email_cliente = request.POST['email'].strip()
                mensaje = request.POST['mensaje'].strip()

                # Import the email modules we'll need
                from email.message import EmailMessage

                # Create a text/plain message
                separador = "\n"
                email_content = f"Mensaje: {separador}Nombre: {apellidos} {nombres}{separador}Fonos: {telefonos}{separador}Email: {email_cliente}{separador}Mensaje: {mensaje}"
                msg = EmailMessage()
                msg.set_content(email_content)

                # me == the sender's email address
                # you == the recipient's email address
                msg['Subject'] = 'Optica Ideal - mensaje'
                msg['From'] = settings.EMAIL_CONTACT_FROM
                # msg['To'] = settings.EMAIL_CONTACT_TO
                msg['To'] = 'acc.claros@gmail.com, alan_claros13@hotmail.com'

                # Send the message via our own SMTP server.
                s = smtplib.SMTP(settings.EMAIL_SERVER_NAME)
                s.send_message(msg)
                s.quit()

            except Exception as e:
                print('Error al enviar el mensaje: ' + str(e))
                error = 1

            context_p = {
                'autenticado': autenticado,
                'error': error,
            }

            return render(request, 'pages/contactenos_mail.html', context_p)

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    context = {
        'autenticado': autenticado,
        'url_main': url_main,
        'cantidad_cart': cantidad_cart,
        'url_carrito': reverse('carrito'),
    }

    return render(request, 'pages/contactenos.html', context)


# cambio de password
def cambiar_password(request):
    """cambio de password de los usuarios"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'
        url_d = reverse('without_permission')
        return HttpResponseRedirect(url_d)

    # por defecto
    usuario_actual = User.objects.get(pk=request.user.id)

    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        # busqueda cliente por ci
        if operation == 'add':
            # verificamos
            error = 0
            password = request.POST['actual'].strip()
            nuevo = request.POST['nuevo'].strip()
            nuevo2 = request.POST['nuevo2'].strip()

            if error == 0 and nuevo == '' and nuevo2 == '':
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'Debe llenar su nuevo password y su repeticion'})

            if error == 0 and not check_password(password, usuario_actual.password):
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'Error en su password'})

            if error == 0 and nuevo != nuevo2:
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'La repeticion de su password no coincide'})

            if error == 0 and len(nuevo) < 6:
                error = 1
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Usuario!', 'description': 'Su nuevo password debe tener al menos 6 letras'})

            if error == 0:
                # actualizamos
                usuario_actual.password = make_password(nuevo)
                usuario_actual.save()
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Usuario!', 'description': 'Su nuevo password se cambio correctamente'})

    context = {
        'autenticado': autenticado,
        'usuario_actual': usuario_actual,
        'module_x': 1000,
    }

    return render(request, 'pages/cambiar_password.html', context)


# carrito de compras
def carrito(request):
    """carrito de compras"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']

        # buscar cupon
        if operation == 'buscar_cupon':
            cupon_id = 0
            porcentaje_descuento = 0
            status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
            try:
                # print('empieza...')
                cupon_txt = request.POST['cupon'].strip()
                #print('cupon_tt: ', cupon_txt)
                cupon_search = apps.get_model('configuraciones', 'Cupones').objects.filter(status_id=status_activo, cupon=cupon_txt)
                #print('cupon search: ', cupon_search)
                if cupon_search:
                    cupon = cupon_search.first()
                    cupon_id = cupon.cupon_id
                    porcentaje_descuento = cupon.porcentaje_descuento

            except Exception as ex:
                cupon_id = 0
                porcentaje_descuento = 0

            context = {
                'cupon_id': cupon_id,
                'porcentaje_descuento': porcentaje_descuento,
                'autenticado': 'si',
            }

            return render(request, 'ventas/cupon.html', context)

        if operation == 'buscar_ci':
            ci_cliente = request.POST['ci'].strip()
            apellidos = ''
            nombres = ''
            telefonos = ''
            direccion = ''
            email = ''
            try:
                busqueda_cliente = apps.get_model('clientes', 'Clientes').objects.filter(ci_nit=ci_cliente)

                if busqueda_cliente:
                    cliente = busqueda_cliente.first()
                    apellidos = cliente.apellidos
                    nombres = cliente.nombres
                    telefonos = cliente.telefonos
                    direccion = cliente.direccion
                    email = cliente.email
            except Exception as ex:
                print('error al buscar CI')

            context = {
                'autenticado': autenticado,
                'apellidos': apellidos,
                'nombres': nombres,
                'telefonos': telefonos,
                'direccion': direccion,
                'email': email,
            }

            return render(request, 'pages/busqueda_ci_cliente.html', context)

        # eliminacion de un producto
        if operation == 'delete':
            p_id = request.POST['producto']
            lista = request.session['productos_cart']
            nueva_lista = []
            for articulo in lista:
                if p_id != articulo['producto']:
                    nueva_lista.append(articulo)

            request.session['productos_cart'] = nueva_lista
            request.session.modified = True

        # realizar pedido
        if operation == 'realizar_pedido':
            try:
                ci = request.POST['ci'].strip()
                nombres = request.POST['nombres'].strip()
                apellidos = request.POST['apellidos'].strip()
                telefonos = request.POST['telefonos'].strip()
                direccion = request.POST['direccion'].strip()
                email = request.POST['email'].strip()
                mensaje = request.POST['mensaje'].strip()

                tipo_pedido = request.POST['tipo_pedido']
                lista_ids = request.POST['lista_productos_ids'].strip()
                lista_cantidad = request.POST['lista_cantidad'].strip()

                cupon = request.POST['cupon'].strip()
                cupon_id = request.POST['cupon_id'].strip()
                porcentaje_descuento = request.POST['porcentaje_descuento'].strip()

                # creamos o actualizamos datos del cliente
                status_activo = apps.get_model('status', 'Status').objects.get(pk=1)

                cliente_search = apps.get_model('clientes', 'Clientes').objects.filter(ci_nit=ci, status_id=status_activo)
                if cliente_search:
                    cliente = cliente_search.first()
                    cliente.nombres = nombres
                    cliente.apellidos = apellidos
                    cliente.telefonos = telefonos
                    cliente.direccion = direccion
                    cliente.email = email
                    cliente.save()
                else:
                    usuario = User.objects.get(pk=1)
                    usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario)
                    punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=usuario_perfil.punto_id)

                    cliente = apps.get_model('clientes', 'Clientes').objects.create(status_id=status_activo, user_perfil_id=usuario_perfil, punto_id=punto, ci_nit=ci, apellidos=apellidos,
                                                                                    nombres=nombres, telefonos=telefonos, direccion=direccion, email=email, razon_social=apellidos, factura_a=apellidos, created_at='now', updated_at='now')
                    cliente.save()

                cliente_id = cliente.cliente_id

                error = 0
                total_pedido = 0

                if lista_cantidad == '':
                    error = 1
                else:
                    # creamos el pedido
                    pedido = apps.get_model('pedidos', 'Pedidos').objects.create(ci_nit=ci, cliente_id=cliente_id, apellidos=apellidos, nombres=nombres, telefonos=telefonos, direccion=direccion, email=email,
                                                                                 mensaje=mensaje, tipo_pedido=tipo_pedido, status_id=status_activo, created_at='now', updated_at='now')
                    pedido.save()
                    total_pedido = 0
                    # datos del cupon
                    porcentaje_descuento = 0
                    cupon = ''
                    #print('cupon_id: ', cupon_id)
                    if cupon_id != '' and cupon_id != '0':
                        cupon_db = apps.get_model('configuraciones', 'Cupones').objects.get(pk=int(cupon_id), status_id=status_activo)
                        porcentaje_descuento = cupon_db.porcentaje_descuento
                        cupon = cupon_db.cupon
                    else:
                        cupon_id = 0

                    # detalles
                    division_ids = lista_ids.split('|')
                    division_cant = lista_cantidad.split('|')
                    #print('division: ', division_ids)

                    for i in range(0, len(division_ids)):
                        p_id = division_ids[i]
                        cant = division_cant[i]

                        producto = apps.get_model('productos', 'Productos').objects.get(pk=int(p_id))
                        cantidad = Decimal(cant)
                        costo = producto.precio_oferta if producto.oferta == 1 else producto.precio
                        total_detalle = cantidad * costo

                        pedido_detalle = apps.get_model('pedidos', 'PedidosDetalles').objects.create(pedido_id=pedido, status_id=status_activo,
                                                                                                     producto_id=producto, cantidad=cantidad, costo=costo, descuento=0, porcentaje_descuento=0, total=total_detalle)
                        pedido_detalle.save()
                        total_pedido += pedido_detalle.total

                    # vemos si hay descuento
                    if porcentaje_descuento > 0:
                        descuento = total_pedido * (porcentaje_descuento/100)
                        total_venta = total_pedido - descuento
                    else:
                        descuento = 0
                        total_venta = total_pedido

                    pedido.subtotal = total_pedido
                    pedido.descuento = descuento
                    pedido.porcentaje_descuento = porcentaje_descuento
                    pedido.cupon_id = int(cupon_id)
                    pedido.cupon = cupon
                    pedido.total = total_venta
                    pedido.save()

                    # borramos la session
                    request.session['productos_cart'] = []
                    request.session.modified = True

                context = {
                    'autenticado': autenticado,
                    'total_pedido': total_pedido,
                    'url_carrito': reverse('carrito'),
                    'error': error,
                }

                return render(request, 'pages/carrito_compras_resultado.html', context)

            except Exception as ex:
                print('error: ', str(ex))
                context = {
                    'autenticado': autenticado,
                    'total_pedido': 0,
                    'url_carrito': reverse('carrito'),
                    'error': 1,
                }

                return render(request, 'pages/carrito_compras_resultado.html', context)

    # carrito de compras
    cantidad_cart = 0
    lista_productos = []
    total_pedido = 0
    lista_ids = ''

    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])
        lista = request.session['productos_cart']
        for articulo in lista:
            #print('articulo: ', articulo)
            producto = apps.get_model('productos', 'Productos').objects.get(pk=int(articulo['producto']))
            cantidad = articulo['cantidad']
            lista_ids += str(producto.producto_id)+';'

            dato = {}
            dato['producto'] = producto.producto
            dato['producto_id'] = producto.producto_id
            dato['cantidad'] = cantidad
            precio = producto.precio_oferta if producto.oferta == 1 else producto.precio
            dato['precio'] = precio
            total = round(Decimal(cantidad) * precio, 2)

            dato['total'] = total
            total_pedido += total

            lista_productos.append(dato)

        if len(lista_ids) > 0:
            lista_ids = lista_ids[0: len(lista_ids)-1]

    #print('lista prod: ', lista_productos)
    # webpush
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')

    # usuarios para la notificacion
    status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    usuarios_notificacion = apps.get_model('permisos', 'UsersPerfiles').objects.filter(status_id=status_activo, notificacion=1).order_by('user_perfil_id')
    lista_notificacion = ''
    for usuario_notif in usuarios_notificacion:
        lista_notificacion += str(usuario_notif.user_id.id) + '|'

    if len(lista_notificacion) > 0:
        lista_notificacion = lista_notificacion[0:len(lista_notificacion)-1]

    url_push = settings.SUB_URL_EMPRESA
    if url_push == 'pvi':
        url_push = '/send_push'
    else:
        url_push = '/' + settings.SUB_URL_EMPRESA + '/send_push'

    context = {
        'autenticado': autenticado,
        'cantidad_cart': cantidad_cart,
        'lista_productos': lista_productos,
        'total_pedido': total_pedido,
        'url_carrito': reverse('carrito'),
        'url_webpush': url_push,
        'lista_ids': lista_ids,
        'lista_notificacion': lista_notificacion,
        'vapid_key': vapid_key,
        'vender_fracciones': 'no',
    }

    return render(request, 'pages/carrito_compras.html', context)


# notificaciones para el usuario
def notificaciones_pagina(request):
    url_pedidos_cliente = reverse('index')
    url_reservas = reverse('index')

    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    if autenticado == 'no':
        context = {
            'cantidad': 0,
            'cantidad_rojos': 0,
            'notificaciones': {},
            'autenticado': autenticado,
        }
        return render(request, 'pages/notificaciones_pagina.html', context)

    try:
        user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
        punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)

        # lista de puntos y sucursales
        estado_activo = 1

        # datos para las consultas
        fecha_actual = get_date_system()
        fecha1 = get_date_to_db(fecha=fecha_actual, formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss')
        fecha2 = get_date_to_db(fecha=fecha_actual, formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

        notificaciones = []
        cantidad = 0
        cantidad_danger = 0
        cantidad_warning = 0

        # lista pedidos
        sql = "SELECT p.pedido_id, p.apellidos, p.nombres, p.total, p.created_at AS fecha FROM pedidos p "
        sql += f"WHERE p.status_id='{estado_activo}' ORDER BY p.created_at "
        #print('sql: ', sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                cantidad += 1
                cantidad_danger += 1
                dato = {}
                dato['tipo'] = 'pedido'
                dato['tipo_notificacion'] = 'danger'
                fecha = get_date_show(fecha=row[4], formato='dd-MMM-yyyy HH:ii', formato_ori='yyyy-mm-dd HH:ii:ss')

                cliente = ""
                if row[2] and row[2].strip() != '':
                    cliente += row[2].strip()[0:1] + '.'

                if row[1] and row[1].strip() != '':
                    cliente += row[1].strip()[0:1] + '.'

                dato['descripcion'] = fecha + ', ' + cliente + ', ' + str(row[3]) + 'Bs.'
                dato['url'] = url_pedidos_cliente
                notificaciones.append(dato)

        # lista de RESERVAS
        estado_preventa = settings.STATUS_PREVENTA
        sql = f"SELECT r.reserva_id, r.nombres, r.apellidos, r.fecha_inicio FROM reservas r WHERE r.status_id='{estado_preventa}' "
        sql += "ORDER BY r.fecha_inicio "
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                cantidad += 1
                cantidad_warning += 1
                dato = {}
                dato['tipo'] = 'reserva'
                dato['tipo_notificacion'] = 'warning'
                fecha = get_date_show(fecha=row[3], formato='dd-MMM-yyyy HH:ii', formato_ori='yyyy-mm-dd HH:ii:ss')

                cliente = ""
                if row[1] and row[1].strip() != '':
                    cliente += row[1].strip() + ' '

                if row[2] and row[2].strip() != '':
                    cliente += row[2].strip()[0:1] + '.'

                dato['descripcion'] = fecha + ', ' + cliente
                dato['url'] = url_reservas
                notificaciones.append(dato)

        # context para el html
        context = {
            'notificaciones': notificaciones,
            'cantidad': cantidad,
            'cantidad_danger': cantidad_danger,
            'autenticado': autenticado,
        }

        return render(request, 'pages/notificaciones_pagina.html', context)

    except Exception as e:
        print('ERROR ' + str(e))
        context = {
            'cantidad': 0,
            'cantidad_danger': 0,
            'notificaciones': {},
            'autenticado': autenticado,
        }
        return render(request, 'pages/notificaciones_pagina.html', context)


def privacy_policy(request):
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    context = {
        'autenticado': autenticado,
    }
    return render(request, 'pages/privacy_policy.html', context)


def refund_policy(request):
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    context = {
        'autenticado': autenticado,
    }
    return render(request, 'pages/refund_policy.html', context)


def terms_service(request):
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    context = {
        'autenticado': autenticado,
    }
    return render(request, 'pages/terms_service.html', context)


def delivery_policy(request):
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    context = {
        'autenticado': autenticado,
    }
    return render(request, 'pages/delivery_policy.html', context)


def faqs(request):
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    context = {
        'autenticado': autenticado,
    }
    return render(request, 'pages/faqs.html', context)


def frecuency_partners(request):
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    context = {
        'autenticado': autenticado,
    }
    return render(request, 'pages/frequency_partners.html', context)


def backup(request):
    """backup"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'
        return render(request, 'pages/without_permission.html')

    if not get_user_permission_operation(request.user, settings.MOD_TABLAS_BACKUP, 'lista'):
        return render(request, 'pages/without_permission.html')

    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        lista_tablas = [['auth', 'User', 'auth_user'],
                        ['status', 'Status', 'status'],

                        ['permisos', 'Perfiles', 'perfiles'],
                        ['permisos', 'Modulos', 'modulos'],
                        ['permisos', 'UsersPerfiles', 'users_perfiles'],
                        ['permisos', 'UsersModulos', 'users_modulos'],

                        ['configuraciones', 'Configuraciones', 'configuraciones'],
                        ['configuraciones', 'Paises', 'paises'],
                        ['configuraciones', 'Ciudades', 'ciudades'],
                        ['configuraciones', 'Sucursales', 'sucursales'],
                        ['configuraciones', 'Puntos', 'puntos'],
                        ['configuraciones', 'TiposMonedas', 'tipos_monedas'],
                        ['configuraciones', 'Monedas', 'monedas'],
                        ['configuraciones', 'Cajas', 'cajas'],
                        ['configuraciones', 'Almacenes', 'almacenes'],
                        ['configuraciones', 'Lineas', 'lineas'],
                        ['configuraciones', 'PuntosAlmacenes', 'puntos_almacenes'],
                        ['configuraciones', 'Proveedores', 'proveedores'],
                        ['configuraciones', 'Materiales', 'materiales'],
                        ['configuraciones', 'TiposMontura', 'tipos_montura'],
                        ['configuraciones', 'Laboratorios', 'laboratorios'],
                        ['configuraciones', 'Tecnicos', 'tecnicos'],
                        ['configuraciones', 'Oftalmologos', 'oftalmologos'],
                        ['configuraciones', 'Cupones', 'cupones'],

                        ['cajas', 'CajasIngresos', 'cajas_ingresos'],
                        ['cajas', 'CajasEgresos', 'cajas_egresos'],
                        ['cajas', 'CajasOperaciones', 'cajas_operaciones'],
                        ['cajas', 'CajasOperacionesDetalles', 'cajas_operaciones_detalles'],
                        ['cajas', 'CajasMovimientos', 'cajas_movimientos'],

                        ['clientes', 'Clientes', 'clientes'],

                        ['productos', 'Productos', 'productos'],
                        ['productos', 'ProductosTiposMontura', 'productos_tipos_montura'],
                        ['productos', 'ProductosMateriales', 'productos_materiales'],
                        ['productos', 'ProductosImagenes', 'productos_imagenes'],
                        ['productos', 'ProductosRelacionados', 'productos_relacionados'],

                        ['inventarios', 'Registros', 'registros'],
                        ['inventarios', 'RegistrosDetalles', 'registros_detalles'],
                        ['inventarios', 'Stock', 'stock'],

                        ['ventas', 'Ventas', 'ventas'],
                        ['ventas', 'VentasDetalles', 'ventas_detalles'],
                        ['ventas', 'VentasImagenes', 'ventas_imagenes'],
                        ['ventas', 'Dosificaciones', 'dosificaciones'],
                        ['ventas', 'Facturas', 'facturas'],
                        ['ventas', 'PlanPagos', 'plan_pagos'],
                        ['ventas', 'PlanPagosDetalles', 'plan_pagos_detalles'],
                        ['ventas', 'PlanPagosPagos', 'plan_pagos_pagos'],
                        
                        ['pedidos', 'Pedidos', 'pedidos'],
                        ['pedidos', 'PedidosDetalles', 'pedidos_detalles'],
                        
                        ['reservas', 'ReservasDias', 'reservas_dias'],
                        ['reservas', 'ReservasHoras', 'reservas_horas'],
                        ['reservas', 'Reservas', 'reservas'],
                        ]

        if operation == 'add':
            # leemos las tablas y realizamos la copia
            wb = openpyxl.Workbook()
            # creamos las hojas
            for tabla in lista_tablas:
                ws = wb.create_sheet(tabla[2])
                modelo = apps.get_model(tabla[0], tabla[1])

                # print('modelo...: ', modelo)
                # for field in modelo._meta.fields:
                #     columna = field.get_attname_column()
                #     print('columna: ', columna)

                #columna = modelo._meta.get_field(arg)
                #ws.append(('111', '22222'))

                # columnas = modelo._meta.fields
                # print('columnas...: ', len(columnas))

                aux_columnas = modelo._meta.fields
                len_columnas = len(aux_columnas)

                lista_filas = []
                lista_select = ''
                for field in modelo._meta.fields:
                    #columna = field[1]
                    #print('columna: ', columna)
                    columna = field.get_attname_column()
                    nombre_columna = columna[1]
                    lista_filas.append(nombre_columna)
                    lista_select += nombre_columna + ','

                if len(lista_select) > 0:
                    lista_select = lista_select[0:len(lista_select)-1]

                # titulos columnas
                ws.append(lista_filas)

                # datos
                nombre_tabla = tabla[2]
                sql = f"SELECT {lista_select} FROM {nombre_tabla} "
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    for row in rows:
                        fila = []
                        for i in range(len_columnas):
                            #print('i...: ', i)
                            fila.append(row[i])

                        # aniadimos la fila
                        ws.append(fila)

            # response = HttpResponse(content_type="application/msexcel")
            # response["Content-Disposition"] = "attachment; filename=backup.xlsx"
            # wb.save(response)
            # return response
            ruta_settings = settings.STATICFILES_DIRS[0]
            ruta_guardar = os.path.join(ruta_settings, 'img', 'files_download', 'backup.xlsx')
            loczip = os.path.join(ruta_settings, 'img', 'files_download', 'backup.zip')

            # eliminamos archivos si es que existen
            if os.path.isfile(ruta_guardar):
                os.unlink(ruta_guardar)
            if os.path.isfile(loczip):
                os.unlink(loczip)

            wb.save(ruta_guardar)
            wb.close()

            zip = zipfile.ZipFile(loczip, "w")
            # con path
            # zip.write(ruta_guardar)
            # quitando el path
            zip.write(ruta_guardar, os.path.basename(ruta_guardar))
            zip.close()

            zip_file = open(loczip, 'rb')
            return FileResponse(zip_file)

            # print('zip fileee....: ', zip_file)
            # response = HttpResponse(zip_file, content_type='application/force-download')
            # print('response...: ', response)
            # response['Content-Disposition'] = 'attachment; filename="%s"' % 'backup.zip'
            # return response

    context = {
        'autenticado': autenticado,
        'url_main': '',
        'module_x': settings.MOD_TABLAS_BACKUP,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    return render(request, 'pages/backup.html', context)


def reserva(request):
    """reserva"""
    usuario = request.user
    id_usuario = usuario.id
    if id_usuario:
        autenticado = 'si'
    else:
        autenticado = 'no'

    # registro de reserva
    if 'add_reserva' in request.POST.keys():
        error = 0
        fecha_mostrar = ''
        try:
            nombres = request.POST['nombres'].strip()
            apellidos = request.POST['apellidos'].strip()
            telefonos = request.POST['telefonos'].strip()
            mensaje = request.POST['mensaje'].strip()
            aux_dia = request.POST['dia'].strip()
            dia = aux_dia if len(aux_dia) == 2 else '0' + aux_dia
            dia_semana = request.POST['dia_semana'].strip()
            hora = request.POST['hora'].strip()
            periodo = request.POST['periodo'].strip()

            reserva_dia = apps.get_model('reservas', 'ReservasDias').objects.get(pk=int(dia_semana))
            reserva_hora = apps.get_model('reservas', 'ReservasHoras').objects.get(pk=int(hora))
            status_preventa = apps.get_model('status', 'Status').objects.get(pk=settings.STATUS_PREVENTA)

            fecha_inicio = fecha_periodo(periodo, dia) + ' ' + reserva_hora.hora + ':00'
            fecha_mostrar = get_date_show(fecha=fecha_inicio, formato_ori='yyyy-mm-dd HH:ii:ss', formato='dd-MMM-yyyy HH:ii')

            reserva = apps.get_model('reservas', 'Reservas').objects.create(
                nombres=nombres, apellidos=apellidos, telefonos=telefonos, mensaje=mensaje,
                reserva_dia_id=reserva_dia, reserva_hora_id=reserva_hora, status_id=status_preventa,
                fecha_inicio=fecha_inicio, fecha_fin=fecha_inicio,
                created_at='now', updated_at='now'
            )
            reserva.save()

        except Exception as ex:
            print('ERROR reserva: ', str(ex))
            error = 1

        context = {
            'error': error,
            'fecha_mostrar': fecha_mostrar,
            'dia': aux_dia,
        }

        return render(request, 'pages/reserva_respuesta.html', context)

    # busqueda de nuevo mes
    if 'search_periodo' in request.POST.keys():
        periodo = request.POST['search_periodo'].strip()
        anio = periodo[0:4]
        mes = periodo[4:6]

        periodo_next = next_periodo(periodo)
        periodo_ant = previous_periodo(periodo)
        calendario = get_calendario_actividades(periodo)

        context = {
            'calendario': calendario,
            'periodo_actual': periodo,
            'periodo_next': periodo_next,
            'periodo_ant': periodo_ant,
            'autenticado': autenticado,
            'status_preventa': settings.STATUS_PREVENTA,
            'status_venta': settings.STATUS_VENTA,
            'status_finalizado': settings.STATUS_FINALIZADO,
            'status_anulado': settings.STATUS_ANULADO,
        }

        return render(request, 'pages/reserva_calendario.html', context)

    anio = int(datetime.now().year)
    mes = int(datetime.now().month)
    anio_str = str(anio)
    mes_str = str(mes)
    if len(mes_str) == 1:
        mes_str = "0" + mes_str

    periodo_actual = anio_str + mes_str
    periodo_next = next_periodo(periodo_actual)
    periodo_ant = previous_periodo(periodo_actual)

    calendario = get_calendario_actividades(periodo_actual)

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    # web push
    # usuarios para la notificacion
    status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    usuarios_notificacion = apps.get_model('permisos', 'UsersPerfiles').objects.filter(status_id=status_activo, notificacion=1).order_by('user_perfil_id')
    lista_notificacion = ''
    for usuario_notif in usuarios_notificacion:
        lista_notificacion += str(usuario_notif.user_id.id) + '|'

    if len(lista_notificacion) > 0:
        lista_notificacion = lista_notificacion[0:len(lista_notificacion)-1]

    # url push
    url_push = settings.SUB_URL_EMPRESA
    if url_push == 'pvi':
        url_push = '/send_push'
    else:
        url_push = '/' + settings.SUB_URL_EMPRESA + '/send_push'

    context = {
        'url_push': url_push,
        'lista_notificacion': lista_notificacion,

        'cantidad_cart': cantidad_cart,
        'calendario': calendario,
        'periodo_actual': periodo_actual,
        'periodo_next': periodo_next,
        'periodo_ant': periodo_ant,
        'url_carrito': reverse('carrito'),
        'autenticado': autenticado,
        'status_preventa': settings.STATUS_PREVENTA,
        'status_venta': settings.STATUS_VENTA,
        'status_finalizado': settings.STATUS_FINALIZADO,
        'status_anulado': settings.STATUS_ANULADO,
    }

    return render(request, 'pages/reserva.html', context)
