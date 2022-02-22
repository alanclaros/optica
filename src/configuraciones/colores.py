from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.conf import settings
from django.contrib import messages

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# clases
from controllers.configuraciones.ColoresController import ColoresController

# controlador del modulo
color_controller = ColoresController()

mod_settings = color_controller.modulo_id
modelo_name = color_controller.modelo_name
app_name = color_controller.modelo_app
msg_title = "Colores!"
msg_description = "este color"
col_name = "color"
col_name_id = "color_id"


# list
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'lista'), 'without_permission')
def colores_index(request):
    permisos = get_permissions_user(request.user, mod_settings)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete', 'mostrar_imagen']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = colores_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = colores_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = colores_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    lista = color_controller.index(request)
    session = request.session[color_controller.modulo_session]
    # print(zonas_session)
    context = {
        'lista': lista,
        'session': session,
        'permisos': permisos,
        'autenticado': 'si',

        'columnas': color_controller.columnas,

        'js_file': color_controller.modulo_session,
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
    return render(request, 'configuraciones/colores.html', context)


# add
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'adicionar'), 'without_permission')
def colores_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if color_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': msg_title, 'description': 'Se agrego ' + msg_description + ': '+request.POST[col_name]}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': color_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), '', request, None, col_name, 'codigo', 'color_hex')
    else:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), '', None, None, col_name, 'codigo', 'color_hex')

    context = {
        'url_main': 'url_main',
        'operation_x': 'add',
        'db_tags': db_tags,
        'control_form': color_controller.control_form,
        'js_file': color_controller.modulo_session,
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
    return render(request, 'configuraciones/colores_form.html', context)


# modify
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'modificar'), 'without_permission')
def colores_modify(request, color_id):
    # url modulo
    objeto_check = apps.get_model(app_name, modelo_name).objects.filter(pk=color_id)
    if not objeto_check:
        return render(request, 'pages/without_permission.html', {})

    objeto = apps.get_model(app_name, modelo_name).objects.get(pk=color_id)

    if objeto.status_id not in [color_controller.status_activo, color_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if color_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': msg_title, 'description': 'Se modifico ' + msg_description + ': '+request.POST[col_name]}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': color_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), '', request, objeto, col_name, 'codigo', 'color_hex')
    else:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), '', None, objeto, col_name, 'codigo', 'color_hex')

    context = {
        'url_main': 'url_main',
        'operation_x': 'modify',
        'objeto': objeto,
        'db_tags': db_tags,
        'control_form': color_controller.control_form,
        'js_file': color_controller.modulo_session,
        'status_active': color_controller.activo,
        'autenticado': 'si',

        'module_x': mod_settings,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': color_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/colores_form.html', context)


# delete
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'eliminar'), 'without_permission')
def colores_delete(request, color_id):
    # url modulo
    objeto_check = apps.get_model(app_name, modelo_name).objects.filter(pk=color_id)
    if not objeto_check:
        return render(request, 'pages/without_permission.html', {})

    objeto = apps.get_model(app_name, modelo_name).objects.get(pk=color_id)

    if objeto.status_id not in [color_controller.status_activo, color_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if color_controller.can_delete(col_name_id, color_id, **color_controller.modelos_eliminar) and color_controller.delete(color_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': msg_title, 'description': 'Se elimino ' + msg_description + ': '+request.POST[col_name]}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': color_controller.error_operation})

    if color_controller.can_delete(col_name_id, color_id, **color_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': 'No puede eliminar ' + msg_description + ', ' + color_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), '', request, objeto, col_name, 'codigo', 'color_hex')
    else:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), '', None, objeto, col_name, 'codigo', 'color_hex')

    context = {
        'url_main': '',
        'operation_x': 'delete',
        'objeto': objeto,
        'db_tags': db_tags,
        'control_form': color_controller.control_form,
        'js_file': color_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': color_controller.error_operation,
        'status_active': color_controller.activo,
        'autenticado': 'si',

        'module_x': mod_settings,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': color_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/colores_form.html', context)
