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
from controllers.ventas.ReservasController import ReservasController

reserva_controller = ReservasController()


# reservas
@user_passes_test(lambda user: get_user_permission_operation(user, settings.MOD_RESERVAS, 'lista'), 'without_permission')
def reservas_index(request):
    permisos = get_permissions_user(request.user, settings.MOD_RESERVAS)

    # operaciones
    if 'operation_x' in request.POST.keys():
        operation = request.POST['operation_x']
        if not operation in ['', 'add_reserva', 'confirmar', 'eliminar', 'eliminar_reserva']:
            return render(request, 'pages/without_permission.html', {})

        # add reserva
        if operation == 'add_reserva':
            error = 0
            fecha_mostrar = ''
            try:
                nombres = request.POST['nombres'].strip()
                apellidos = request.POST['apellidos'].strip()
                telefonos = request.POST['telefonos'].strip()
                aux_dia = request.POST['dia'].strip()
                dia = aux_dia if len(aux_dia) == 2 else '0' + aux_dia
                dia_semana = request.POST['dia_semana'].strip()
                hora = request.POST['hora'].strip()
                periodo = request.POST['periodo'].strip()

                reserva_dia = apps.get_model('reservas', 'ReservasDias').objects.get(pk=int(dia_semana))
                reserva_hora = apps.get_model('reservas', 'ReservasHoras').objects.get(pk=int(hora))
                # registro ya confirmado
                status_venta = apps.get_model('status', 'Status').objects.get(pk=settings.STATUS_VENTA)

                fecha_inicio = fecha_periodo(periodo, dia) + ' ' + reserva_hora.hora + ':00'
                fecha_mostrar = get_date_show(fecha=fecha_inicio, formato_ori='yyyy-mm-dd HH:ii:ss', formato='dd-MMM-yyyy HH:ii')

                reserva = apps.get_model('reservas', 'Reservas').objects.create(
                    nombres=nombres, apellidos=apellidos, telefonos=telefonos, mensaje='',
                    reserva_dia_id=reserva_dia, reserva_hora_id=reserva_hora, status_id=status_venta,
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

            return render(request, 'ventas/reservas_respuesta.html', context)

        # confirmar
        if operation == 'confirmar':
            error = 0
            try:
                reserva_id = int(request.POST['reserva_id'].strip())
                # registro ya confirmado
                status_venta = apps.get_model('status', 'Status').objects.get(pk=settings.STATUS_VENTA)
                reserva = apps.get_model('reservas', 'Reservas').objects.get(pk=reserva_id)
                reserva.status_id = status_venta
                reserva.updated_at = 'now'
                reserva.save()

            except Exception as ex:
                print('ERROR reserva: ', str(ex))
                error = 1

            context = {
                'error': error,
            }

            return render(request, 'ventas/reservas_respuesta_confirmar.html', context)

        # eliminar
        if operation == 'eliminar':
            error = 0
            try:
                reserva_id = int(request.POST['reserva_id'].strip())
                # registro ya confirmado
                status_anulado = apps.get_model('status', 'Status').objects.get(pk=settings.STATUS_ANULADO)
                reserva = apps.get_model('reservas', 'Reservas').objects.get(pk=reserva_id)
                reserva.status_id = status_anulado
                reserva.updated_at = 'now'
                reserva.save()

            except Exception as ex:
                print('ERROR reserva: ', str(ex))
                error = 1

            context = {
                'error': error,
            }

            return render(request, 'ventas/reservas_respuesta_eliminar.html', context)

        # eliminar reserva
        if operation == 'eliminar_reserva':
            error = 0
            try:
                reserva_id = int(request.POST['reserva_id'].strip())
                # registro ya confirmado
                status_anulado = apps.get_model('status', 'Status').objects.get(pk=settings.STATUS_ANULADO)
                reserva = apps.get_model('reservas', 'Reservas').objects.get(pk=reserva_id)
                reserva.status_id = status_anulado
                reserva.updated_at = 'now'
                reserva.save()

            except Exception as ex:
                print('ERROR reserva: ', str(ex))
                error = 1

            context = {
                'error': error,
            }

            return render(request, 'ventas/reservas_respuesta_eliminar.html', context)

    # verificamos mensajes
    if 'nuevo_mensaje' in request.session.keys():
        messages.add_message(request, messages.SUCCESS, request.session['nuevo_mensaje'])
        del request.session['nuevo_mensaje']
        request.session.modified = True

    # datos por defecto
    calendario = reserva_controller.index(request)
    #print('calendario: ', calendario)
    reservas_session = request.session[reserva_controller.modulo_session]

    periodo = reserva_controller.variables_filtros_values['search_periodo']
    periodo_next = next_periodo(periodo)
    periodo_ant = previous_periodo(periodo)

    # print(zonas_session)
    context = {
        'calendario': calendario,
        'session': reservas_session,
        'permisos': permisos,
        'url_main': '',
        'status_anulado': reserva_controller.anulado,
        'status_preventa': reserva_controller.preventa,
        'status_venta': reserva_controller.venta,
        'status_finalizado': reserva_controller.finalizado,
        'autenticado': 'si',

        'periodo_actual': periodo,
        'periodo_next': periodo_next,
        'periodo_ant': periodo_ant,

        'js_file': reserva_controller.modulo_session,
        'columnas': reserva_controller.columnas,
        'module_x': settings.MOD_RESERVAS,
        'module_x2': '',
        'module_x3': '',

        'operation_x': '',
        'operation_x2': '',
        'operation_x3': '',

        'id': '',
        'id2': '',
        'id3': '',
    }
    return render(request, 'ventas/reservas.html', context)
