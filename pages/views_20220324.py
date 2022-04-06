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
# reportes
from src.reportes.reportes import reportes_index

# password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from decimal import Decimal

# fechas
from utils.dates_functions import get_date_to_db, get_date_show, get_date_system
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
    for linea in lista_lineas:
        listado_lineas.append(linea)
        # verficamos sus sublineas
        listado2 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea.linea_id).order_by('posicion')
        for linea2 in listado2:
            listado_lineas.append(linea2)
            # tercer nivel
            listado3 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea2.linea_id).order_by('posicion')
            for linea3 in listado3:
                listado_lineas.append(linea3)

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
    #productos_ofertas = lista_productos(request=request, oferta='1')
    productos_ofertas = []
    # listado de mas vendidos
    #productos_mas_vendidos = lista_productos(request=request, mas_vendido='1')
    productos_mas_vendidos = []
    # listado de novedades
    #productos_novedades = lista_productos(request=request, novedad='1')
    productos_novedades = []

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

    try:
        if 'productosinicio' in request.session.keys():
            if 'tipos_montura_select' in request.session['productosinicio'].keys():
                tipos_montura_select = request.session['productosinicio']['tipos_montura_select']

            if 'materiales_select' in request.session['productosinicio'].keys():
                materiales_select = request.session['productosinicio']['materiales_select']

            if 'oferta' in request.session['productosinicio'].keys():
                oferta = request.session['productosinicio']['oferta']

            if 'mas_vendido' in request.session['productosinicio'].keys():
                mas_vendido = request.session['productosinicio']['mas_vendido']

            if 'novedad' in request.session['productosinicio'].keys():
                novedad = request.session['productosinicio']['novedad']

    except Exception as ex:
        # eliminamos la session
        del request.session['productosinicio']

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

    if 'search_producto_x' in request.POST.keys():
        request.session['productosinicio']['producto'] = request.POST['producto'].strip()
        request.session['productosinicio']['linea'] = 0

        request.session['productosinicio']['tipos_montura_select'] = request.POST['tipos_montura_select'].strip()
        request.session['productosinicio']['materiales_select'] = request.POST['materiales_select'].strip()

        request.session['productosinicio']['oferta'] = request.POST['oferta'].strip()
        request.session['productosinicio']['mas_vendido'] = request.POST['mas_vendido'].strip()
        request.session['productosinicio']['novedad'] = request.POST['novedad'].strip()

        # pagina
        request.session['productosinicio']['pagina'] = 1

    if 'search_linea_x' in request.POST.keys():
        request.session['productosinicio']['linea'] = int(request.POST['linea'].strip())
        request.session['productosinicio']['producto'] = ''

        request.session['productosinicio']['tipos_montura_select'] = request.POST['tipos_montura_select'].strip()
        request.session['productosinicio']['materiales_select'] = request.POST['materiales_select'].strip()

        request.session['productosinicio']['oferta'] = request.POST['oferta'].strip()
        request.session['productosinicio']['mas_vendido'] = request.POST['mas_vendido'].strip()
        request.session['productosinicio']['novedad'] = request.POST['novedad'].strip()

        # pagina
        request.session['productosinicio']['pagina'] = 1

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
    for linea in lista_lineas_aux:
        linea_obj = {}
        linea_obj['linea_id'] = linea.linea_id
        linea_obj['linea'] = linea.linea
        linea_obj['espacios'] = ''
        lista_lineas.append(linea_obj)

        # verificamos si tiene lineas inferiores
        lineas_inf1 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea.linea_id).order_by('posicion')

        for linea_dato_inf1 in lineas_inf1:
            linea_obj = {}
            linea_obj['linea_id'] = linea_dato_inf1.linea_id
            linea_obj['linea'] = linea_dato_inf1.linea
            linea_obj['espacios'] = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
            lista_lineas.append(linea_obj)

            # verificamos lineas inferiores nivel2
            lineas_inf2 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea_dato_inf1.linea_id).order_by('posicion')
            for linea_dato_inf2 in lineas_inf2:
                linea_obj2 = {}
                linea_obj2['linea_id'] = linea_dato_inf2.linea_id
                linea_obj2['linea'] = linea_dato_inf2.linea
                linea_obj2['espacios'] = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' * 2
                lista_lineas.append(linea_obj2)

                # verificamos lineas inferiores nivel3
                lineas_inf3 = apps.get_model('configuraciones', 'Lineas').objects.filter(status_id=status_activo, linea_superior_id=linea_dato_inf2.linea_id).order_by('posicion')
                for linea_dato_inf3 in lineas_inf3:
                    linea_obj3 = {}
                    linea_obj3['linea_id'] = linea_dato_inf3.linea_id
                    linea_obj3['linea'] = linea_dato_inf3.linea
                    linea_obj3['espacios'] = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' * 3
                    lista_lineas.append(linea_obj3)

    # descripcion del producto
    txt_producto = ''

    tipos_montura_select = request.session['productosinicio']['tipos_montura_select']
    materiales_select = request.session['productosinicio']['materiales_select']
    oferta = request.session['productosinicio']['oferta']
    mas_vendido = request.session['productosinicio']['mas_vendido']
    novedad = request.session['productosinicio']['novedad']

    if producto_busqueda == '':
        if linea_id == 0:
            lista_pro = lista_productos(request, linea_id=linea1.linea_id, producto_nombre='', oferta=oferta, mas_vendido=mas_vendido, novedad=novedad,
                                        tipo_montura=tipos_montura_select, material=materiales_select)
            # txt_producto = linea1.proveedor_id.proveedor + ' - ' + linea1.linea
            txt_producto = '<span class="link_lineas pointer" onclick="paginaInicio();">Inicio</span>' + link_linea(linea1.linea_id)
        else:
            lista_pro = lista_productos(request, linea_id=linea_id, producto_nombre='', oferta=oferta, mas_vendido=mas_vendido, novedad=novedad, tipo_montura=tipos_montura_select,
                                        disenio_lente=disenio_lentes_select, material=materiales_select, color=colores_select, marca=marcas_select)
            linea_actual = apps.get_model('configuraciones', 'Lineas').objects.get(pk=int(linea_id))
            #txt_producto = linea_actual.proveedor_id.proveedor + ' - ' + linea_actual.linea
            txt_producto = '<span class="link_lineas pointer" onclick="paginaInicio();">Inicio</span>' + link_linea(linea_actual.linea_id)
    else:
        lista_pro = lista_productos(request, linea_id=0, producto_nombre=producto_busqueda, oferta=oferta, mas_vendido=mas_vendido, novedad=novedad,
                                    tipo_montura=tipos_montura_select, disenio_lente=disenio_lentes_select, material=materiales_select, color=colores_select, marca=marcas_select)
        txt_producto = '<span class="link_lineas pointer" onclick="paginaInicio();">Inicio</span>' + ' / ' + producto_busqueda

    url_main = reverse('productos_inicio')
    url_carrito = reverse('carrito')

    # carrito de compras
    cantidad_cart = 0
    if 'productos_cart' in request.session.keys():
        cantidad_cart = len(request.session['productos_cart'])

    # listado por defecto
    # listado por defecto
    status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    tipos_montura_db = apps.get_model('configuraciones', 'TiposMontura').objects.filter(status_id=status_activo).order_by('tipo_montura')
    disenio_lentes_db = apps.get_model('configuraciones', 'DisenioLentes').objects.filter(status_id=status_activo).order_by('disenio_lente')
    materiales_db = apps.get_model('configuraciones', 'Materiales').objects.filter(status_id=status_activo).order_by('material')
    colores_db = apps.get_model('configuraciones', 'Colores').objects.filter(status_id=status_activo).order_by('color')
    marcas_db = apps.get_model('configuraciones', 'Marcas').objects.filter(status_id=status_activo).order_by('marca')

    lista_tipos_montura_select = get_lista_session(request.session['productosinicio']['tipos_montura_select'])
    lista_disenio_lentes_select = get_lista_session(request.session['productosinicio']['disenio_lentes_select'])
    lista_materiales_select = get_lista_session(request.session['productosinicio']['materiales_select'])
    lista_colores_select = get_lista_session(request.session['productosinicio']['colores_select'])
    lista_marcas_select = get_lista_session(request.session['productosinicio']['marcas_select'])

    color_borde_resaltado = '#46107F'
    color_borde_normal = '#FFFFFF'

    p_lista_tipos_montura = ''
    p_lista_disenio_lentes = ''
    p_lista_materiales = ''
    p_lista_colores = ''
    p_lista_marcas = ''

    # tipos de montura
    lista_tipos_montura = get_lista_cuadros('tipo_montura_id', request.session['productosinicio']['lista_tipos_montura'], lista_tipos_montura_select, color_borde_normal, color_borde_resaltado)
    for aux_li in lista_tipos_montura:
        p_lista_tipos_montura += str(aux_li['tipo_montura_id']) + ','
    # ajustamos
    if len(p_lista_tipos_montura) > 0:
        p_lista_tipos_montura = p_lista_tipos_montura[0:len(p_lista_tipos_montura)-1]

    # disenio lentes
    lista_disenio_lentes = get_lista_cuadros('disenio_lente_id', request.session['productosinicio']['lista_disenio_lentes'], lista_disenio_lentes_select, color_borde_normal, color_borde_resaltado)
    for aux_li in lista_disenio_lentes:
        p_lista_disenio_lentes += str(aux_li['disenio_lente_id']) + ','
    # ajustamos
    if len(p_lista_disenio_lentes) > 0:
        p_lista_disenio_lentes = p_lista_disenio_lentes[0:len(p_lista_disenio_lentes)-1]

    # materiales
    lista_materiales = get_lista_cuadros('material_id', request.session['productosinicio']['lista_materiales'], lista_materiales_select, color_borde_normal, color_borde_resaltado)
    for aux_li in lista_materiales:
        p_lista_materiales += str(aux_li['material_id']) + ','
    # ajustamos
    if len(p_lista_materiales) > 0:
        p_lista_materiales = p_lista_materiales[0:len(p_lista_materiales)-1]

    # colores
    lista_colores = get_lista_cuadros('color_id', request.session['productosinicio']['lista_colores'], lista_colores_select, color_borde_normal, color_borde_resaltado)
    for aux_li in lista_colores:
        p_lista_colores += str(aux_li['color_id']) + ','
    # ajustamos
    if len(p_lista_colores) > 0:
        p_lista_colores = p_lista_colores[0:len(p_lista_colores)-1]

    # marcas
    lista_marcas = get_lista_cuadros('marca_id', request.session['productosinicio']['lista_marcas'], lista_marcas_select, color_borde_normal, color_borde_resaltado)
    for aux_li in lista_marcas:
        p_lista_marcas += str(aux_li['marca_id']) + ','
    # ajustamos
    if len(p_lista_marcas) > 0:
        p_lista_marcas = p_lista_marcas[0:len(p_lista_marcas)-1]

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
                dato_producto['disenio_lente_id'] = producto_r.producto_relacion_id.disenio_lente_id
                dato_producto['material_id'] = producto_r.producto_relacion_id.material_id
                dato_producto['color_id'] = producto_r.producto_relacion_id.color_id
                dato_producto['marca_id'] = producto_r.producto_relacion_id.marca_id
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
            'lista_lineas': lista_lineas,
            'linea_session': request.session['productosinicio']['linea'],
            'producto_session': request.session['productosinicio']['producto'],
            'url_main': url_main,
            'url_carrito': url_carrito,
            'url_index': reverse('index'),
            'cantidad_cart': cantidad_cart,
            'txt_producto': txt_producto,

            'productos_relacionados': listado,

            'producto': producto,
            'imagen1': imagen1,
            'productos_imagenes': productos_imagenes,

            'lista_tipos_montura': lista_tipos_montura,
            'lista_disenio_lentes': lista_disenio_lentes,
            'lista_materiales': lista_materiales,
            'lista_colores': lista_colores,
            'lista_marcas': lista_marcas,

            'p_lista_tipos_montura': p_lista_tipos_montura,
            'p_lista_disenio_lentes': p_lista_disenio_lentes,
            'p_lista_materiales': p_lista_materiales,
            'p_lista_colores': p_lista_colores,
            'p_lista_marcas': p_lista_marcas,

            'oferta': oferta,
            'mas_vendido': mas_vendido,
            'novedad': novedad,

            'color_borde_normal': color_borde_normal,
            'color_borde_resaltado': color_borde_resaltado,

            'tipos_montura_select': tipos_montura_select,
            'disenio_lentes_select': disenio_lentes_select,
            'materiales_select': materiales_select,
            'colores_select': colores_select,
            'marcas_select': marcas_select,

            'tipos_montura_db': tipos_montura_db,
            'disenio_lentes_db': disenio_lentes_db,
            'materiales_db': materiales_db,
            'colores_db': colores_db,
            'marcas_db': marcas_db,
        }

        return render(request, 'pages/productos_inicio_detalle.html', context_p)

    # ajax para la busqueda de productos
    if 'from_index' not in request.POST.keys():
        if 'search_producto_x' in request.POST.keys() or 'search_linea_x' in request.POST.keys() or 'pagina' in request.POST.keys():
            context2 = {
                'autenticado': autenticado,
                'lista_lineas': lista_lineas,
                'listado_productos': lista_pro,

                'lista_tipos_montura': lista_tipos_montura,
                'lista_disenio_lentes': lista_disenio_lentes,
                'lista_materiales': lista_materiales,
                'lista_colores': lista_colores,
                'lista_marcas': lista_marcas,

                'p_lista_tipos_montura': p_lista_tipos_montura,
                'p_lista_disenio_lentes': p_lista_disenio_lentes,
                'p_lista_materiales': p_lista_materiales,
                'p_lista_colores': p_lista_colores,
                'p_lista_marcas': p_lista_marcas,

                'oferta': oferta,
                'mas_vendido': mas_vendido,
                'novedad': novedad,

                'color_borde_normal': color_borde_normal,
                'color_borde_resaltado': color_borde_resaltado,

                'tipos_montura_select': tipos_montura_select,
                'disenio_lentes_select': disenio_lentes_select,
                'materiales_select': materiales_select,
                'colores_select': colores_select,
                'marcas_select': marcas_select,

                'tipos_montura_db': tipos_montura_db,
                'disenio_lentes_db': disenio_lentes_db,
                'materiales_db': materiales_db,
                'colores_db': colores_db,
                'marcas_db': marcas_db,

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
        'listado_productos': lista_pro,

        'lista_tipos_montura': lista_tipos_montura,
        'lista_disenio_lentes': lista_disenio_lentes,
        'lista_materiales': lista_materiales,
        'lista_colores': lista_colores,
        'lista_marcas': lista_marcas,

        'p_lista_tipos_montura': p_lista_tipos_montura,
        'p_lista_disenio_lentes': p_lista_disenio_lentes,
        'p_lista_materiales': p_lista_materiales,
        'p_lista_colores': p_lista_colores,
        'p_lista_marcas': p_lista_marcas,

        'oferta': oferta,
        'mas_vendido': mas_vendido,
        'novedad': novedad,

        'color_borde_normal': color_borde_normal,
        'color_borde_resaltado': color_borde_resaltado,

        'tipos_montura_select': tipos_montura_select,
        'disenio_lentes_select': disenio_lentes_select,
        'materiales_select': materiales_select,
        'colores_select': colores_select,
        'marcas_select': marcas_select,

        'tipos_montura_db': tipos_montura_db,
        'disenio_lentes_db': disenio_lentes_db,
        'materiales_db': materiales_db,
        'colores_db': colores_db,
        'marcas_db': marcas_db,

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


def link_linea(linea_id):
    try:
        linea = apps.get_model('configuraciones', 'Lineas').objects.get(pk=int(linea_id))
        retorno = ''
        if linea.linea_principal == 1:
            retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'

        else:
            # linea principal antes
            linea_sup1 = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea.linea_superior_id)

            if linea_sup1.linea_principal == 1:
                retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup1.linea_id) + "'" + ');">' + linea_sup1.linea + '</span>'
                retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'
            else:
                # otra linea superior antes
                linea_sup2 = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea_sup1.linea_superior_id)

                if linea_sup2.linea_principal == 1:
                    retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup2.linea_id) + "'" + ');">' + linea_sup2.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup1.linea_id) + "'" + ');">' + linea_sup1.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'
                else:
                    linea_sup3 = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea_sup2.linea_superior_id)
                    retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup3.linea_id) + "'" + ');">' + linea_sup3.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup2.linea_id) + "'" + ');">' + linea_sup2.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup1.linea_id) + "'" + ');">' + linea_sup1.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'

        return retorno

    except Exception as ex:
        retorno = ''
        return retorno


