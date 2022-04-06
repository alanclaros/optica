from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.conf import settings
from django.contrib import messages

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# clases
from controllers.configuraciones.LaboratoriosController import LaboratoriosController

# controlador del modulo
laboratorio_controller = LaboratoriosController()

mod_settings = laboratorio_controller.modulo_id
modelo_name = laboratorio_controller.modelo_name
app_name = laboratorio_controller.modelo_app
msg_title = "Laboratorios!"
msg_description = "este laboratorio"
col_name = "laboratorio"
col_name_id = "laboratorio_id"


# list
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'lista'), 'without_permission')
def laboratorios_index(request):
    permisos = get_permissions_user(request.user, mod_settings)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete', 'mostrar_imagen']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = laboratorios_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = laboratorios_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = laboratorios_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'mostrar_imagen':
            imagen = apps.get_model(app_name, modelo_name).objects.get(pk=int(request.POST['id']))
            context_img = {
                'imagen': imagen,
                'autenticado': 'si',
            }
            return render(request, 'configuraciones/laboratorios_imagen_mostrar.html', context_img)

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    lista = laboratorio_controller.index(request)
    session = request.session[laboratorio_controller.modulo_session]
    # print(zonas_session)
    context = {
        'lista': lista,
        'session': session,
        'permisos': permisos,
        'autenticado': 'si',

        'columnas': laboratorio_controller.columnas,

        'js_file': laboratorio_controller.modulo_session,
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
    return render(request, 'configuraciones/laboratorios.html', context)


# add
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'adicionar'), 'without_permission')
def laboratorios_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if laboratorio_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': msg_title, 'description': 'Se agrego ' + msg_description + ': '+request.POST[col_name]}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': laboratorio_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), 'descripcion', request, None, col_name, 'codigo', 'descripcion')
    else:
        db_tags = get_html_column(apps.get_model(app_name, modelo_name), 'descripcion', None, None, col_name, 'codigo', 'descripcion')

    context = {
        'url_main': 'url_main',
        'operation_x': 'add',
        'db_tags': db_tags,
        'control_form': laboratorio_controller.control_form,
        'js_file': laboratorio_controller.modulo_session,
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
    return render(request, 'configuraciones/laboratorios_form.html', context)


# modify
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'modificar'), 'without_permission')
def laboratorios_modify(request, color_id):
    # url modulo
    objeto_check = apps.get_model(app_name, modelo_name).objects.filter(pk=color_id)
    if not objeto_check:
        return render(request, 'pages/without_permission.html', {})

    objeto = apps.get_model(app_name, modelo_name).objects.get(pk=color_id)

    if objeto.status_id not in [laboratorio_controller.status_activo, laboratorio_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if laboratorio_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': msg_title, 'description': 'Se modifico ' + msg_description + ': '+request.POST[col_name]}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': laboratorio_controller.error_operation})

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
        'control_form': laboratorio_controller.control_form,
        'js_file': laboratorio_controller.modulo_session,
        'status_active': laboratorio_controller.activo,
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
    return render(request, 'configuraciones/laboratorios_form.html', context)


# delete
@user_passes_test(lambda user: get_user_permission_operation(user, mod_settings, 'eliminar'), 'without_permission')
def laboratorios_delete(request, color_id):
    # url modulo
    objeto_check = apps.get_model(app_name, modelo_name).objects.filter(pk=color_id)
    if not objeto_check:
        return render(request, 'pages/without_permission.html', {})

    objeto = apps.get_model(app_name, modelo_name).objects.get(pk=color_id)

    if objeto.status_id not in [laboratorio_controller.status_activo, laboratorio_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if laboratorio_controller.can_delete(col_name_id, color_id, **laboratorio_controller.modelos_eliminar) and laboratorio_controller.delete(color_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': msg_title, 'description': 'Se elimino ' + msg_description + ': '+request.POST[col_name]}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': laboratorio_controller.error_operation})

    if laboratorio_controller.can_delete(col_name_id, color_id, **laboratorio_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': msg_title, 'description': 'No puede eliminar ' + msg_description + ', ' + laboratorio_controller.error_operation})
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
        'control_form': laboratorio_controller.control_form,
        'js_file': laboratorio_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': laboratorio_controller.error_operation,
        'status_active': laboratorio_controller.activo,
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
    return render(request, 'configuraciones/laboratorios_form.html', context)
