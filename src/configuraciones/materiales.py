from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.conf import settings
from django.contrib import messages

# utils
from utils.permissions import get_user_permission_operation, get_permissions_user, get_html_column

# clases
from controllers.configuraciones.MaterialesController import MaterialesController

# modelo
from configuraciones.models import Materiales

# controlador del modulo
material_controller = MaterialesController()


# materiales
# materiales
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_MATERIALES, 'lista'), 'without_permission')
def materiales_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_MATERIALES)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add', 'modify', 'delete', 'mostrar_imagen']:
            return render(request, 'pages/without_permission.html', {})

        if operation == 'add':
            respuesta = materiales_add(request)
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'modify':
            respuesta = materiales_modify(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'delete':
            respuesta = materiales_delete(request, request.POST['id'])
            if not type(respuesta) == bool:
                return respuesta

        if operation == 'mostrar_imagen':
            imagen = Materiales.objects.get(pk=int(request.POST['id']))
            context_img = {
                'imagen': imagen,
                'autenticado': 'si',
            }
            return render(request, 'configuraciones/materiales_imagen_mostrar.html', context_img)

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    materiales_lista = material_controller.index(request)
    materiales_session = request.session[material_controller.modulo_session]
    # print(zonas_session)
    context = {
        'materiales': materiales_lista,
        'session': materiales_session,
        'permisos': permisos,
        'autenticado': 'si',

        'columnas': material_controller.columnas,

        'js_file': material_controller.modulo_session,
        'module_x': settings.MOD_MATERIALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/materiales.html', context)


# materiales add
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_MATERIALES, 'adicionar'), 'without_permission')
def materiales_add(request):

    # guardamos
    existe_error = False
    if 'add_x' in request.POST.keys():
        if material_controller.save(request, type='add'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Materiales!', 'description': 'Se agrego el nuevo material: '+request.POST['material']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Materiales!', 'description': material_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Materiales'), 'descripcion', request, None, 'material', 'codigo', 'descripcion')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Materiales'), 'descripcion', None, None, 'material', 'codigo', 'descripcion')

    context = {
        'url_main': 'url_main',
        'operation_x': 'add',
        'db_tags': db_tags,
        'control_form': material_controller.control_form,
        'js_file': material_controller.modulo_session,
        'autenticado': 'si',

        'module_x': settings.MOD_MATERIALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'add',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/materiales_form.html', context)


# materiales modify
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_MATERIALES, 'modificar'), 'without_permission')
def materiales_modify(request, material_id):
    # url modulo
    material_check = Materiales.objects.filter(pk=material_id)
    if not material_check:
        return render(request, 'pages/without_permission.html', {})

    material = apps.get_model('configuraciones', 'Materiales').objects.get(pk=material_id)

    if material.status_id not in [material_controller.status_activo, material_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # guardamos
    existe_error = False
    if 'modify_x' in request.POST.keys():
        if material_controller.save(request, type='modify'):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Materiales!', 'description': 'Se modifico el material: '+request.POST['material']}
            request.session.modified = True
            return True
        else:
            # error al adicionar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Materiales!', 'description': material_controller.error_operation})

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Materiales'), 'descripcion', request, material, 'material', 'codigo', 'descripcion')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Materiales'), 'descripcion', None, material, 'material', 'codigo', 'descripcion')

    context = {
        'url_main': 'url_main',
        'operation_x': 'modify',
        'material': material,
        'db_tags': db_tags,
        'control_form': material_controller.control_form,
        'js_file': material_controller.modulo_session,
        'status_active': material_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_MATERIALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'modify',
        'operation_x2': '',
        'operation_x3': '',

        'id': material_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/materiales_form.html', context)


# materiales delete
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_MATERIALES, 'eliminar'), 'without_permission')
def materiales_delete(request, material_id):
    # url modulo
    material_check = Materiales.objects.filter(pk=material_id)
    if not material_check:
        return render(request, 'pages/without_permission.html', {})

    material = apps.get_model('configuraciones', 'Materiales').objects.get(pk=material_id)

    if material.status_id not in [material_controller.status_activo, material_controller.status_inactivo]:
        return render(request, 'pages/without_permission.html', {})

    # confirma eliminacion
    existe_error = False
    if 'delete_x' in request.POST.keys():
        if material_controller.can_delete('material_id', material_id, **material_controller.modelos_eliminar) and material_controller.delete(material_id):
            request.session['nuevo_mensaje'] = {'type': 'success', 'title': 'Materiales!', 'description': 'Se elimino el material: '+request.POST['material']}
            request.session.modified = True
            return True
        else:
            # error al modificar
            existe_error = True
            messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Materiales!', 'description': material_controller.error_operation})

    if material_controller.can_delete('material_id', material_id, **material_controller.modelos_eliminar):
        puede_eliminar = 1
    else:
        messages.add_message(request, messages.SUCCESS, {'type': 'warning', 'title': 'Materiales!', 'description': 'No puede eliminar este material, ' + material_controller.error_operation})
        puede_eliminar = 0

    # restricciones de columna
    if existe_error:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Materiales'), 'descripcion', request, material, 'material', 'codigo', 'descripcion')
    else:
        db_tags = get_html_column(apps.get_model('configuraciones', 'Materiales'), 'descripcion', None, material, 'material', 'codigo', 'descripcion')

    context = {
        'url_main': '',
        'operation_x': 'delete',
        'material': material,
        'db_tags': db_tags,
        'control_form': material_controller.control_form,
        'js_file': material_controller.modulo_session,
        'puede_eliminar': puede_eliminar,
        'error_eliminar': material_controller.error_operation,
        'status_active': material_controller.activo,
        'autenticado': 'si',

        'module_x': settings.MOD_MATERIALES,
        'module_x2': '',
        'module_x3': '',

        'operation_x': 'delete',
        'operation_x2': '',
        'operation_x3': '',

        'id': material_id,
        'id2': '',
        'id3': '',
    }
    return render(request, 'configuraciones/materiales_form.html', context)