def lista_productos(request, linea_id=0, producto_nombre='', novedad='0', mas_vendido='0', oferta='0', tipo_montura='', material=''):
    #print('color...', color)
    producto = reemplazar_codigo_html(producto_nombre.strip())

    """lista de productos segun linea o ubicacion"""
    settings_sistema = get_system_settings()
    cant_per_page = settings_sistema['cant_productos_home']

    # verificamos si escribo busqueda o selecciono combo
    sql_add = "AND p.status_id='1' AND l.status_id='1' "
    sql_add_linea = "AND p.status_id='1' AND l.status_id='1' "
    sql_add_filtro = "AND p.status_id='1' AND l.status_id='1' "

    if len(tipo_montura) > 0:
        div_tipo = tipo_montura.split(',')
        sql_add += f"AND ("
        for dato in div_tipo:
            sql_add += f"p.tipo_montura_id LIKE '%{dato}%' OR "
            sql_add_linea += f"p.tipo_montura_id LIKE '%{dato}%' OR "
        sql_add = sql_add[0:len(sql_add)-4] + ') '
        sql_add_linea = sql_add_linea[0:len(sql_add_linea)-4] + ') '

    if len(material) > 0:
        div_material = material.split(',')
        sql_add += f"AND ("
        for dato in div_material:
            sql_add += f"p.material_id LIKE '%{dato}%' OR "
            sql_add_linea += f"p.material_id LIKE '%{dato}%' OR "
        sql_add = sql_add[0:len(sql_add)-4] + ') '
        sql_add_linea = sql_add_linea[0:len(sql_add_linea)-4] + ') '

    if oferta == '1' or novedad == '1' or mas_vendido == '1':
        sql_add += "AND ("
        sql_add_linea += "AND ("

        if oferta == '1':
            sql_add += "p.oferta='1' OR "
            sql_add_linea += "p.oferta='1' OR "

        if novedad == '1':
            sql_add += "p.novedad='1' OR "
            sql_add_linea += "p.novedad='1' OR "

        if mas_vendido == '1':
            sql_add += "p.mas_vendido='1' OR "
            sql_add_linea += "p.mas_vendido='1' OR "

        # quitamos el ultimo OR
        sql_add = sql_add[0:len(sql_add)-4] + ') '
        sql_add_linea = sql_add_linea[0:len(sql_add_linea)-4] + ') '

    # linea
    # if linea_id != 0:
    #     sql_add = f"AND l.linea_id='{linea_id}' "
        #sql_add_filtro += f"AND l.linea_id='{linea_id}' "

    if producto != '':
        division = producto.split(' ')
        if len(division) == 1:
            sql_add += f"AND p.producto LIKE '%{producto}%' "
            sql_add_filtro += f"AND p.producto LIKE '%{producto}%' "

        elif len(division) == 2:
            sql_add += f"AND (p.producto LIKE '%{division[0]}%{division[1]}%' OR p.producto LIKE '%{division[1]}%{division[0]}%' "
            sql_add += ') '

            sql_add_filtro += f"AND (p.producto LIKE '%{division[0]}%{division[1]}%' OR p.producto LIKE '%{division[1]}%{division[0]}%' "
            sql_add_filtro += ') '

        # if len(division) == 3:
        elif len(division) == 3:
            sql_add += f"AND (p.producto LIKE '%{division[0]}%{division[1]}%{division[2]}%' "
            sql_add += f"OR p.producto LIKE '%{division[0]}%{division[2]}%{division[1]}%' "

            sql_add += f"OR p.producto LIKE '%{division[1]}%{division[0]}%{division[2]}%' "
            sql_add += f"OR p.producto LIKE '%{division[1]}%{division[2]}%{division[0]}%' "

            sql_add += f"OR p.producto LIKE '%{division[2]}%{division[0]}%{division[1]}%' "
            sql_add += f"OR p.producto LIKE '%{division[2]}%{division[1]}%{division[0]}%' "

            sql_add += ') '

            sql_add_filtro += f"AND (p.producto LIKE '%{division[0]}%{division[1]}%{division[2]}%' "
            sql_add_filtro += f"OR p.producto LIKE '%{division[0]}%{division[2]}%{division[1]}%' "

            sql_add_filtro += f"OR p.producto LIKE '%{division[1]}%{division[0]}%{division[2]}%' "
            sql_add_filtro += f"OR p.producto LIKE '%{division[1]}%{division[2]}%{division[0]}%' "

            sql_add_filtro += f"OR p.producto LIKE '%{division[2]}%{division[0]}%{division[1]}%' "
            sql_add_filtro += f"OR p.producto LIKE '%{division[2]}%{division[1]}%{division[0]}%' "

            sql_add_filtro += ') '
        else:
            nuevo_p = '%'
            for i in range(len(division)):
                nuevo_p += division[i] + '%'

            sql_add += f"AND p.producto LIKE '{nuevo_p}' "
            sql_add_filtro += f"AND p.producto LIKE '{nuevo_p}' "

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

    pages_limit_bottom = (int(request.session['productosinicio']['pagina']) - 1) * cant_per_page
    pages_limit_top = cant_per_page

    # listado de productos
    lista_pp = []
    cant_total = 0

    # listados generales de color, marca, etc producto o linea
    # sin contar los otros filtros, para que el usuario pueda filtrar solo de este grupo
    listado_tipos_montura = []
    listado_materiales = []

    # busqueda por de texto de productos
    if linea_id == 0:
        # listados del grupo por busqueda de producto txt
        sql = "SELECT DISTINCT p.tipo_montura_id, p.disenio_lente_id, p.material_id, p.color_id, p.marca_id FROM productos p, lineas l WHERE p.linea_id=l.linea_id "
        sql += sql_add_filtro
        #print('sql..: ', sql)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                # tipos montura
                existe = 0
                for lis_tp in listado_tipos_montura:
                    if str(lis_tp) == str(row[0]):
                        existe = 1
                if existe == 0:
                    listado_tipos_montura.append(row[0])

                # disenio lentes
                existe = 0
                for list_dl in listado_disenio_lentes:
                    if str(list_dl) == str(row[0]):
                        existe = 1
                if existe == 0:
                    listado_disenio_lentes.append(row[0])

                # disenio materiales
                existe = 0
                for list_ma in listado_materiales:
                    if str(list_ma) == str(row[0]):
                        existe = 1
                if existe == 0:
                    listado_materiales.append(row[0])

                # colores
                existe = 0
                for lis_col in listado_colores:
                    if str(lis_col) == str(row[0]):
                        existe = 1
                if existe == 0:
                    listado_colores.append(row[0])

                # marcas
                existe = 0
                for lis_mar in listado_marcas:
                    if str(lis_mar) == str(row[1]):
                        existe = 1
                if existe == 0:
                    listado_marcas.append(row[1])

        sql = "SELECT l.linea, p.producto, p.codigo, p.precio, p.precio_oferta, p.producto_id, l.linea_id, "
        sql += "p.tipo_montura_id, p.disenio_lente_id, p.material_id, p.color_id, p.marca_id, p.novedad, p.mas_vendido, p.oferta "
        sql += "FROM productos p, lineas l WHERE p.linea_id=l.linea_id " + sql_add
        sql += "ORDER BY l.linea, p.producto "
        #print('sql: ', sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                cant_total = cant_total + 1
                # imagen del producto
                sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row[5]}' ORDER BY posicion LIMIT 0,1 "
                imagen = ''
                imagen_thumb = ''
                with connection.cursor() as cursor2:
                    cursor2.execute(sql_imagen)
                    row_imagen = cursor2.fetchone()
                    if row_imagen:
                        imagen = row_imagen[0]
                        imagen_thumb = row_imagen[1]

                dato_producto = {}
                dato_producto['linea'] = row[0]
                dato_producto['producto'] = reemplazar_codigo_html(row[1])
                dato_producto['codigo'] = row[2]
                dato_producto['precio'] = row[3]
                dato_producto['precio_oferta'] = row[4]
                dato_producto['imagen'] = imagen
                dato_producto['imagen_thumb'] = imagen_thumb
                dato_producto['producto_id'] = row[5]

                dato_producto['tipo_montura_id'] = row[7]
                dato_producto['disenio_lente_id'] = row[8]
                dato_producto['material_id'] = row[9]
                dato_producto['color_id'] = row[10]
                dato_producto['marca_id'] = row[11]
                dato_producto['novedad'] = row[12]
                dato_producto['mas_vendido'] = row[13]
                dato_producto['oferta'] = row[14]

                lista_pp.append(dato_producto)

    # busqueda por seleccion de linea
    # busqueda por seleccion de linea
    if linea_id != 0:
        # listados del grupo por busqueda de producto txt
        sql = f"SELECT DISTINCT p.tipo_montura_id, p.disenio_lente_id, p.material_id, p.color_id, p.marca_id FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{linea_id}' "
        sql += sql_add_filtro
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                # tipos montura
                existe = 0
                for lis_tp in listado_tipos_montura:
                    if str(lis_tp) == str(row[0]):
                        existe = 1
                if existe == 0:
                    listado_tipos_montura.append(row[0])

                # disenio lentes
                existe = 0
                for list_dl in listado_disenio_lentes:
                    if str(list_dl) == str(row[0]):
                        existe = 1
                if existe == 0:
                    listado_disenio_lentes.append(row[0])

                # disenio materiales
                existe = 0
                for list_ma in listado_materiales:
                    if str(list_ma) == str(row[0]):
                        existe = 1
                if existe == 0:
                    listado_materiales.append(row[0])

                # colores
                existe = 0
                for lis_col in listado_colores:
                    if str(lis_col) == str(row[0]):
                        existe = 1
                if existe == 0:
                    listado_colores.append(row[0])

                # marcas
                existe = 0
                for lis_mar in listado_marcas:
                    if str(lis_mar) == str(row[1]):
                        existe = 1
                if existe == 0:
                    listado_marcas.append(row[1])

        # entramos un nivel
        sql = "SELECT l.linea, p.producto, p.codigo, p.precio, p.precio_oferta, p.producto_id, l.linea_id, "
        sql += "p.tipo_montura_id, p.disenio_lente_id, p.material_id, p.color_id, p.marca_id, p.novedad, p.mas_vendido, p.oferta "
        sql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{linea_id}' "
        sql += sql_add_linea
        sql += "ORDER BY l.linea, p.producto "
        #print('sql: ', sql)

        with connection.cursor() as cursor22:
            cursor22.execute(sql)
            rows2 = cursor22.fetchall()

            for row2 in rows2:
                cant_total = cant_total + 1
                # imagen del producto
                sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row2[5]}' ORDER BY posicion LIMIT 0,1 "
                imagen = ''
                imagen_thumb = ''
                with connection.cursor() as cursor33:
                    cursor33.execute(sql_imagen)
                    row_imagen3 = cursor33.fetchone()
                    if row_imagen3:
                        imagen = row_imagen3[0]
                        imagen_thumb = row_imagen3[1]

                dato_producto = {}
                dato_producto['linea'] = row2[0]
                dato_producto['producto'] = reemplazar_codigo_html(row2[1])
                dato_producto['codigo'] = row2[2]
                dato_producto['precio'] = row2[3]
                dato_producto['precio_oferta'] = row2[4]
                dato_producto['imagen'] = imagen
                dato_producto['imagen_thumb'] = imagen_thumb
                dato_producto['producto_id'] = row2[5]

                dato_producto['tipo_montura_id'] = row2[7]
                dato_producto['disenio_lente_id'] = row2[8]
                dato_producto['material_id'] = row2[9]
                dato_producto['color_id'] = row2[10]
                dato_producto['marca_id'] = row2[11]
                dato_producto['novedad'] = row2[12]
                dato_producto['mas_vendido'] = row2[13]
                dato_producto['oferta'] = row2[14]

                lista_pp.append(dato_producto)

        # lineas inferior segundo nivel
        sql = f"SELECT linea_id FROM lineas WHERE linea_superior_id='{linea_id}' "
        with connection.cursor() as cursor10:
            cursor10.execute(sql)
            rows10 = cursor10.fetchall()
            for row10 in rows10:

                # segundo nivel
                # listados del grupo por busqueda de producto txt
                sql = f"SELECT DISTINCT p.tipo_montura_id, p.disenio_lente_id, p.material_id, p.color_id, p.marca_id  FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{row10[0]}' "
                sql += sql_add_filtro
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    for row in rows:
                        # tipos montura
                        existe = 0
                        for lis_tp in listado_tipos_montura:
                            if str(lis_tp) == str(row[0]):
                                existe = 1
                        if existe == 0:
                            listado_tipos_montura.append(row[0])

                        # disenio lentes
                        existe = 0
                        for list_dl in listado_disenio_lentes:
                            if str(list_dl) == str(row[0]):
                                existe = 1
                        if existe == 0:
                            listado_disenio_lentes.append(row[0])

                        # disenio materiales
                        existe = 0
                        for list_ma in listado_materiales:
                            if str(list_ma) == str(row[0]):
                                existe = 1
                        if existe == 0:
                            listado_materiales.append(row[0])

                        # colores
                        existe = 0
                        for lis_col in listado_colores:
                            if str(lis_col) == str(row[0]):
                                existe = 1
                        if existe == 0:
                            listado_colores.append(row[0])

                        # marcas
                        existe = 0
                        for lis_mar in listado_marcas:
                            if str(lis_mar) == str(row[1]):
                                existe = 1
                        if existe == 0:
                            listado_marcas.append(row[1])

                # segundo nivel
                sql = "SELECT l.linea, p.producto, p.codigo, p.precio, p.precio_oferta, p.producto_id, l.linea_id, "
                sql += "p.tipo_montura_id, p.disenio_lente_id, p.material_id, p.color_id, p.marca_id, p.novedad, p.mas_vendido, p.oferta "
                sql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{row10[0]}' "
                sql += sql_add_linea
                sql += "ORDER BY l.linea, p.producto "
                #print('sql2: ', sql)
                with connection.cursor() as cursor44:
                    cursor44.execute(sql)
                    rows4 = cursor44.fetchall()
                    for row4 in rows4:
                        cant_total = cant_total + 1

                        # imagen del producto
                        sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row4[5]}' ORDER BY posicion LIMIT 0,1 "
                        imagen = ''
                        imagen_thumb = ''
                        with connection.cursor() as cursor55:
                            cursor55.execute(sql_imagen)
                            row_imagen5 = cursor55.fetchone()
                            if row_imagen5:
                                imagen = row_imagen5[0]
                                imagen_thumb = row_imagen5[1]

                        dato_producto = {}
                        dato_producto['linea'] = row4[0]
                        dato_producto['producto'] = reemplazar_codigo_html(row4[1])
                        dato_producto['codigo'] = row4[2]
                        dato_producto['precio'] = row4[3]
                        dato_producto['precio_oferta'] = row4[4]
                        dato_producto['imagen'] = imagen
                        dato_producto['imagen_thumb'] = imagen_thumb
                        dato_producto['producto_id'] = row4[5]

                        dato_producto['tipo_montura_id'] = row4[7]
                        dato_producto['disenio_lente_id'] = row4[8]
                        dato_producto['material_id'] = row4[9]
                        dato_producto['color_id'] = row4[10]
                        dato_producto['marca_id'] = row4[11]
                        dato_producto['novedad'] = row4[12]
                        dato_producto['mas_vendido'] = row4[13]
                        dato_producto['oferta'] = row4[14]

                        lista_pp.append(dato_producto)

                # tercer nivel
                sql = f"SELECT linea_id FROM lineas WHERE linea_superior_id='{row10[0]}' "
                with connection.cursor() as cursor20:
                    cursor20.execute(sql)
                    rows20 = cursor20.fetchall()
                    for row20 in rows20:
                        # tercer nivel
                        # listados del grupo por busqueda de producto txt
                        sql = f"SELECT DISTINCT p.tipo_montura_id, p.disenio_lente_id, p.material_id, p.color_id, p.marca_id FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{row20[0]}' "
                        sql += sql_add_filtro
                        with connection.cursor() as cursor:
                            cursor.execute(sql)
                            rows = cursor.fetchall()
                            for row in rows:
                                # tipos montura
                                existe = 0
                                for lis_tp in listado_tipos_montura:
                                    if str(lis_tp) == str(row[0]):
                                        existe = 1
                                if existe == 0:
                                    listado_tipos_montura.append(row[0])

                                # disenio lentes
                                existe = 0
                                for list_dl in listado_disenio_lentes:
                                    if str(list_dl) == str(row[0]):
                                        existe = 1
                                if existe == 0:
                                    listado_disenio_lentes.append(row[0])

                                # disenio materiales
                                existe = 0
                                for list_ma in listado_materiales:
                                    if str(list_ma) == str(row[0]):
                                        existe = 1
                                if existe == 0:
                                    listado_materiales.append(row[0])

                                # colores
                                existe = 0
                                for lis_col in listado_colores:
                                    if str(lis_col) == str(row[0]):
                                        existe = 1
                                if existe == 0:
                                    listado_colores.append(row[0])

                                # marcas
                                existe = 0
                                for lis_mar in listado_marcas:
                                    if str(lis_mar) == str(row[1]):
                                        existe = 1
                                if existe == 0:
                                    listado_marcas.append(row[1])

                        # tercer nivel
                        sql = "SELECT l.linea, p.producto, p.codigo, p.precio, p.precio_oferta, p.producto_id, l.linea_id, "
                        sql += "p.tipo_montura_id, p.disenio_lente_id, p.material_id, p.color_id, p.marca_id, p.novedad, p.mas_vendido, p.oferta "
                        sql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{row20[0]}' "
                        sql += sql_add_linea
                        sql += "ORDER BY l.linea, p.producto "
                        #print('sql 3: ', sql)
                        with connection.cursor() as cursor66:
                            cursor66.execute(sql)
                            rows6 = cursor66.fetchall()
                            for row6 in rows6:
                                cant_total = cant_total + 1

                                # imagen del producto
                                sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row6[5]}' ORDER BY posicion LIMIT 0,1 "
                                imagen = ''
                                imagen_thumb = ''
                                with connection.cursor() as cursor77:
                                    cursor77.execute(sql_imagen)
                                    row_imagen7 = cursor77.fetchone()
                                    if row_imagen7:
                                        imagen = row_imagen7[0]
                                        imagen_thumb = row_imagen7[1]

                                dato_producto = {}
                                dato_producto['linea'] = row6[0]
                                dato_producto['producto'] = reemplazar_codigo_html(row6[1])
                                dato_producto['codigo'] = row6[2]
                                dato_producto['precio'] = row6[3]
                                dato_producto['precio_oferta'] = row6[4]
                                dato_producto['imagen'] = imagen
                                dato_producto['imagen_thumb'] = imagen_thumb
                                dato_producto['producto_id'] = row6[5]

                                dato_producto['tipo_montura_id'] = row6[7]
                                dato_producto['disenio_lente_id'] = row6[8]
                                dato_producto['material_id'] = row6[9]
                                dato_producto['color_id'] = row6[10]
                                dato_producto['marca_id'] = row6[11]
                                dato_producto['novedad'] = row6[12]
                                dato_producto['mas_vendido'] = row6[13]
                                dato_producto['oferta'] = row6[14]

                                lista_pp.append(dato_producto)

    # listados generales
    # print('listado_colores: ', listado_colores)
    # print('listado_marcas: ', listado_marcas)
    # print('listado_tallas: ', listado_tallas)

    # paginacion
    #print('cant total: ', cant_total)
    j = 1
    i = 0
    pages_list = []
    while i < cant_total:
        pages_list.append(j)
        i = i + cant_per_page
        j += 1
        if j > 15:
            break

    request.session['productosinicio']['pages_list'] = pages_list
    request.session.modified = True

    # listado de retorno
    listado = []
    cant_fila = 3
    cant_actual = 0
    lista_fila = []
    contador = 0

    #print('lista prodd: ', lista_pp)
    #print('limit bottom: ', pages_limit_bottom, ' limit top: ', pages_limit_top)
    for producto_p in lista_pp:
        if contador >= pages_limit_bottom and contador < (pages_limit_bottom+pages_limit_top):
            if cant_actual < cant_fila:
                lista_fila.append(producto_p)

            # aumentamos la columna
            cant_actual += 1

            if cant_actual == cant_fila:
                listado.append(lista_fila)
                cant_actual = 0
                lista_fila = []

        contador += 1

    # print('lista colores: ', lista_colores)
    # print('lista tallas: ', lista_tallas)
    # print('lista marcas: ', lista_marcas)
    request.session['productosinicio']['lista_tipos_montura'] = listado_tipos_montura
    request.session['productosinicio']['lista_disenio_lentes'] = listado_disenio_lentes
    request.session['productosinicio']['lista_materiales'] = listado_materiales
    request.session['productosinicio']['lista_colores'] = listado_colores
    request.session['productosinicio']['lista_marcas'] = listado_marcas
    request.session.modified = True

    # termina los productos
    if cant_actual > 0:
        # no termino de llenarse los datos de la fila
        for i in range(cant_actual, cant_fila):
            dato_producto = {}
            dato_producto['linea'] = ''
            dato_producto['producto'] = ''
            dato_producto['codigo'] = ''
            dato_producto['precio'] = ''
            dato_producto['precio_oferta'] = 0
            dato_producto['producto_id'] = 0
            lista_fila.append(dato_producto)

        # aniadimos a la lista principal
        listado.append(lista_fila)

    # devolvemos los productos
    #print('listado...: ', listado)
    return listado


