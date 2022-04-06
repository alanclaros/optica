from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.apps import apps
# settings de la app
from django.conf import settings

# para los usuarios
from utils.permissions import get_user_permission_operation, get_permissions_user
from utils.dates_functions import next_periodo, previous_periodo, fecha_periodo, get_date_show

# clases por modulo
from controllers.ventas.PedidosController import PedidosController
import io
from django.http import FileResponse
from reportes.ventas.rptPedidoCliente import rptPedidoCliente

pedido_controller = PedidosController()


# pedidos
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PEDIDOS, 'lista'), 'without_permission')
def pedidos_cliente_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_PEDIDOS)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'marcar_pedido', 'anular', 'print']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'marcar_pedido':
            respuesta = pedidos_cliente_marcar(request, int(request.POST['id']))
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'anular':
            respuesta = pedidos_cliente_nullify(request, int(request.POST['id']))
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'print':
            if permisos.imprimir:
                buffer = io.BytesIO()
                rptPedidoCliente(buffer, request.user, int(request.POST['id']))

                buffer.seek(0)
                # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
                return FileResponse(buffer, filename='pedido.pdf')
            else:
                return render(request, 'pages/without_permission.html', {})

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto

    # print(Ciudades)
    pedidos_lista = pedido_controller.index(request)
    pedidos_session = request.session[pedido_controller.modulo_session]

    # print(zonas_session)
    context = {
        'lista_pedidos': pedidos_lista,
        'session': pedidos_session,
        'permisos': permisos,
        'estado_anulado': pedido_controller.anulado,
        'estado_activo': pedido_controller.activo,
        'estado_finalizado': pedido_controller.finalizado,
        'autenticado': 'si',

        'columnas': pedido_controller.columnas,
        'module_x': settings.MOD_PEDIDOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'ventas/pedidos.html', context)


# pedidos marcar
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PEDIDOS, 'modificar'), 'without_permission')
def pedidos_cliente_marcar(request, pedido_id):
    pedido_check = apps.get_model('pedidos', 'Pedidos').objects.filter(pk=pedido_id)
    if not pedido_check:
        return render(request, 'pages/without_permission.html', {})

    pedido = pedido_check.first()
    if pedido.status_id != pedido_controller.status_activo:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'marcar_pedido_x' in request.POST.keys():
        if pedido_controller.pedidos_cliente_marcar(request, pedido_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Pedidos Cliente!', 'description': 'Se marco el pedido: ' + request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Pedidos Cliente!', 'description': pedido_controller.error_operation})

    db_tags = {}

    # datos del pedido
    datos_pedido = pedido_controller.get_pedido(pedido_id)

    context = {

        'datos_pedido': datos_pedido,
        'db_tags': db_tags,
        'control_form': pedido_controller.control_form,

        'autenticado': 'si',
        'status_finalizado': pedido_controller.finalizado,

        'module_x': settings.MOD_PEDIDOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'marcar_pedido',
        'operation_x2': '',
        'operation_x3': '',

        'id': pedido_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'ventas/pedidos_form.html', context)


# pedidos cliente anular
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_PEDIDOS, 'anular'), 'without_permission')
def pedidos_cliente_nullify(request, pedido_id):
    # url modulo
    pedido_check = apps.get_model('pedidos', 'Pedidos').objects.filter(pk=pedido_id)
    if not pedido_check:
        return render(request, 'pages/without_permission.html', {})

    pedido = apps.get_model('pedidos', 'Pedidos').objects.get(pk=pedido_id)

    # verificamos el estado
    if pedido.status_id.status_id == pedido_controller.anulado:
        request.session['nuevo_mensaje'] = {'type': 'warning', 'title': 'Pedidos!', 'description': 'El registro ya esta anulado'}
        request.session.modified = True
        return False

    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
    if not pedido_controller.permission_operation(user_perfil, 'anular'):
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    if 'anular_x' in request.POST.keys():
        if pedido_controller.can_anular(pedido_id, request.user) and pedido_controller.anular(request, pedido_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Pedidos!', 'description': 'Se anulo el registro: '+request.POST['id']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Pedidos!', 'description': pedido_controller.error_operation})

    if pedido_controller.can_anular(pedido_id, request.user):
        puede_anular = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Pedidos!', 'description': 'No puede anular este registro, ' + pedido_controller.error_operation})
        puede_anular = 0

    # restricciones de columna
    db_tags = {}

    # datos del pedido
    datos_pedido = pedido_controller.get_pedido(pedido_id)

    context = {
        'url_main': '',
        'datos_pedido': datos_pedido,

        'db_tags': db_tags,
        'control_form': pedido_controller.control_form,
        'puede_anular': puede_anular,
        'autenticado': 'si',

        'module_x': settings.MOD_PEDIDOS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'anular',
        'operation_x2': '',
        'operation_x3': '',

        'id': pedido_id,
        'id2': '',
        'id3': '',
    }

    return render(request, 'ventas/pedidos_form.html', context)
