from controllers.DefaultValues import DefaultValues
from django.apps import apps
from django.conf import settings
from datetime import datetime

from utils.dates_functions import get_date_system, get_date_show, add_days_datetime
from utils.dates_functions import get_seconds_date1_sub_date2, get_date_to_db
from utils.permissions import get_permissions_user
from utils.validators import validate_string

from django.db import transaction


class PedidosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Pedidos'
        self.modelo_id = 'pedido_id'
        self.modelo_app = 'pedidos'
        self.modulo_id = settings.MOD_PEDIDOS

        # variables de session
        self.modulo_session = "pedidos"
        self.columnas.append('created_at')
        self.columnas.append('nombres')
        self.columnas.append('apellidos')
        self.columnas.append('telefonos')

        self.variables_filtros.append('search_fecha_ini')
        self.variables_filtros.append('search_fecha_fin')
        self.variables_filtros.append('search_nombres')
        self.variables_filtros.append('search_apellidos')
        self.variables_filtros.append('search_telefonos')

        self.variables_filtros_defecto['search_apellidos'] = ''
        self.variables_filtros_defecto['search_nombres'] = ''
        self.variables_filtros_defecto['search_telefonos'] = ''

        fecha_actual = get_date_system()
        fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')
        fecha_ini = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=-7, formato='dd-MMM-yyyy')

        self.variables_filtros_defecto['search_fecha_ini'] = fecha_ini
        self.variables_filtros_defecto['search_fecha_fin'] = fecha_fin

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        self.variable_order_type_value = 'DESC'

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = ""

    def index(self, request):
        DefaultValues.index(self, request)

        # ultimo acceso
        if 'last_access' in request.session[self.modulo_session].keys():
            # restamos
            resta = abs(get_seconds_date1_sub_date2(fecha1=get_date_system(time='yes'), formato1='yyyy-mm-dd HH:ii:ss', fecha2=request.session[self.modulo_session]['last_access'], formato2='yyyy-mm-dd HH:ii:ss'))
            # print('resta:', resta)
            if resta > 14400:  # 4 horas (4x60x60)
                # print('modificando')
                fecha_actual = get_date_system()
                fecha_inicio = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=-7, formato='dd-MMM-yyyy')
                fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')

                self.variables_filtros_values['search_fecha_ini'] = fecha_inicio
                self.variables_filtros_defecto['search_fecha_ini'] = fecha_inicio
                self.variables_filtros_values['search_fecha_fin'] = fecha_fin
                self.variables_filtros_defecto['search_fecha_fin'] = fecha_fin

                # orden por defecto
                self.variable_order_value = self.columnas[0]
                self.variable_order_type_value = 'DESC'
                request.session[self.modulo_session][self.variable_order] = self.variable_order_value
                request.session[self.modulo_session][self.variable_order_type] = self.variable_order_type_value

                # session
                request.session[self.modulo_session]['search_fecha_ini'] = self.variables_filtros_defecto['search_fecha_ini']
                request.session[self.modulo_session]['search_fecha_fin'] = self.variables_filtros_defecto['search_fecha_fin']
                request.session.modified = True

            # print('variable:', self.variable_val)
            # actualizamos a la fecha actual
            request.session[self.modulo_session]['last_access'] = get_date_system(time='yes')
            request.session.modified = True
        else:
            request.session[self.modulo_session]['last_access'] = get_date_system(time='yes')
            request.session.modified = True

        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.anulado, self.activo, self.finalizado]

        # fechas
        if self.variables_filtros_values['search_fecha_ini'].strip() != '' and self.variables_filtros_values['search_fecha_fin'].strip() != '':
            self.filtros_modulo['created_at__gte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_ini'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
            self.filtros_modulo['created_at__lte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_fin'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

        # apellidos
        if self.variables_filtros_values['search_apellidos'].strip() != "":
            self.filtros_modulo['apellidos__icontains'] = self.variables_filtros_values['search_apellidos'].strip()
        # nombres
        if self.variables_filtros_values['search_nombres'].strip() != "":
            self.filtros_modulo['nombres__icontains'] = self.variables_filtros_values['search_nombres'].strip()
        # telefonos
        if self.variables_filtros_values['search_telefonos'].strip() != "":
            self.filtros_modulo['telefonos__icontains'] = self.variables_filtros_values['search_telefonos'].strip()

        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def get_list(self):
        # orden
        orden_enviar = ''
        if self.variable_order_value != '':
            orden_enviar = self.variable_order_value
            if self.variable_order_type_value != '':
                if self.variable_order_type_value == 'DESC':
                    orden_enviar = '-' + orden_enviar
        # print(orden_enviar)

        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        retorno = modelo.objects.filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]

        return retorno

    def permission_operation(self, user_perfil, operation):
        """add ingreso almacen"""
        try:
            if user_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
                return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
                return True

            return False

        except Exception as ex:
            print('Error in permission operation, ', str(ex))
            return False

    def get_pedido(self, pedido_id):
        """devuelve datos del pedido"""
        pedido_retorno = {}
        try:
            pedido = apps.get_model('pedidos', 'Pedidos').objects.get(pk=int(pedido_id))
            pedido_retorno = pedido.__dict__

            # detalles
            detalles = []
            pedido_detalles = apps.get_model('pedidos', 'PedidosDetalles').objects.select_related('producto_id').filter(pedido_id=pedido, status_id=self.status_activo).order_by('producto_id__producto')

            for detalle in pedido_detalles:
                dato = {}
                dato['producto_id'] = detalle.producto_id.producto_id
                dato['producto'] = detalle.producto_id.producto
                dato['cantidad'] = int(detalle.cantidad)
                dato['costo'] = detalle.costo
                dato['descuento'] = detalle.descuento
                dato['total'] = detalle.total

                detalles.append(dato)

            pedido_retorno['detalles'] = detalles

        except Exception as ex:
            print('Error al recuperar el pedido: ' + str(ex))
            pedido_retorno = {}

        return pedido_retorno

    def pedidos_cliente_marcar(self, request, id):
        """marcamos el pedido"""

        try:
            # estado
            status_pedido = apps.get_model('status', 'Status').objects.get(pk=int(request.POST['tipo_venta']))
            pedido = apps.get_model('pedidos', 'Pedidos').objects.get(pk=int(id))

            # datos
            datos = {}
            datos['status_id'] = status_pedido
            datos['updated_at'] = 'now'

            if self.pedidos_cliente_marcar_db(id, **datos):
                self.error_operation = ""
                return True
            else:
                self.error_operation = 'error al marcar el pedido'
                return False
        except:
            self.error_operation = "Error al actualizar el pedido"
            return False

    def pedidos_cliente_marcar_db(self, id, **datos):
        """actualizamos a la base de datos"""

        try:
            with transaction.atomic():
                campos_update = {}
                campos_update['status_id'] = datos['status_id']
                campos_update['updated_at'] = datos['updated_at']

                pedido_update = apps.get_model('pedidos', 'Pedidos').objects.filter(pk=id)
                pedido_update.update(**campos_update)

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR pedido marcar, ' + str(ex))
            return False

    def can_anular(self, id, user):
        """verificando si se puede eliminar o no la tabla"""
        # puede anular el usuario con permiso de la sucursal
        usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=user)
        punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=usuario_perfil.punto_id)
        permisos = get_permissions_user(user, settings.MOD_PEDIDOS)

        # pedido
        pedido = apps.get_model('pedidos', 'Pedidos').objects.get(pk=id)
        if pedido.status_id.status_id == self.anulado:
            self.error_operation = 'el registro ya esta anulado'
            return False

        if permisos.anular:
            return True

        return False

    def anular(self, request, id):
        """anulando el registro"""
        try:
            if self.can_anular(id, request.user):

                status_anular = self.status_anulado
                motivo_a = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')

                campos_update = {}
                user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)

                campos_update['user_perfil_id'] = user_perfil
                campos_update['user_perfil_id_anula'] = user_perfil.user_perfil_id
                campos_update['motivo_anula'] = motivo_a
                campos_update['status_id'] = status_anular
                campos_update['deleted_at'] = 'now'

                if self.anular_db(id, **campos_update):
                    self.error_operation = ''
                    return True
                else:
                    return False

            else:
                self.error_operation = 'No tiene permiso para anular este pedido'
                return False

        except Exception as ex:
            print('Error anular pedido: ' + str(ex))
            self.error_operation = 'Error al anular el pedido, ' + str(ex)
            return False

    def anular_db(self, id, **datos):
        """ anulamos en la bd """
        try:
            with transaction.atomic():
                campos_update = {}
                campos_update['user_id_anula'] = datos['user_perfil_id_anula']
                campos_update['motivo_anula'] = datos['motivo_anula']
                campos_update['status_id'] = datos['status_id']
                campos_update['deleted_at'] = datos['deleted_at']

                # registramos
                pedido_update = apps.get_model('pedidos', 'Pedidos').objects.filter(pk=id)
                pedido_update.update(**campos_update)

                self.error_operation = ''
                return True

        except Exception as ex:
            print('Error anular pedido db: ' + str(ex))
            self.error_operation = 'Error de argumentos, ' + str(ex)
            return False
