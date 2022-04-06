from email.mime import image
from django.apps import apps
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# settings de la app
from django.conf import settings
from ventas.models import Ventas, VentasDetalles
from utils.dates_functions import get_date_show, get_date_to_db, get_date_id

# para los usuarios
from utils.permissions import current_date, get_user_permission_operation, get_permissions_user, get_almacen_user, get_system_settings

# clases por modulo
from controllers.ventas.VentasController import VentasController
from controllers.ListasController import ListasController
from controllers.SystemController import SystemController
from controllers.clientes.ClientesController import ClientesController
from controllers.cajas.CajasController import CajasController
from controllers.inventarios.StockController import StockController

# reportes
import io
import os
import shutil
from os import remove
from django.http import FileResponse

from django.core.files.base import ContentFile
from PIL import Image

# from reportes.ventas.rptVentasConCostos import rptVentasConCostos
# from reportes.ventas.rptVentasSinCostos import rptVentasSinCostos
from reportes.ventas.rptVentasResumen import rptVentasResumen
from reportes.ventas.rptVentasDisenio import rptVentasDisenio
from reportes.ventas.rptVentasPreImpreso import rptVentasPreImpreso

from reportes.cajas.rptCajaEgresoRecibo import rptCajaEgresoRecibo
from reportes.cajas.rptCajaIngresoRecibo import rptCajaIngresoRecibo

venta_controller = VentasController()
lista_controller = ListasController()
system_controller = SystemController()
cliente_controller = ClientesController()
caja_controller = CajasController()
stock_controller = StockController()


