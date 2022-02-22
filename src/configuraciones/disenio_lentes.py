from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.conf import settings
from django.contrib import messages

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# clases
from controllers.configuraciones.DisenioLentesController import DisenioLentesController

# controlador del modulo
disenio_lentes_controller = DisenioLentesController()

mod_settings = disenio_lentes_controller.modulo_id
modelo_name = disenio_lentes_controller.modelo_name
app_name = disenio_lentes_controller.modelo_app
msg_title = "Dise&#241;o Lentes!"
msg_description = "este dise&#241;o de lente"
col_name = "disenio_lente"
col_name_id = "disenio_lente_id"


# list
# list
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'lista'), 'without_permission')
def disenio_lentes_index(request):
    permisos = get_permissions_user(request.user, mod_settings)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete', 'mostrar_imagen']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = disenio_lentes_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = disenio_lentes_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = disenio_lentes_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'mostrar_imagen':
            imagen = apps.get_model(app_name, modelo_name).objects.get(pk=int(request.POST['id']))
            context_img = {
                'imagen': imagen,
                'autenticado': 'si',
            }
            return render(request, 'configuraciones/disenio_lentes_imagen_mostrar.html', context_img)

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    lista = disenio_lentes_controller.index(request)
    session = request.session[disenio_lentes_controller.modulo_session]
    # print(zonas_session)
    context = {
        'lista': lista,
        'session': session,
        'permisos': permisos,
        'autenticado': 'si',

        'columnas': disenio_lentes_controller.columnas,

        'js_file': disenio_lentes_controller.modulo_session,
        'module_x': mod_settings,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/disenio_lentes.html', context)


# add
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'adicionar'), 'without_permission')
def disenio_lentes_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if disenio_lentes_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': msg_title, 'description': 'Se agrego ' + msg_description + ': '+request.POST[col_name]}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': disenio_lentes_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), 'descripcion', request, None, col_name, 'codigo', 'descripcion')
    else:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), 'descripcion', None, None, col_name, 'codigo', 'descripcion')

    context = {
        'url_main': 'url_main',
        'operation_x': 'add',
        'db_tags': db_tags,
        'control_form': disenio_lentes_controller.control_form,
        'js_file': disenio_lentes_controller.modulo_session,
        'autenticado': 'si',

        'module_x': mod_settings,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/disenio_lentes_form.html', context)


# modify
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'modificar'), 'without_permission')
def disenio_lentes_modify(request, disenio_lente_id):
    # url modulo
    objeto_check = apps.get_model(app_name, modelo_name).objects.filter(pk=disenio_lente_id)
    if not objeto_check:
        return render(request, 'pages/without_permission.html', {})

    objeto = apps.get_model(app_name, modelo_name).objects.get(pk=disenio_lente_id)

    if objeto.status_id not in [disenio_lentes_controller.status_activo, disenio_lentes_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if disenio_lentes_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': msg_title, 'description': 'Se modifico ' + msg_description + ': '+request.POST[col_name]}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': disenio_lentes_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), 'descripcion', request, objeto, col_name, 'codigo', 'descripcion')
    else:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), 'descripcion', None, objeto, col_name, 'codigo', 'descripcion')

    context = {
        'url_main': 'url_main',
        'operation_x': 'modify',
        'objeto': objeto,
        'db_tags': db_tags,
        'control_form': disenio_lentes_controller.control_form,
        'js_file': disenio_lentes_controller.modulo_session,
        'status_active': disenio_lentes_controller.activo,
        'autenticado': 'si',

        'module_x': mod_settings,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': disenio_lente_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/disenio_lentes_form.html', context)


# delete
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'eliminar'), 'without_permission')
def disenio_lentes_delete(request, disenio_lente_id):
    # url modulo
    objeto_check = apps.get_model(app_name, modelo_name).objects.filter(pk=disenio_lente_id)
    if not objeto_check:
        return render(request, 'pages/without_permission.html', {})

    objeto = apps.get_model(app_name, modelo_name).objects.get(pk=disenio_lente_id)

    if objeto.status_id not in [disenio_lentes_controller.status_activo, disenio_lentes_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if disenio_lentes_controller.can_delete(col_name_id, disenio_lente_id, **disenio_lentes_controller.modelos_eliminar) and disenio_lentes_controller.delete(disenio_lente_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': msg_title, 'description': 'Se elimino ' + msg_description + ': '+request.POST[col_name]}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': disenio_lentes_controller.error_operation})

    if disenio_lentes_controller.can_delete(col_name_id, disenio_lente_id, **disenio_lentes_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': 'No puede eliminar ' + msg_description + ', ' + disenio_lentes_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), 'descripcion', request, objeto, col_name, 'codigo', 'descripcion')
    else:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), 'descripcion', None, objeto, col_name, 'codigo', 'descripcion')

    context = {
        'url_main': '',
        'operation_x': 'delete',
        'objeto': objeto,
        'db_tags': db_tags,
        'control_form': disenio_lentes_controller.control_form,
        'js_file': disenio_lentes_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': disenio_lentes_controller.error_operation,
        'status_active': disenio_lentes_controller.activo,
        'autenticado': 'si',

        'module_x': mod_settings,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': disenio_lente_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/disenio_lentes_form.html', context)