def reemplazar_codigo_html(cadena):
    retorno = cadena
    retorno = retorno.replace('&', "&#38;")
    retorno = retorno.replace('#', "&#35;")

    retorno = retorno.replace("'", "&#39;")
    retorno = retorno.replace('"', "&#34;")
    retorno = retorno.replace('á', "&#225;")
    retorno = retorno.replace('é', "&#233;")
    retorno = retorno.replace('í', "&#237;")
    retorno = retorno.replace('ó', "&#243;")
    retorno = retorno.replace('ú', "&#250;")
    retorno = retorno.replace('Á', "&#193;")
    retorno = retorno.replace('É', "&#201;")
    retorno = retorno.replace('Í', "&#205;")
    retorno = retorno.replace('Ó', "&#211;")
    retorno = retorno.replace('Ú', "&#218;")
    retorno = retorno.replace('!', "&#33;")

    retorno = retorno.replace('$', "&#36;")
    retorno = retorno.replace('%', "&#37;")
    retorno = retorno.replace('*', "&#42;")
    retorno = retorno.replace('+', "&#43;")
    retorno = retorno.replace('-', "&#45;")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")

    return retorno


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
        sucursal = apps.get_model('configuraciones', 'Sucursales').objects.get(pk=punto.sucursal_id.sucursal_id)

        # lista de puntos y sucursales
        estado_activo = 1

        # datos para las consultas
        fecha_actual = get_date_system()
        fecha1 = get_date_to_db(fecha=fecha_actual, formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss')
        fecha2 = get_date_to_db(fecha=fecha_actual, formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

        notificaciones = []
        cantidad = 0
        cantidad_rojos = 0

        # lista pedidos
        sql = "SELECT p.pedido_id, p.apellidos, p.nombres, p.total, p.created_at AS fecha FROM pedidos p "
        #sql += f"WHERE p.status_id='{estado_activo}' AND p.created_at>='{fecha1}' AND p.created_at<='{fecha2}' ORDER BY p.created_at "
        sql += f"WHERE p.status_id='{estado_activo}' ORDER BY p.created_at "
        #print('sql: ', sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                cantidad += 1
                cantidad_rojos += 1
                dato = {}
                dato['tipo'] = 'pedido'
                fecha = get_date_show(fecha=row[4], formato='dd-MMM-yyyy HH:ii', formato_ori='yyyy-mm-dd HH:ii:ss')
                dato['descripcion'] = fecha + ', ' + row[1] + ' ' + row[2] + ', ' + str(row[3])
                dato['url'] = url_pedidos_cliente
                notificaciones.append(dato)

        # context para el html
        context = {
            'notificaciones': notificaciones,
            'cantidad': cantidad,
            'cantidad_rojos': cantidad_rojos,
            'autenticado': autenticado,
        }

        return render(request, 'pages/notificaciones_pagina.html', context)

    except Exception as e:
        print('ERROR ' + str(e))
        context = {
            'cantidad': 0,
            'cantidad_rojos': 0,
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


def get_lista_session(session_var):
    lista_select = []
    if len(session_var) > 0:
        div_lista = session_var.split(',')
        for dato in div_lista:
            lista_select.append(dato.strip())

    return lista_select


def get_lista_cuadros(col_name, lista_session, lista_select, borde_nomal, borde_resaltado):

    # listado
    listado = []
    if len(lista_session) > 0:
        for ax_d in lista_session:
            dato = {}
            dato[col_name] = ax_d
            existe = 0
            for lcs in lista_select:
                if str(lcs) == str(ax_d):
                    existe = 1

            if existe == 0:
                dato['borde'] = borde_nomal
            else:
                dato['borde'] = borde_resaltado

            listado.append(dato)

    return listado


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
        lista_tablas = [['auth', 'User', 'auth_user'], ['status', 'Status', 'status'],

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
                        ['productos', 'ProductosImagenes', 'productos_imagenes'],
                        ['productos', 'ProductosRelacionados', 'productos_relacionados'],
                        ['productos', 'ProductosTiposMontura', 'productos_tipos_montura'],
                        ['productos', 'ProductosMateriales', 'productos_materiales'],

                        ['inventarios', 'Registros', 'registros'],
                        ['inventarios', 'RegistrosDetalles', 'registros_detalles'],
                        ['inventarios', 'Stock', 'stock'],

                        ['ventas', 'Dosificaciones', 'dosificaciones'],
                        ['ventas', 'Facturas', 'facturas'],
                        ['ventas', 'PlanPagos', 'plan_pagos'],
                        ['ventas', 'PlanPagosDetalles', 'plan_pagos_detalles'],
                        ['ventas', 'PlanPagosPagos', 'plan_pagos_pagos'],
                        ['ventas', 'Ventas', 'ventas'],
                        ['ventas', 'VentasDetalles', 'ventas_detalles'],
                        ['ventas', 'VentasImagenes', 'ventas_imagenes'],
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