# ventas
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'lista'), 'without_permission')
def ventas_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_VENTAS)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'anular',
                             'buscar_cliente', 'stock_monturas',
                             'pasar_venta', 'pasar_venta_anular',
                             #  'pasar_salida', 'pasar_salida_anular',
                             #  'pasar_vuelta', 'pasar_vuelta_anular',
                             # 'gastos', 'gastos_print', 'cobros', 'cobros_print',
                             'add_imagen', 'mostrar_imagen', 'eliminar_imagen',
                             'mostrar_imagen_venta', 'get_historias',
                             'cobros', 'cobros_print',
                             'pasar_finalizado', 'pasar_finalizado_anular',
                             'imprimir_preimpreso', 'imprimir_disenio',
                             'print_resumen']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'get_historias':
            cliente_id = int(request.POST['cliente_id'])
            nombres = request.POST['nombres']
            apellidos = request.POST['apellidos']

            historias = venta_controller.get_historias(cliente_id)
            context_img = {
                'historias': historias,
                'nombres': nombres,
                'apellidos': apellidos
            }
            return render(request, 'ventas/ventas_historias.html', context_img)

        if operation == 'mostrar_imagen':
            id = request.POST['id']
            imagenes = request.session['session_imagenes']
            imagen_mostrar = None
            for imagen in imagenes:
                if imagen['imagen_id'] == id:
                    imagen_mostrar = imagen['imagen']

            context_img = {
                'imagen_mostrar': imagen_mostrar,
                'autenticado': 'si',
            }
            return render(request, 'ventas/ventas_imagenes_mostrar.html', context_img)

        if operation == 'mostrar_imagen_venta':
            id = int(request.POST['id'])
            venta_imagen = apps.get_model('ventas', 'VentasImagenes').objects.get(pk=id)

            context_img = {
                'venta_imagen': venta_imagen,
            }
            return render(request, 'ventas/ventas_imagen_venta.html', context_img)

        if operation == 'eliminar_imagen':
            id = request.POST['id']
            imagenes = request.session['session_imagenes']
            nombre_img = ""
            nombre_thumb = ""
            nueva_lista = []
            for imagen in imagenes:
                if imagen['imagen_id'] == id:
                    nombre_img = imagen['imagen']
                    nombre_thumb = imagen['imagen_thumb']
                else:
                    nueva_lista.append(imagen)

            # eliminamos los archivos
            full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', nombre_img)
            full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', nombre_thumb)
            try:
                remove(full_filename)
                remove(full_filename_thumb)
            except Exception as el:
                print('no se pudo eliminar imagenes')

            request.session['session_imagenes'] = nueva_lista
            request.session.modified = True

            context_img = {
                'imagenes': nueva_lista,
            }

            return render(request, 'ventas/ventas_imagenes_lista.html', context_img)

        if operation == 'add_imagen':
            aux = request.POST['img_venta_id'].strip()
            venta_id = 0 if aux == '' else int(aux)
            aux = request.POST['img_cliente_id'].strip()
            cliente_id = 0 if aux == '' else int(aux)
            aux = request.POST['posn_1'].strip()
            posicion = 1 if aux == '' else int(aux)

            imagenes = []
            try:
                if 'imagen1' in request.FILES.keys() and request.FILES['imagen1'].name.strip() != '':
                    uploaded_filename = request.FILES['imagen1'].name

                    # full_filename = os.path.join(settings.STATIC_ROOT, 'media', 'productos', uploaded_filename)
                    system_controller = SystemController()
                    aux = system_controller.nombre_imagen('tmp', uploaded_filename)

                    full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', aux['nombre_archivo'])
                    full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', aux['nombre_archivo_thumb'])

                    fout = open(full_filename, 'wb+')
                    file_content = ContentFile(request.FILES['imagen1'].read())
                    for chunk in file_content.chunks():
                        fout.write(chunk)
                    fout.close()

                    # creamos el thumb
                    imagen = Image.open(full_filename)
                    max_size = (settings.PRODUCTOS_THUMB_WIDTH, settings.PRODUCTOS_THUMB_HEIGHT)
                    imagen.thumbnail(max_size)
                    imagen.save(full_filename_thumb)

                    # registramos
                    session_imagenes = request.session['session_imagenes']
                    dato_imagen = {}
                    dato_imagen['imagen_id'] = get_date_id()
                    dato_imagen['imagen'] = aux['nombre_archivo']
                    dato_imagen['imagen_thumb'] = aux['nombre_archivo_thumb']
                    dato_imagen['posicion'] = posicion

                    # session_imagenes.append(dato_imagen)
                    session_imagenes.insert(0, dato_imagen)
                    # print('session imagene...: ', session_imagenes)

                    #session_imagenes = sorted(session_imagenes, key=lambda imagen: imagen['posicion'])
                    # print('ordenado...:', session_imagenes)

                    request.session['session_imagenes'] = session_imagenes
                    request.session.modified = True

                # recuperamos las imagenes
                imagenes = request.session['session_imagenes']

            except Exception as ex:
                error = 1
                print('Error add imagen: ' + str(ex))

            context = {
                'imagenes': imagenes,
            }

            return render(request, 'ventas/ventas_imagenes_lista.html', context)

        # buscar cliente
        if operation == 'buscar_cliente':
            datos_cliente = cliente_controller.buscar_cliente(telefonos=request.POST['telefonos'], apellidos=request.POST['apellidos'], nombres=request.POST['nombres'])
            # print(datos_cliente)
            context_buscar = {
                'clientes': datos_cliente,
                'autenticado': 'si',
            }
            return render(request, 'ventas/clientes_buscar.html', context_buscar)

        # stock de monturas
        if operation == 'stock_monturas':
            tipo_montura_id = request.POST['tipo_montura_id'].strip()
            almacen_id = request.POST['almacen_id'].strip()

            stock_monturas = stock_controller.get_stock_montura(tipo_montura_id=tipo_montura_id, almacen_id=almacen_id, vendidas=0)
            cantidad = len(stock_monturas)

            context_stock = {
                'stock_monturas': stock_monturas,
                'autenticado': 'si',
                'cantidad': cantidad,
            }
            return render(request, 'ventas/stock_monturas.html', context_stock)

        if operation == 'add':
            respuesta = ventas_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = ventas_modificar_preventa(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_venta':
            respuesta = ventas_pasar_venta(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_venta_anular':
            respuesta = ventas_pasar_venta_anular(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'anular':
            respuesta = ventas_nullify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'cobros':
            respuesta = ventas_cobros(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_finalizado':
            respuesta = ventas_pasar_finalizado(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'pasar_finalizado_anular':
            respuesta = ventas_pasar_finalizado_anular(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'imprimir_preimpreso':
            if permisos.imprimir:
                try:
                    buffer = io.BytesIO()
                    rptVentasPreImpreso(buffer, request.user, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='venta_'+str(request.POST['id'])+'.pdf')

                except Exception as ex:
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

        if operation == 'imprimir_disenio':
            if permisos.imprimir:
                try:
                    buffer = io.BytesIO()
                    rptVentasDisenio(buffer, request.user, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='venta_'+str(request.POST['id'])+'.pdf')

                except Exception as ex:
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

        if operation == 'cobros_print':
            if permisos.imprimir:
                try:
                    buffer = io.BytesIO()
                    rptCajaIngresoRecibo(buffer, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='ci_venta_recibo.pdf')

                except Exception as ex:
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

        if operation == 'print_resumen':
            if permisos.imprimir:
                try:
                    buffer = io.BytesIO()
                    rptVentasResumen(buffer, request.user, int(request.POST['id']))

                    buffer.seek(0)
                    return FileResponse(buffer, filename='venta_resumen.pdf')

                except Exception as ex:
                    return render(request, 'pages/internal_error.html', {'error': str(ex)})

            else:
                return render(request, 'pages/without_permission.html', {})

            # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    ventas_lista = venta_controller.index(request)
    ventas_session = request.session[venta_controller.modulo_session]

    # lista de almacenes

    almacen = get_almacen_user(request.user)

    # print(zonas_session)
    context = {
        'ventas': ventas_lista,
        'session': ventas_session,
        'permisos': permisos,
        'almacen': almacen,
        'url_main': '',
        'estado_anulado': venta_controller.anulado,
        'estado_preventa': venta_controller.preventa,
        'estado_venta': venta_controller.venta,
        'estado_finalizado': venta_controller.finalizado,
        'autenticado': 'si',

        'js_file': venta_controller.modulo_session,
        'columnas': venta_controller.columnas,
        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'ventas/ventas.html', context)


# ventas add
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'adicionar'), 'without_permission')
def ventas_add(request):

    vender_fracciones = 'no'

    # guardamos
    if 'add_x' in request.POST.keys():
        if venta_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se agrego la nueva preventa'}
            request.session.modified = True
            return True
        else:
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # lista de tipos de montura
    tipos_montura_lista = lista_controller.get_lista_tipos_montura(request.user)
    almacen = get_almacen_user(request.user)
    materiales_lista = lista_controller.get_lista_materiales(request.user)
    materiales_select = []

    laboratorios_lista = lista_controller.get_lista_laboratorios(request.user)
    tecnicos_lista = lista_controller.get_lista_tecnicos(request.user)
    oftalmologos_lista = lista_controller.get_lista_oftalmologos(request.user)

    # numero actual
    system_settings = get_system_settings()
    numero_venta = system_settings['numero_actual_venta'] + 1

    # cantidad de filas
    filas = []
    for i in range(1, 51):
        filas.append(i)

    fecha_actual = get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato="dd-MMM-yyyy")
    fecha_preventa = fecha_actual

    # imagenes en session para la posible venta
    session_imagenes = []
    request.session['session_imagenes'] = session_imagenes
    request.session.modified = True

    context = {
        'url_main': '',
        'tipos_montura_lista': tipos_montura_lista,
        'materiales_lista': materiales_lista,
        'materiales_select': materiales_select,
        'laboratorios_lista': laboratorios_lista,
        'tecnicos_lista': tecnicos_lista,
        'oftalmologos_lista': oftalmologos_lista,
        'almacen': almacen,
        'filas': filas,
        'fecha_actual': fecha_actual,
        'fecha_preventa': fecha_preventa,
        'numero_venta': numero_venta,

        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'vender_fracciones': vender_fracciones,

        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation': venta_controller.preventa,
        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_preventa.html', context)


# ventas modify
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_modificar_preventa(request, venta_id):

    venta_check = apps.get_model('ventas', 'Ventas').objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = venta_check.first()
    if venta.status_id != venta_controller.status_preventa:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    if 'modify_x' in request.POST.keys():
        if venta_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'PreVentas!', 'description': 'Se modifico la preventa'}
            request.session.modified = True
            return True
        else:
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # lista de tipos de montura
    tipos_montura_lista = lista_controller.get_lista_tipos_montura(request.user)
    almacen = get_almacen_user(request.user)
    materiales_lista = lista_controller.get_lista_materiales(request.user)
    materiales_select = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta, tipo_montura_id=0)
    #print('materiales select..: ', materiales_select)

    laboratorios_lista = lista_controller.get_lista_laboratorios(request.user)
    tecnicos_lista = lista_controller.get_lista_tecnicos(request.user)
    oftalmologos_lista = lista_controller.get_lista_oftalmologos(request.user)

    # detalles
    venta_detalles = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta)
    len_detalles = len(venta_detalles)

    # verificamos el tipo de montura
    tipo_montura = {}
    tipo_montura['tipo_montura'] = ''
    tipo_montura['tipo_montura_id'] = 0

    for detalle in venta_detalles:
        if detalle.tipo_montura_id > 0:
            tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=detalle.tipo_montura_id)

    fecha_preventa = get_date_show(fecha=venta.fecha_preventa)

    # stock
    stock = {}
    cantidad_stock = 0
    stock_monturas = {}
    if venta.stock_id > 0:
        stock = apps.get_model('inventarios', 'Stock').objects.get(pk=venta.stock_id)
        stock_monturas = stock_controller.get_stock_montura(tipo_montura_id=tipo_montura.tipo_montura_id, almacen_id=venta.almacen_id.almacen_id, vendidas=0)
        cantidad_stock = len(stock_monturas)

    # imagenes
    session_imagenes = []
    ventas_imagenes = apps.get_model('ventas', 'VentasImagenes').objects.filter(venta_id=venta).order_by('venta_imagen_id')
    for imagen in ventas_imagenes:
        # copiamos a los temporales
        aux = system_controller.nombre_imagen('tmp', imagen.imagen)
        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', aux['nombre_archivo'])
        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', aux['nombre_archivo_thumb'])

        full_filename_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen.imagen)
        full_filename_thumb_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen.imagen_thumb)

        shutil.copy(full_filename_ori, full_filename)
        shutil.copy(full_filename_thumb_ori, full_filename_thumb)

        dato_imagen = {}
        dato_imagen['imagen_id'] = str(imagen.venta_imagen_id)
        dato_imagen['imagen'] = aux['nombre_archivo']
        dato_imagen['imagen_thumb'] = aux['nombre_archivo_thumb']
        dato_imagen['posicion'] = 1
        session_imagenes.append(dato_imagen)

    request.session['session_imagenes'] = session_imagenes
    request.session.modified = True

    # historias
    historias = venta_controller.get_historias(venta.cliente_id.cliente_id)

    context = {
        'session_imagenes': session_imagenes,
        'url_main': '',
        'historias': historias,
        'tipos_montura_lista': tipos_montura_lista,
        'tipo_montura': tipo_montura,
        'stock': stock,
        'cantidad_stock': cantidad_stock,
        'stock_monturas': stock_monturas,
        'almacen': almacen,
        'materiales_lista': materiales_lista,
        'fecha_preventa': fecha_preventa,
        'materiales_select': materiales_select,
        'laboratorios_lista': laboratorios_lista,
        'tecnicos_lista': tecnicos_lista,
        'oftalmologos_lista': oftalmologos_lista,

        'venta': venta,
        'venta_detalles': venta_detalles,
        'len_detalles': len_detalles,
        'numero_venta': venta.numero_venta,

        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'vender_fracciones': 'si',

        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation': venta_controller.preventa,
        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_preventa.html', context)


# ventas anular
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'anular'), 'without_permission')
def ventas_nullify(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id == venta_controller.anulado:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro ya esta anulado'}
        request.session.modified = True
        return False

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not venta_controller.permission_operation(user_perfil, 'anular'):
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    if 'anular_x' in request.POST.keys():
        if venta_controller.can_anular(venta_id, user_perfil) and venta_controller.anular(request, venta_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se anulo el registro: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    if venta_controller.can_anular(venta_id, user_perfil):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'No puede anular este registro, ' + venta_controller.error_operation})
        puede_anular = 0

    # restricciones de columna
    db_tags = {}

    # detalles
    venta_detalles = VentasDetalles.objects.filter(venta_id=venta).order_by('venta_detalle_id')

    fecha_preventa = get_date_show(fecha=venta.fecha_preventa)

    tipos_montura_lista = lista_controller.get_lista_tipos_montura(request.user)
    almacen = get_almacen_user(request.user)
    materiales_lista = lista_controller.get_lista_materiales(request.user)
    materiales_select = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta, tipo_montura_id=0)

    laboratorios_lista = lista_controller.get_lista_laboratorios(request.user)
    tecnicos_lista = lista_controller.get_lista_tecnicos(request.user)
    oftalmologos_lista = lista_controller.get_lista_oftalmologos(request.user)

    # verificamos el tipo de montura
    tipo_montura = {}
    tipo_montura['tipo_montura'] = ''
    tipo_montura['tipo_montura_id'] = 0

    for detalle in venta_detalles:
        if detalle.tipo_montura_id > 0:
            tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=detalle.tipo_montura_id)

    # stock
    stock = {}
    cantidad_stock = 0
    stock_monturas = {}
    if venta.stock_id > 0:
        stock = apps.get_model('inventarios', 'Stock').objects.get(pk=venta.stock_id)
        stock_monturas = stock_controller.get_stock_montura(tipo_montura_id=tipo_montura.tipo_montura_id, almacen_id=venta.almacen_id.almacen_id, vendidas=0)
        cantidad_stock = len(stock_monturas)

    context = {
        'url_main': '',
        'venta': venta,

        'tipos_montura_lista': tipos_montura_lista,
        'tipo_montura': tipo_montura,
        'stock': stock,
        'cantidad_stock': cantidad_stock,
        'stock_monturas': stock_monturas,
        'almacen': almacen,
        'materiales_lista': materiales_lista,
        'fecha_preventa': fecha_preventa,
        'materiales_select': materiales_select,
        'laboratorios_lista': laboratorios_lista,
        'tecnicos_lista': tecnicos_lista,
        'oftalmologos_lista': oftalmologos_lista,

        'venta_detalles': venta_detalles,
        'numero_venta': venta.numero_venta,

        'db_tags': db_tags,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    context['operation'] = venta_controller.preventa
    return render(request, 'ventas/ventas_preventa.html', context)


# ventas pasar venta
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_pasar_venta(request, venta_id):

    vender_fracciones = 'no'
    venta_check = apps.get_model('ventas', 'Ventas').objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = venta_check.first()
    if venta.status_id != venta_controller.status_preventa:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    if 'pasar_venta_x' in request.POST.keys():
        if venta_controller.save(request, type='pasar_venta'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se confirmo la venta'}
            request.session.modified = True
            return True
        else:
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # detalles
    # lista de tipos de montura
    tipos_montura_lista = lista_controller.get_lista_tipos_montura(request.user)
    almacen = get_almacen_user(request.user)
    materiales_lista = lista_controller.get_lista_materiales(request.user)
    materiales_select = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta, tipo_montura_id=0)

    laboratorios_lista = lista_controller.get_lista_laboratorios(request.user)
    tecnicos_lista = lista_controller.get_lista_tecnicos(request.user)
    oftalmologos_lista = lista_controller.get_lista_oftalmologos(request.user)

    # detalles
    venta_detalles = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta)
    len_detalles = len(venta_detalles)

    # verificamos el tipo de montura
    tipo_montura = {}
    tipo_montura['tipo_montura'] = ''
    tipo_montura['tipo_montura_id'] = 0

    for detalle in venta_detalles:
        if detalle.tipo_montura_id > 0:
            tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=detalle.tipo_montura_id)

    fecha_preventa = get_date_show(fecha=venta.fecha_preventa)

    # stock
    stock = {}
    cantidad_stock = 0
    stock_monturas = {}
    if venta.stock_id > 0:
        stock = apps.get_model('inventarios', 'Stock').objects.get(pk=venta.stock_id)
        stock_monturas = stock_controller.get_stock_montura(tipo_montura_id=tipo_montura.tipo_montura_id, almacen_id=venta.almacen_id.almacen_id, vendidas=0)
        cantidad_stock = len(stock_monturas)

    fecha_actual = get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato="dd-MMM-yyyy")

    caja_lista = caja_controller.cash_active(current_date(), request.user, formato_ori='yyyy-mm-dd')

    if not caja_lista:
        # no tiene caja activa
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'Debe tener una caja activa'}
        request.session.modified = True
        return False

    caja_usuario = caja_lista[0]

    # imagenes
    session_imagenes = []
    ventas_imagenes = apps.get_model('ventas', 'VentasImagenes').objects.filter(venta_id=venta).order_by('venta_imagen_id')
    for imagen in ventas_imagenes:
        # copiamos a los temporales
        aux = system_controller.nombre_imagen('tmp', imagen.imagen)
        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', aux['nombre_archivo'])
        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', aux['nombre_archivo_thumb'])

        full_filename_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen.imagen)
        full_filename_thumb_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen.imagen_thumb)

        shutil.copy(full_filename_ori, full_filename)
        shutil.copy(full_filename_thumb_ori, full_filename_thumb)

        dato_imagen = {}
        dato_imagen['imagen_id'] = str(imagen.venta_imagen_id)
        dato_imagen['imagen'] = aux['nombre_archivo']
        dato_imagen['imagen_thumb'] = aux['nombre_archivo_thumb']
        dato_imagen['posicion'] = 1
        session_imagenes.append(dato_imagen)

    request.session['session_imagenes'] = session_imagenes
    request.session.modified = True

    # historias
    historias = venta_controller.get_historias(venta.cliente_id.cliente_id)

    context = {
        'url_main': '',
        'session_imagenes': session_imagenes,
        'historias': historias,
        'caja_usuario': caja_usuario,
        'fecha_actual': fecha_actual,
        'tipos_montura_lista': tipos_montura_lista,
        'tipo_montura': tipo_montura,
        'stock': stock,
        'cantidad_stock': cantidad_stock,
        'stock_monturas': stock_monturas,
        'almacen': almacen,
        'materiales_lista': materiales_lista,
        'fecha_preventa': fecha_preventa,
        'materiales_select': materiales_select,
        'laboratorios_lista': laboratorios_lista,
        'tecnicos_lista': tecnicos_lista,
        'oftalmologos_lista': oftalmologos_lista,

        'venta': venta,
        'venta_detalles': venta_detalles,
        'len_detalles': len_detalles,
        'numero_venta': venta.numero_venta,

        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'vender_fracciones': vender_fracciones,

        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation': venta_controller.venta,
        'operation_x': 'pasar_venta',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_venta.html', context)


# pasar venta anular
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'anular'), 'without_permission')
def ventas_pasar_venta_anular(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id != venta_controller.venta:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro no es una venta confirmada'}
        request.session.modified = True
        return False

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not venta_controller.permission_operation(user_perfil, 'anular'):
        return render(request, 'pages/without_permission.html', {})

    # confirma anulacion
    if 'anular_x' in request.POST.keys():
        if venta_controller.can_anular(venta_id, user_perfil) and venta_controller.anular(request, venta_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se anulo la venta: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    if venta_controller.can_anular(venta_id, user_perfil):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'No puede anular este registro, ' + venta_controller.error_operation})
        puede_anular = 0

    # restricciones de columna
    db_tags = {}

    # detalles
    numero_venta = venta.numero_venta
    fecha_preventa = get_date_show(fecha=venta.fecha_preventa)

    tipos_montura_lista = lista_controller.get_lista_tipos_montura(request.user)
    almacen = get_almacen_user(request.user)
    materiales_lista = lista_controller.get_lista_materiales(request.user)
    materiales_select = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta, tipo_montura_id=0)

    laboratorios_lista = lista_controller.get_lista_laboratorios(request.user)
    tecnicos_lista = lista_controller.get_lista_tecnicos(request.user)
    oftalmologos_lista = lista_controller.get_lista_oftalmologos(request.user)

    # detalles
    venta_detalles = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta)

    # verificamos el tipo de montura
    tipo_montura = {}
    tipo_montura['tipo_montura'] = ''
    tipo_montura['tipo_montura_id'] = 0

    for detalle in venta_detalles:
        if detalle.tipo_montura_id > 0:
            tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=detalle.tipo_montura_id)

    # stock
    stock = {}
    cantidad_stock = 0
    stock_monturas = {}
    if venta.stock_id > 0:
        stock = apps.get_model('inventarios', 'Stock').objects.get(pk=venta.stock_id)
        stock_monturas = stock_controller.get_stock_montura(tipo_montura_id=tipo_montura.tipo_montura_id, almacen_id=venta.almacen_id.almacen_id, vendidas=0)
        cantidad_stock = len(stock_monturas)

    # verificamos si tiene plan de pagos
    plan_pagos = {}
    plan_pagos['plan_pago_id'] = 0
    plan_pagos['numero_cuotas'] = 0
    plan_pagos['tiempo_dias'] = 0
    fecha_actual = get_date_show(fecha=current_date(), formato_ori='yyyy-mm-dd', formato="dd-MMM-yyyy")
    if venta.plan_pago == 1:
        plan_pagos = apps.get_model('ventas', 'PlanPagos').objects.get(venta_id=venta, status_id=venta_controller.status_activo)
        fecha_actual = get_date_show(fecha=plan_pagos.fecha)

    context = {
        'url_main': '',
        'venta': venta,
        'venta_detalles': venta_detalles,
        'db_tags': db_tags,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',
        'plan_pagos': plan_pagos,
        'fecha_actual': fecha_actual,

        'fecha_preventa': fecha_preventa,
        'numero_venta': numero_venta,

        'tipos_montura_lista': tipos_montura_lista,
        'tipo_montura': tipo_montura,
        'stock': stock,
        'cantidad_stock': cantidad_stock,
        'stock_monturas': stock_monturas,
        'almacen': almacen,
        'materiales_lista': materiales_lista,
        'materiales_select': materiales_select,
        'laboratorios_lista': laboratorios_lista,
        'tecnicos_lista': tecnicos_lista,
        'oftalmologos_lista': oftalmologos_lista,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'pasar_venta_anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    context['operation'] = venta_controller.venta
    return render(request, 'ventas/ventas_venta.html', context)

# gastos sobre la venta


@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_gastos(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id not in [venta_controller.venta, venta_controller.salida_almacen, venta_controller.vuelta_almacen]:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro debe estar activo'}
        request.session.modified = True
        return False

    caja_lista = caja_controller.cash_active(current_date(), request.user, formato_ori='yyyy-mm-dd')

    if not caja_lista:
        # no tiene caja activa
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'Debe tener una caja activa'}
        request.session.modified = True
        return False

    caja_usuario = caja_lista[0]

    # confirma adicion gasto
    if 'gastos_x' in request.POST.keys():
        if venta_controller.add_gasto(venta_id, caja_usuario, request):
            # request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se adiciono el gasto correctamente'}
            # request.session.modified = True
            # return True
            messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Gastos!', 'description': 'se adiciono el gasto correctamente'})
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # confirma anulacion gasto
    if 'operation_x2' in request.POST.keys():
        operation2 = request.POST['operation_x2']
        if operation2 == 'gastos_anular_x':
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            if not venta_controller.permission_operation(user_perfil, 'anular'):
                return render(request, 'pages/without_permission.html', {})

            if venta_controller.anular_gasto(venta_id, caja_usuario, request):
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Gastos!', 'description': 'se anulo el gasto correctamente'})
            else:
                # error al modificar
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    # lista de gastos
    saldo_dia = caja_controller.day_balance(fecha=current_date(), Cajas=caja_usuario, formato_ori='yyyy-mm-dd')
    saldo_caja = saldo_dia[caja_usuario.caja_id]

    lista_gastos = apps.get_model('cajas', 'CajasEgresos').objects.filter(venta_id=venta.venta_id).order_by('caja_egreso_id')
    fecha_actual = get_date_show(fecha=current_date(), formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

    context = {
        'url_main': '',
        'venta': venta,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',
        'lista_gastos': lista_gastos,
        'estado_anulado': venta_controller.anulado,
        'caja_usuario': caja_usuario,
        'saldo_caja': saldo_caja,
        'fecha_actual': fecha_actual,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'gastos',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_gastos.html', context)


# cobros sobre la venta
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_cobros(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id not in [venta_controller.venta]:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro debe estar activo'}
        request.session.modified = True
        return False

    caja_lista = caja_controller.cash_active(current_date(), request.user, formato_ori='yyyy-mm-dd')

    if not caja_lista:
        # no tiene caja activa
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'Debe tener una caja activa'}
        request.session.modified = True
        return False

    caja_usuario = caja_lista[0]

    # confirma adicion gasto
    if 'cobros_x' in request.POST.keys():
        if venta_controller.add_cobro(venta_id, caja_usuario, request):
            messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Cobros!', 'description': 'se adiciono el cobro correctamente'})
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Cobros!', 'description': venta_controller.error_operation})

    # confirma anulacion gasto
    if 'operation_x2' in request.POST.keys():
        operation2 = request.POST['operation_x2']
        if operation2 == 'cobros_anular_x':
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            if not venta_controller.permission_operation(user_perfil, 'anular'):
                return render(request, 'pages/without_permission.html', {})

            if venta_controller.anular_cobro(venta_id, caja_usuario, request):
                messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Gastos!', 'description': 'se anulo el cobro correctamente'})
            else:
                # error al modificar
                messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    saldo_inicial = venta.total
    saldo_venta = saldo_inicial

    # lista de gastos
    lista_gastos = apps.get_model('cajas', 'CajasEgresos').objects.filter(venta_id=venta.venta_id).order_by('caja_egreso_id')
    fecha_actual = get_date_show(fecha=current_date(), formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')
    # lista de ingresos
    lista_ingresos = apps.get_model('cajas', 'CajasIngresos').objects.filter(venta_id=venta.venta_id).order_by('caja_ingreso_id')

    # lista de aumentos
    # lista_aumentos = apps.get_model('ventas', 'VentasAumentos').objects.filter(venta_id=venta, status_id=venta_controller.status_activo).order_by('venta_aumento_id')

    total_gastos = 0
    for gasto in lista_gastos:
        if gasto.status_id == venta_controller.status_activo:
            saldo_venta = saldo_venta + gasto.monto
            total_gastos += gasto.monto

    total_cobros = 0
    for ingreso in lista_ingresos:
        if ingreso.status_id == venta_controller.status_activo:
            saldo_venta = saldo_venta - ingreso.monto
            total_cobros += ingreso.monto

    context = {
        'url_main': '',
        'venta': venta,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',
        'lista_gastos': lista_gastos,
        'lista_ingresos': lista_ingresos,
        'saldo_venta': saldo_venta,
        'saldo_inicial': saldo_inicial,
        'total_gastos': total_gastos,
        'total_cobros': total_cobros,
        'estado_anulado': venta_controller.anulado,
        'caja_usuario': caja_usuario,
        'fecha_actual': fecha_actual,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'cobros',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_cobros.html', context)


# pasar a estado finalizado
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'modificar'), 'without_permission')
def ventas_pasar_finalizado(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id != venta_controller.venta:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro debe ser una venta'}
        request.session.modified = True
        return False

    # confirma adicion gasto
    if 'pasar_finalizado_x' in request.POST.keys():
        if venta_controller.save(request, type='finalizado'):
            # messages.add_message(request, messages.SUCCESS, {'type': 'success', 'title': 'Finalizado!', 'description': 'se finalizo la venta correctamente'})
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se realizo la finalizacion de la venta'}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Finalizado!', 'description': venta_controller.error_operation})

    saldo_venta = venta_controller.saldo_venta(venta_id)

    caja_lista = caja_controller.cash_active(current_date(), request.user, formato_ori='yyyy-mm-dd')

    if not caja_lista:
        if venta.plan_pago == 1:
            # no tiene caja activa
            request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'Debe tener una caja activa'}
            request.session.modified = True
            return False

    caja_usuario = caja_lista[0]

    # imagenes
    session_imagenes = []
    ventas_imagenes = apps.get_model('ventas', 'VentasImagenes').objects.filter(venta_id=venta).order_by('venta_imagen_id')
    for imagen in ventas_imagenes:
        # copiamos a los temporales
        aux = system_controller.nombre_imagen('tmp', imagen.imagen)
        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', aux['nombre_archivo'])
        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', aux['nombre_archivo_thumb'])

        full_filename_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen.imagen)
        full_filename_thumb_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen.imagen_thumb)

        shutil.copy(full_filename_ori, full_filename)
        shutil.copy(full_filename_thumb_ori, full_filename_thumb)

        dato_imagen = {}
        dato_imagen['imagen_id'] = str(imagen.venta_imagen_id)
        dato_imagen['imagen'] = aux['nombre_archivo']
        dato_imagen['imagen_thumb'] = aux['nombre_archivo_thumb']
        dato_imagen['posicion'] = 1
        session_imagenes.append(dato_imagen)

    request.session['session_imagenes'] = session_imagenes
    request.session.modified = True

    context = {
        'url_main': '',
        'session_imagenes': session_imagenes,
        'venta': venta,
        'caja_usuario': caja_usuario,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',
        'saldo_venta': saldo_venta,
        'estado_anulado': venta_controller.anulado,

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'pasar_finalizado',
        'operation_x2': '',
        'operation_x3': '',
        'operation': venta_controller.finalizado,

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/ventas_finalizar.html', context)


# pasar finalizado anular
@ user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_VENTAS, 'anular'), 'without_permission')
def ventas_pasar_finalizado_anular(request, venta_id):
    # url modulo
    venta_check = Ventas.objects.filter(pk=venta_id)
    if not venta_check:
        return render(request, 'pages/without_permission.html', {})

    venta = Ventas.objects.get(pk=venta_id)

    # verificamos el estado
    if venta.status_id.status_id != venta_controller.finalizado:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Ventas!', 'description': 'El registro no es una venta finalizada'}
        request.session.modified = True
        return False

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not venta_controller.permission_operation(user_perfil, 'anular'):
        return render(request, 'pages/without_permission.html', {})

    # confirma anulacion
    if 'anular_x' in request.POST.keys():
        if venta_controller.can_anular(venta_id, user_perfil) and venta_controller.anular(request, venta_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Ventas!', 'description': 'Se anulo la venta: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': venta_controller.error_operation})

    if venta_controller.can_anular(venta_id, user_perfil):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Ventas!', 'description': 'No puede anular este registro, ' + venta_controller.error_operation})
        puede_anular = 0

    saldo_venta = venta_controller.saldo_venta(venta_id)

    context = {
        'url_main': '',
        'venta': venta,
        'saldo_venta': saldo_venta,
        'control_form': venta_controller.control_form,
        'js_file': venta_controller.modulo_session,
        'puede_anular': puede_anular,
        'error_anular': venta_controller.error_operation,
        'autenticado': 'si',

        'module_x': settings.MOD_VENTAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'pasar_finalizado_anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': venta_id,
        'id2': '',
        'id3': '',
    }

    context['operation'] = venta_controller.finalizado
    return render(request, 'ventas/ventas_finalizar.html', context)
