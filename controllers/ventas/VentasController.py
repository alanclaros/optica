from decimal import Decimal
# from re import match
# from typing import Match

from clientes.models import Clientes
from configuraciones.models import Almacenes, Puntos
from controllers.cajas.CajasEgresosController import CajasEgresosController
from controllers.cajas.CajasIngresosController import CajasIngresosController
from controllers.clientes.ClientesController import ClientesController
from controllers.DefaultValues import DefaultValues
from controllers.inventarios.StockController import StockController
from controllers.cajas.CajasController import CajasController
from django.apps import apps
from django.conf import settings
from django.db import connection, transaction
from controllers.ventas.PlanPagosCreate import PlanPagosCreate
from inventarios.models import Stock
from permisos.models import UsersPerfiles
from productos.models import Productos
# fechas
from utils.dates_functions import (add_days_datetime, add_minutes_datetime,
                                   get_date_show, get_date_system,
                                   get_date_to_db, get_fecha_int,
                                   get_seconds_date1_sub_date2)
from utils.permissions import get_almacen_user, get_permissions_user, get_system_settings, current_date
from utils.validators import (validate_number_decimal, validate_number_int,
                              validate_string)

from ventas.models import (Ventas, VentasImagenes, VentasDetalles)
from controllers.SystemController import SystemController
import os
import shutil


class VentasController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Ventas'
        self.modelo_id = 'venta_id'
        self.modelo_app = 'ventas'
        self.modulo_id = settings.MOD_VENTAS

        # variables de session
        self.modulo_session = "ventas"
        self.columnas.append('fecha_preventa')
        self.columnas.append('nombres')
        self.columnas.append('apellidos')

        self.variables_filtros.append('search_fecha_ini')
        self.variables_filtros.append('search_fecha_fin')
        self.variables_filtros.append('search_numero_venta')
        self.variables_filtros.append('search_apellidos')
        self.variables_filtros.append('search_nombres')
        self.variables_filtros.append('search_telefonos')

        fecha_actual = get_date_system()
        fecha_fin = get_date_show(fecha=fecha_actual, formato='dd-MMM-yyyy', formato_ori='yyyy-mm-dd')
        fecha_ini = add_days_datetime(fecha=fecha_actual, formato_ori='yyyy-mm-dd', dias=-7, formato='dd-MMM-yyyy')

        self.variables_filtros_defecto['search_fecha_ini'] = fecha_ini
        self.variables_filtros_defecto['search_fecha_fin'] = fecha_fin
        self.variables_filtros_defecto['search_numero_venta'] = ''
        self.variables_filtros_defecto['search_apellidos'] = ''
        self.variables_filtros_defecto['search_nombres'] = ''
        self.variables_filtros_defecto['search_telefonos'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"
        self.variable_order_type_value = 'DESC'

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {}

        # control del formulario
        self.control_form = "txt|2|S|apellidos|Apellidos;"
        self.control_form += "txt|2|S|nombres|Nombres;"
        self.control_form += "txt|5|S|telefonos|Telefonos;"
        self.control_form += "txt|1|S|numero_venta|Numero Venta;"
        self.control_form += "txt|1|S|total_venta|Total"

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
        self.filtros_modulo['status_id_id__in'] = [self.anulado, self.preventa, self.venta, self.finalizado]

        # numero_venta
        if self.variables_filtros_values['search_numero_venta'].strip() != "":
            self.filtros_modulo['numero_venta'] = self.variables_filtros_values['search_numero_venta'].strip()
        else:
            # fechas
            if self.variables_filtros_values['search_fecha_ini'].strip() != '' and self.variables_filtros_values['search_fecha_fin'].strip() != '':
                self.filtros_modulo['fecha_preventa__gte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_ini'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='00:00:00')
                self.filtros_modulo['fecha_preventa__lte'] = get_date_to_db(fecha=self.variables_filtros_values['search_fecha_fin'].strip(), formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss', tiempo='23:59:59')

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
        retorno = modelo.objects.select_related('almacen_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]

        return retorno

    def permission_operation(self, user_perfil, operation):
        """add ingreso almacen"""
        try:
            if user_perfil.perfil_id.perfil_id == settings.PERFIL_ADMIN:
                return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_SUPERVISOR:
                return True

            if user_perfil.perfil_id.perfil_id == settings.PERFIL_CAJERO:
                if operation == self.preventa or operation == self.venta or operation == self.finalizado:
                    return True

            return False

        except Exception as ex:
            print('Error in permission operation, ', str(ex))
            return False

    def save(self, request, type='add'):
        """aniadimos un nuevo registro"""
        try:
            # punto
            usuario = request.user
            usuario_perfil = UsersPerfiles.objects.get(user_id=usuario)
            punto = Puntos.objects.get(pk=usuario_perfil.punto_id)
            cant_almacenes = apps.get_model('configuraciones', 'PuntosAlmacenes').objects.filter(punto_id=punto).count()
            if cant_almacenes != 1:
                self.error_operation = 'Solo debe tener asignado 1 almacen'
                return False
            punto_almacen = apps.get_model('configuraciones', 'PuntosAlmacenes').objects.get(punto_id=punto)
            almacen = punto_almacen.almacen_id

            operation = validate_string('operation', request.POST['operation'])

            if not self.permission_operation(usuario_perfil, int(operation)):
                self.error_operation = 'no tiene permiso para esta operacion'
                return False

            if int(operation) == self.preventa:
                cliente_id = validate_number_int('cliente_id', request.POST['cliente_id'], len_zero='yes')
                id = validate_number_int('id', request.POST['id'], len_zero='yes')

                laboratorio_id = validate_number_int('laboratorio', request.POST['laboratorio_id'])
                tecnico_id = validate_number_int('tecnico', request.POST['tecnico_id'])
                oftalmologo_id = validate_number_int('oftalmologo', request.POST['oftalmologo_id'])

                tipo_montura_id = validate_number_int('tipo montura', request.POST['tipo_montura'], len_zero='yes')
                tipo_montura_precio = validate_number_decimal('tipo montura precio', request.POST['tipo_montura_precio'], len_zero='yes')
                stock_id = validate_number_int('stock', request.POST['stock_1'], len_zero='yes')
                materiales_select = request.POST.getlist('materiales_select')
                material_precio = validate_number_decimal('material precio', request.POST['material_precio'], len_zero='yes')

                configuraciones = apps.get_model('configuraciones', 'Configuraciones').objects.get(pk=1)
                numero_actual_venta = configuraciones.numero_actual_venta

                apellidos = validate_string('apellidos', request.POST['apellidos'], remove_specials='yes')
                nombres = validate_string('nombres', request.POST['nombres'], remove_specials='yes')
                ci_nit = validate_string('ci/nit', request.POST['ci_nit'], remove_specials='yes', len_zero='yes')
                telefonos = validate_string('telefonos', request.POST['telefonos'], remove_specials='yes')
                email = ''
                cupon_id = 0
                cupon = ''
                tipo_venta = 'CONTADO'
                plan_pago = 0
                caja_id = 0

                direccion = validate_string('direccion', request.POST['direccion'], remove_specials='yes', len_zero='yes')
                factura_a = validate_string('factura a', request.POST['factura_a'], remove_specials='yes', len_zero='yes')
                nota = validate_string('nota', request.POST['nota'], remove_specials='yes', len_zero='yes')

                subtotal = validate_number_decimal('subtotal', request.POST['total_pedido'])
                descuento = validate_number_decimal('descuento', request.POST['descuento'], len_zero='yes')
                porcentaje_descuento = validate_number_decimal('porcentaje descuento', request.POST['porcentaje_descuento'], len_zero='yes')
                total = validate_number_decimal('total', request.POST['total_venta'])
                a_cuenta = validate_number_decimal('a_cuenta', request.POST['a_cuenta'], len_zero='yes')
                saldo = validate_number_decimal('saldo', request.POST['saldo'], len_zero='yes')

                # datos lentes
                lejos_od_esf = validate_number_decimal('lejos od esf', request.POST['lejos_od_esf'], len_zero='yes')
                lejos_od_cli = validate_number_decimal('lejos od cli', request.POST['lejos_od_cli'], len_zero='yes')
                lejos_od_eje = validate_number_decimal('lejos od eje', request.POST['lejos_od_eje'], len_zero='yes')
                lejos_oi_esf = validate_number_decimal('lejos oi esf', request.POST['lejos_oi_esf'], len_zero='yes')
                lejos_oi_cli = validate_number_decimal('lejos oi cli', request.POST['lejos_oi_cli'], len_zero='yes')
                lejos_oi_eje = validate_number_decimal('lejos oi eje', request.POST['lejos_oi_eje'], len_zero='yes')
                lejos_di = validate_number_decimal('lejos di', request.POST['lejos_di'], len_zero='yes')

                cerca_od_esf = validate_number_decimal('cerca od esf', request.POST['cerca_od_esf'], len_zero='yes')
                cerca_od_cli = validate_number_decimal('cerca od cli', request.POST['cerca_od_cli'], len_zero='yes')
                cerca_od_eje = validate_number_decimal('cerca od eje', request.POST['cerca_od_eje'], len_zero='yes')
                cerca_oi_esf = validate_number_decimal('cerca oi esf', request.POST['cerca_oi_esf'], len_zero='yes')
                cerca_oi_cli = validate_number_decimal('cerca oi cli', request.POST['cerca_oi_cli'], len_zero='yes')
                cerca_oi_eje = validate_number_decimal('cerca oi eje', request.POST['cerca_oi_eje'], len_zero='yes')
                cerca_di = validate_number_decimal('cerca di', request.POST['cerca_di'], len_zero='yes')

                aux = validate_string('fecha', request.POST['fecha_preventa'], remove_specials='yes')
                fecha_preventa = get_date_to_db(fecha=aux, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss')

                datos = {}
                datos['type'] = type
                datos['id'] = id
                datos['almacen_id'] = almacen
                datos['punto_id'] = punto
                datos['lista_imagenes'] = request.session['session_imagenes']
                datos['user_perfil_id'] = usuario_perfil
                datos['laboratorio_id'] = laboratorio_id
                datos['tecnico_id'] = tecnico_id
                datos['oftalmologo_id'] = oftalmologo_id
                datos['tipo_montura_id'] = tipo_montura_id
                datos['tipo_montura_precio'] = tipo_montura_precio
                datos['stock_id'] = stock_id
                datos['materiales_select'] = materiales_select
                datos['material_precio'] = material_precio

                datos['status_id'] = self.status_preventa
                datos['operation'] = operation

                datos['fecha_preventa'] = fecha_preventa
                datos['cliente_id'] = cliente_id
                datos['apellidos'] = apellidos
                datos['nombres'] = nombres
                datos['ci_nit'] = ci_nit
                datos['telefonos'] = telefonos
                datos['direccion'] = direccion
                datos['factura_a'] = factura_a

                datos['email'] = email
                datos['cupon_id'] = cupon_id
                datos['cupon'] = cupon
                datos['tipo_venta'] = tipo_venta
                datos['plan_pago'] = plan_pago
                datos['caja_id'] = caja_id

                datos['numero_venta'] = numero_actual_venta + 1
                datos['nota'] = nota

                datos['lejos_od_esf'] = lejos_od_esf
                datos['lejos_od_cli'] = lejos_od_cli
                datos['lejos_od_eje'] = lejos_od_eje
                datos['lejos_oi_esf'] = lejos_oi_esf
                datos['lejos_oi_cli'] = lejos_oi_cli
                datos['lejos_oi_eje'] = lejos_oi_eje
                datos['lejos_di'] = lejos_di

                datos['cerca_od_esf'] = cerca_od_esf
                datos['cerca_od_cli'] = cerca_od_cli
                datos['cerca_od_eje'] = cerca_od_eje
                datos['cerca_oi_esf'] = cerca_oi_esf
                datos['cerca_oi_cli'] = cerca_oi_cli
                datos['cerca_oi_eje'] = cerca_oi_eje
                datos['cerca_di'] = cerca_di

                datos['subtotal'] = subtotal
                datos['descuento'] = descuento
                datos['porcentaje_descuento'] = porcentaje_descuento
                datos['total'] = total
                datos['a_cuenta'] = a_cuenta
                datos['saldo'] = saldo

                datos['created_at'] = 'now'
                datos['updated_at'] = 'now'

                if self.save_preventa(**datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            if int(operation) == self.venta:
                id = validate_number_int('id', request.POST['id'], len_zero='yes')
                laboratorio_id = validate_number_int('laboratorio', request.POST['laboratorio_id'])
                tecnico_id = validate_number_int('tecnico', request.POST['tecnico_id'])
                oftalmologo_id = validate_number_int('oftalmologo', request.POST['oftalmologo_id'])

                tipo_montura_id = validate_number_int('tipo montura', request.POST['tipo_montura'])
                tipo_montura_precio = validate_number_decimal('tipo montura precio', request.POST['tipo_montura_precio'], len_zero='yes')
                stock_id = validate_number_int('stock', request.POST['stock_1'])
                materiales_select = request.POST.getlist('materiales_select')
                material_precio = validate_number_decimal('material precio', request.POST['material_precio'], len_zero='yes')

                nota = validate_string('nota', request.POST['nota'], remove_specials='yes', len_zero='yes')

                subtotal = validate_number_decimal('subtotal', request.POST['total_pedido'])
                descuento = validate_number_decimal('descuento', request.POST['descuento'], len_zero='yes')
                porcentaje_descuento = validate_number_decimal('porcentaje descuento', request.POST['porcentaje_descuento'], len_zero='yes')
                total = validate_number_decimal('total', request.POST['total_venta'])
                a_cuenta = validate_number_decimal('a_cuenta', request.POST['a_cuenta'], len_zero='yes')
                saldo = validate_number_decimal('saldo', request.POST['saldo'], len_zero='yes')

                # datos lentes
                lejos_od_esf = validate_number_decimal('lejos od esf', request.POST['lejos_od_esf'], len_zero='yes')
                lejos_od_cli = validate_number_decimal('lejos od cli', request.POST['lejos_od_cli'], len_zero='yes')
                lejos_od_eje = validate_number_decimal('lejos od eje', request.POST['lejos_od_eje'], len_zero='yes')
                lejos_oi_esf = validate_number_decimal('lejos oi esf', request.POST['lejos_oi_esf'], len_zero='yes')
                lejos_oi_cli = validate_number_decimal('lejos oi cli', request.POST['lejos_oi_cli'], len_zero='yes')
                lejos_oi_eje = validate_number_decimal('lejos oi eje', request.POST['lejos_oi_eje'], len_zero='yes')
                lejos_di = validate_number_decimal('lejos di', request.POST['lejos_di'], len_zero='yes')

                cerca_od_esf = validate_number_decimal('cerca od esf', request.POST['cerca_od_esf'], len_zero='yes')
                cerca_od_cli = validate_number_decimal('cerca od cli', request.POST['cerca_od_cli'], len_zero='yes')
                cerca_od_eje = validate_number_decimal('cerca od eje', request.POST['cerca_od_eje'], len_zero='yes')
                cerca_oi_esf = validate_number_decimal('cerca oi esf', request.POST['cerca_oi_esf'], len_zero='yes')
                cerca_oi_cli = validate_number_decimal('cerca oi cli', request.POST['cerca_oi_cli'], len_zero='yes')
                cerca_oi_eje = validate_number_decimal('cerca oi eje', request.POST['cerca_oi_eje'], len_zero='yes')
                cerca_di = validate_number_decimal('cerca di', request.POST['cerca_di'], len_zero='yes')

                tipo_venta = validate_string('tipo venta', request.POST['tipo_venta'], remove_specials='yes')
                aux = validate_string('fecha plan pagos', request.POST['fecha_planpagos'], remove_specials='yes')
                fecha_planpagos = get_date_to_db(fecha=aux, formato_ori='dd-MMM-yyyy', formato='yyyy-mm-dd HH:ii:ss')
                cuotas_planpagos = validate_number_int('cuotas', request.POST['cuotas_planpagos'], len_zero='yes')
                dias_planpagos = validate_number_int('dias', request.POST['dias_planpagos'], len_zero='yes')

                plan_pago = 0
                caja_controller = CajasController()
                caja_lista = caja_controller.cash_active(current_date(), request.user, formato_ori='yyyy-mm-dd')

                if not caja_lista:
                    self.error_operation = 'Debe tener una caja activa'
                    return False
                caja_usuario = caja_lista[0]

                datos = {}
                datos['operation'] = operation
                datos['id'] = id
                datos['user_perfil_id'] = usuario_perfil
                datos['updated_at'] = 'now'
                datos['lista_imagenes'] = request.session['session_imagenes']

                datos['laboratorio_id'] = laboratorio_id
                datos['tecnico_id'] = tecnico_id
                datos['oftalmologo_id'] = oftalmologo_id
                datos['tipo_montura_id'] = tipo_montura_id
                datos['tipo_montura_precio'] = tipo_montura_precio
                datos['stock_id'] = stock_id
                datos['materiales_select'] = materiales_select
                datos['material_precio'] = material_precio

                datos['status_id'] = self.status_venta
                datos['operation'] = operation

                datos['tipo_venta'] = tipo_venta
                datos['plan_pago'] = plan_pago
                datos['fecha_planpagos'] = fecha_planpagos
                datos['cuotas_planpagos'] = cuotas_planpagos
                datos['dias_planpagos'] = dias_planpagos
                datos['caja_id'] = caja_usuario

                datos['nota'] = nota

                datos['lejos_od_esf'] = lejos_od_esf
                datos['lejos_od_cli'] = lejos_od_cli
                datos['lejos_od_eje'] = lejos_od_eje
                datos['lejos_oi_esf'] = lejos_oi_esf
                datos['lejos_oi_cli'] = lejos_oi_cli
                datos['lejos_oi_eje'] = lejos_oi_eje
                datos['lejos_di'] = lejos_di

                datos['cerca_od_esf'] = cerca_od_esf
                datos['cerca_od_cli'] = cerca_od_cli
                datos['cerca_od_eje'] = cerca_od_eje
                datos['cerca_oi_esf'] = cerca_oi_esf
                datos['cerca_oi_cli'] = cerca_oi_cli
                datos['cerca_oi_eje'] = cerca_oi_eje
                datos['cerca_di'] = cerca_di

                datos['subtotal'] = subtotal
                datos['descuento'] = descuento
                datos['porcentaje_descuento'] = porcentaje_descuento
                datos['total'] = total
                datos['a_cuenta'] = a_cuenta
                datos['saldo'] = saldo

                if self.save_venta(**datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            if int(operation) == self.finalizado:
                id = validate_number_int('id', request.POST['id'], len_zero='yes')
                notificar = validate_string('notificar', request.POST['notificar'], remove_specials='yes')

                # caja para la operation
                caja_controller = CajasController()
                caja_lista = caja_controller.cash_active(current_date(), request.user, formato_ori='yyyy-mm-dd')

                if not caja_lista:
                    self.error_operation = 'Debe tener una caja activa'
                    return False
                caja_usuario = caja_lista[0]

                datos = {}
                datos['operation'] = operation
                datos['id'] = id
                datos['lista_imagenes'] = request.session['session_imagenes']
                datos['notificar'] = notificar
                datos['caja_id'] = caja_usuario
                datos['user_perfil_id'] = usuario_perfil
                datos['updated_at'] = 'now'

                # print('datos para finalizar...: ', datos)
                if self.save_finalizado(**datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            self.error_operation = 'operation no valid'
            return False

        except Exception as ex:
            self.error_operation = "Error al agregar el registro, " + str(ex)
            return False

    def save_preventa(self, **datos):
        """aniadimos a la base de datos"""
        try:
            if not self.permission_operation(datos['user_perfil_id'], datos['operation']):
                self.error_operation = 'no puede realizar esta operacion'
                return False

            #stock_controller = StockController()
            cliente_controller = ClientesController()
            # print('antes transaccion')
            with transaction.atomic():
                campos_add = {}
                campos_add['almacen_id'] = datos['almacen_id']
                campos_add['punto_id'] = datos['punto_id']
                campos_add['caja_id'] = datos['caja_id']
                campos_add['user_perfil_id_preventa'] = datos['user_perfil_id']
                campos_add['status_id'] = datos['status_id']

                if datos['cliente_id'] == 0:
                    # registramos nuevo cliente
                    datos_cliente = {}
                    if datos['ci_nit'] == '':
                        # registramos nuevo cliente directamente
                        datos_cliente['apellidos'] = datos['apellidos']
                        datos_cliente['nombres'] = datos['nombres']
                        datos_cliente['ci_nit'] = datos['ci_nit']
                        datos_cliente['telefonos'] = datos['telefonos']
                        datos_cliente['direccion'] = datos['direccion']
                        datos_cliente['email'] = datos['email']
                        datos_cliente['razon_social'] = datos['factura_a']
                        datos_cliente['factura_a'] = datos['factura_a']
                        datos_cliente['created_at'] = datos['created_at']
                        datos_cliente['updated_at'] = datos['updated_at']
                        datos_cliente['status_id'] = self.status_activo
                        datos_cliente['user_perfil_id'] = datos['user_perfil_id']
                        datos_cliente['punto_id'] = datos['punto_id']
                        datos_cliente['id'] = 0

                        if not cliente_controller.save_db(type='add', **datos_cliente):
                            transaction.set_rollback(True)
                            self.error_operation = 'Error al crear el nuevo cliente'
                            return False

                        # recuperamos el ultimo id
                        cliente_aux = apps.get_model('clientes', 'Clientes').objects.latest('cliente_id')
                        datos['cliente_id'] = cliente_aux

                    else:
                        # buscamos y creamos o actualizamos
                        cliente_aux = apps.get_model('clientes', 'Clientes').objects.filter(ci_nit=datos['ci_nit'])
                        if cliente_aux:
                            primer_cliente = cliente_aux.first()
                            if primer_cliente.ci_nit == 0:
                                # no actualizamos el cliente por defecto 0
                                datos['cliente_id'] = primer_cliente
                            else:
                                # actualizamos datos
                                datos_cliente['apellidos'] = datos['apellidos']
                                datos_cliente['nombres'] = datos['nombres']
                                datos_cliente['ci_nit'] = datos['ci_nit']
                                datos_cliente['telefonos'] = datos['telefonos']
                                datos_cliente['direccion'] = datos['direccion']
                                datos_cliente['factura_a'] = datos['factura_a']
                                datos_cliente['razon_social'] = primer_cliente.razon_social
                                datos_cliente['email'] = primer_cliente.email
                                datos_cliente['updated_at'] = datos['updated_at']
                                datos_cliente['status_id'] = self.status_activo
                                datos_cliente['id'] = primer_cliente.cliente_id

                                if not cliente_controller.save_db(type='modify', **datos_cliente):
                                    transaction.set_rollback(True)
                                    self.error_operation = 'Error al actualizar datos del cliente'
                                    return False
                                cliente_aux = apps.get_model('clientes', 'Clientes').objects.get(ci_nit=datos['ci_nit'])
                                datos['cliente_id'] = cliente_aux
                        else:
                            # creamos un nuevo cliente
                            datos_cliente['apellidos'] = datos['apellidos']
                            datos_cliente['nombres'] = datos['nombres']
                            datos_cliente['ci_nit'] = datos['ci_nit']
                            datos_cliente['telefonos'] = datos['telefonos']
                            datos_cliente['direccion'] = datos['direccion']
                            datos_cliente['email'] = datos['email']
                            datos_cliente['razon_social'] = datos['factura_a']
                            datos_cliente['factura_a'] = datos['factura_a']
                            datos_cliente['created_at'] = datos['created_at']
                            datos_cliente['updated_at'] = datos['updated_at']
                            datos_cliente['status_id'] = self.status_activo
                            datos_cliente['user_perfil_id'] = datos['user_perfil_id']
                            datos_cliente['punto_id'] = datos['punto_id']
                            datos_cliente['id'] = 0

                            if not cliente_controller.save_db(type='add', **datos_cliente):
                                transaction.set_rollback(True)
                                self.error_operation = 'Error al crear el nuevo cliente'
                                return False

                            cliente_aux = apps.get_model('clientes', 'Clientes').objects.get(ci_nit=datos['ci_nit'])
                            datos['cliente_id'] = cliente_aux
                else:
                    # actualizamos datos
                    cliente_actual = apps.get_model('clientes', 'Clientes').objects.get(pk=datos['cliente_id'])
                    datos_cliente = {}
                    datos_cliente['apellidos'] = datos['apellidos']
                    datos_cliente['nombres'] = datos['nombres']
                    datos_cliente['ci_nit'] = datos['ci_nit']
                    datos_cliente['telefonos'] = datos['telefonos']
                    datos_cliente['direccion'] = datos['direccion']
                    datos_cliente['factura_a'] = datos['factura_a']
                    datos_cliente['razon_social'] = cliente_actual.razon_social
                    datos_cliente['email'] = cliente_actual.email
                    datos_cliente['updated_at'] = datos['updated_at']
                    datos_cliente['status_id'] = self.status_activo
                    datos_cliente['id'] = cliente_actual.cliente_id

                    if not cliente_controller.save_db(type='modify', **datos_cliente):
                        self.error_operation = 'Error al actualizar datos del cliente'
                        return False

                    datos['cliente_id'] = cliente_actual

                campos_add['cliente_id'] = datos['cliente_id']
                campos_add['apellidos'] = datos['apellidos']
                campos_add['nombres'] = datos['nombres']
                campos_add['ci_nit'] = datos['ci_nit']
                campos_add['telefonos'] = datos['telefonos']
                campos_add['direccion'] = datos['direccion']
                campos_add['factura_a'] = datos['factura_a']

                campos_add['laboratorio_id'] = datos['laboratorio_id']
                campos_add['tecnico_id'] = datos['tecnico_id']
                campos_add['oftalmologo_id'] = datos['oftalmologo_id']
                campos_add['stock_id'] = datos['stock_id']

                campos_add['cupon_id'] = datos['cupon_id']
                campos_add['cupon'] = datos['cupon']
                campos_add['tipo_venta'] = datos['tipo_venta']
                campos_add['plan_pago'] = datos['plan_pago']

                campos_add['numero_venta'] = datos['numero_venta']
                campos_add['nota'] = datos['nota']

                campos_add['precio_montura'] = datos['tipo_montura_precio']
                campos_add['precio_material'] = datos['material_precio']

                campos_add['subtotal'] = datos['subtotal']
                campos_add['descuento'] = datos['descuento']
                campos_add['porcentaje_descuento'] = datos['porcentaje_descuento']
                campos_add['total'] = datos['total']
                campos_add['a_cuenta'] = datos['a_cuenta']
                campos_add['saldo'] = datos['saldo']
                #campos_add['user_perfil_id_preventa'] = datos['user_perfil_id']

                campos_add['lejos_od_esf'] = datos['lejos_od_esf']
                campos_add['lejos_od_cli'] = datos['lejos_od_cli']
                campos_add['lejos_od_eje'] = datos['lejos_od_eje']
                campos_add['lejos_oi_esf'] = datos['lejos_oi_esf']
                campos_add['lejos_oi_cli'] = datos['lejos_oi_cli']
                campos_add['lejos_oi_eje'] = datos['lejos_oi_eje']
                campos_add['lejos_di'] = datos['lejos_di']

                campos_add['cerca_od_esf'] = datos['cerca_od_esf']
                campos_add['cerca_od_cli'] = datos['cerca_od_cli']
                campos_add['cerca_od_eje'] = datos['cerca_od_eje']
                campos_add['cerca_oi_esf'] = datos['cerca_oi_esf']
                campos_add['cerca_oi_cli'] = datos['cerca_oi_cli']
                campos_add['cerca_oi_eje'] = datos['cerca_oi_eje']
                campos_add['cerca_di'] = datos['cerca_di']

                campos_add['updated_at'] = datos['updated_at']
                # print('campos add: ', campos_add)
                # venta
                if datos['type'] == 'add':
                    campos_add['fecha_preventa'] = datos['fecha_preventa']
                    campos_add['created_at'] = datos['created_at']
                    venta_add = Ventas.objects.create(**campos_add)
                    venta_add.save()

                    # numero de venta
                    configuraciones = apps.get_model('configuraciones', 'Configuraciones').objects.get(pk=1)
                    configuraciones.numero_actual_venta = configuraciones.numero_actual_venta + 1
                    configuraciones.save()

                if datos['type'] == 'modify':
                    # eliminamos detalles
                    venta_actual = Ventas.objects.get(pk=datos['id'])
                    ventas_detalles_del = VentasDetalles.objects.filter(venta_id=venta_actual)
                    ventas_detalles_del.delete()

                    venta_actual = Ventas.objects.filter(pk=datos['id'])
                    venta_actual.update(**campos_add)
                    venta_add = Ventas.objects.get(pk=datos['id'])

                # imagenes
                lista_imagenes = datos['lista_imagenes']
                lista_eliminar = []
                if datos['type'] == 'modify':
                    # recuperamos las imagenes para eliminar
                    imagenes_db = apps.get_model('ventas', 'VentasImagenes').objects.filter(venta_id=venta_add)
                    for imagen_db in imagenes_db:
                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen_db.imagen)
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen_db.imagen_thumb)
                        dato_eliminar = {}
                        dato_eliminar['imagen'] = full_filename
                        dato_eliminar['imagen_thumb'] = full_filename_thumb
                        dato_eliminar['venta_imagen_id'] = imagen_db.venta_imagen_id
                        lista_eliminar.append(dato_eliminar)

                for imagen in lista_imagenes:
                    # copiamos a venta y borramos de tmp
                    uploaded_filename = imagen['imagen']
                    system_controller = SystemController()
                    aux = system_controller.nombre_imagen('ventas', uploaded_filename)
                    full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', aux['nombre_archivo'])
                    full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', aux['nombre_archivo_thumb'])

                    full_filename_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', imagen['imagen'])
                    full_filename_thumb_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', imagen['imagen_thumb'])

                    shutil.move(full_filename_ori, full_filename)
                    shutil.move(full_filename_thumb_ori, full_filename_thumb)

                    # creamos el registro
                    imagen_add = apps.get_model('ventas', 'VentasImagenes').objects.create(
                        imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'], status_id=self.status_activo,
                        created_at='now', updated_at='now', venta_id=venta_add
                    )
                    imagen_add.save()

                # eliminamos las anteriores imagenes
                for imagen_eliminar in lista_eliminar:
                    venta_imagen_db = apps.get_model('ventas', 'VentasImagenes').objects.get(pk=imagen_eliminar['venta_imagen_id'])
                    venta_imagen_db.delete()
                    os.remove(imagen_eliminar['imagen'])
                    os.remove(imagen_eliminar['imagen_thumb'])

                # detalles
                if datos['tipo_montura_id'] != 0:
                    detalle_add = VentasDetalles.objects.create(
                        venta_id=venta_add, punto_id=datos['punto_id'], tipo_montura_id=datos['tipo_montura_id'],
                        cantidad=1, costo=datos['tipo_montura_precio'], porcentaje_descuento=0, descuento=0, total=datos['tipo_montura_precio']
                    )
                    detalle_add.save()

                for material_id in datos['materiales_select']:
                    material = apps.get_model('configuraciones', 'Materiales').objects.get(pk=material_id)

                    detalle_add = VentasDetalles.objects.create(
                        venta_id=venta_add, punto_id=datos['punto_id'], material_id=material_id,
                        cantidad=1, costo=material.costo, porcentaje_descuento=0, descuento=0, total=material.costo
                    )
                    detalle_add.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add preventa, '+str(ex))
            return False

    def save_venta(self, **datos):
        """aniadimos a la base de datos"""
        try:
            if not self.permission_operation(datos['user_perfil_id'], datos['operation']):
                self.error_operation = 'no tiene permisos para realizar esta operacion'
                return False

            venta = Ventas.objects.get(pk=datos['id'])
            if venta.status_id != self.status_preventa:
                self.error_operation = 'esta operacion no es una preventa'
                return False

            laboratorio = apps.get_model('configuraciones', 'Laboratorios').objects.get(pk=datos['laboratorio_id'])
            tecnico = apps.get_model('configuraciones', 'Tecnicos').objects.get(pk=datos['tecnico_id'])
            oftalmologo = apps.get_model('configuraciones', 'Oftalmologos').objects.get(pk=datos['oftalmologo_id'])

            tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=datos['tipo_montura_id'])
            stock = apps.get_model('inventarios', 'Stock').objects.get(pk=datos['stock_id'])

            if datos['tipo_venta'] == 'planpagos':
                if datos['a_cuenta'] > 0:
                    self.error_operation = 'En ventas con Plan de Pagos, no debe existir monto a cuenta'
                    return False

                if datos['cuotas_planpagos'] <= 0:
                    self.error_operation = 'Debe llenar la cantidad de cuotas'
                    return False

                if datos['dias_planpagos'] <= 0:
                    self.error_operation = 'Debe llenar los dias de las cuotas'
                    return False

            with transaction.atomic():
                campos_add = {}
                campos_add['user_perfil_id_venta'] = datos['user_perfil_id'].user_perfil_id
                campos_add['caja_id'] = datos['caja_id'].caja_id
                campos_add['fecha_venta'] = datos['updated_at']
                campos_add['updated_at'] = datos['updated_at']
                campos_add['status_id'] = self.status_venta

                campos_add['laboratorio_id'] = laboratorio.laboratorio_id
                campos_add['tecnico_id'] = tecnico.tecnico_id
                campos_add['oftalmologo_id'] = oftalmologo.oftalmologo_id

                campos_add['stock_id'] = datos['stock_id']

                campos_add['tipo_venta'] = datos['tipo_venta']
                campos_add['plan_pago'] = 1 if datos['tipo_venta'] == 'planpagos' else 0

                campos_add['nota'] = datos['nota']
                campos_add['precio_montura'] = datos['tipo_montura_precio']
                campos_add['precio_material'] = datos['material_precio']

                campos_add['subtotal'] = datos['subtotal']
                campos_add['descuento'] = datos['descuento']
                campos_add['porcentaje_descuento'] = datos['porcentaje_descuento']
                campos_add['total'] = datos['total']
                campos_add['a_cuenta'] = datos['a_cuenta']
                campos_add['saldo'] = datos['saldo']

                campos_add['lejos_od_esf'] = datos['lejos_od_esf']
                campos_add['lejos_od_cli'] = datos['lejos_od_cli']
                campos_add['lejos_od_eje'] = datos['lejos_od_eje']
                campos_add['lejos_oi_esf'] = datos['lejos_oi_esf']
                campos_add['lejos_oi_cli'] = datos['lejos_oi_cli']
                campos_add['lejos_oi_eje'] = datos['lejos_oi_eje']
                campos_add['lejos_di'] = datos['lejos_di']

                campos_add['cerca_od_esf'] = datos['cerca_od_esf']
                campos_add['cerca_od_cli'] = datos['cerca_od_cli']
                campos_add['cerca_od_eje'] = datos['cerca_od_eje']
                campos_add['cerca_oi_esf'] = datos['cerca_oi_esf']
                campos_add['cerca_oi_cli'] = datos['cerca_oi_cli']
                campos_add['cerca_oi_eje'] = datos['cerca_oi_eje']
                campos_add['cerca_di'] = datos['cerca_di']

                venta_actual = Ventas.objects.filter(pk=datos['id'])
                venta_actual.update(**campos_add)

                # eliminamos detalles
                venta_actual = Ventas.objects.get(pk=datos['id'])
                ventas_detalles_del = VentasDetalles.objects.filter(venta_id=venta_actual)
                ventas_detalles_del.delete()

                # detalles
                if datos['tipo_montura_id'] != 0:
                    detalle_add = VentasDetalles.objects.create(
                        venta_id=venta_actual, punto_id=venta_actual.punto_id, tipo_montura_id=tipo_montura.tipo_montura_id,
                        cantidad=1, costo=datos['tipo_montura_precio'], porcentaje_descuento=0, descuento=0, total=datos['tipo_montura_precio']
                    )

                for material_id in datos['materiales_select']:
                    material = apps.get_model('configuraciones', 'Materiales').objects.get(pk=material_id)

                    detalle_add = VentasDetalles.objects.create(
                        venta_id=venta_actual, punto_id=venta_actual.punto_id, material_id=material_id,
                        cantidad=1, costo=material.costo, porcentaje_descuento=0, descuento=0, total=material.costo
                    )
                    detalle_add.save()

                # imagenes
                lista_imagenes = datos['lista_imagenes']
                lista_eliminar = []
                # recuperamos las imagenes para eliminar
                imagenes_db = apps.get_model('ventas', 'VentasImagenes').objects.filter(venta_id=venta_actual)
                for imagen_db in imagenes_db:
                    full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen_db.imagen)
                    full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen_db.imagen_thumb)
                    dato_eliminar = {}
                    dato_eliminar['imagen'] = full_filename
                    dato_eliminar['imagen_thumb'] = full_filename_thumb
                    dato_eliminar['venta_imagen_id'] = imagen_db.venta_imagen_id
                    lista_eliminar.append(dato_eliminar)

                for imagen in lista_imagenes:
                    # copiamos a venta y borramos de tmp
                    uploaded_filename = imagen['imagen']
                    system_controller = SystemController()
                    aux = system_controller.nombre_imagen('ventas', uploaded_filename)
                    full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', aux['nombre_archivo'])
                    full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', aux['nombre_archivo_thumb'])

                    full_filename_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', imagen['imagen'])
                    full_filename_thumb_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', imagen['imagen_thumb'])

                    shutil.move(full_filename_ori, full_filename)
                    shutil.move(full_filename_thumb_ori, full_filename_thumb)

                    # creamos el registro
                    imagen_add = apps.get_model('ventas', 'VentasImagenes').objects.create(
                        imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'], status_id=self.status_activo,
                        created_at='now', updated_at='now', venta_id=venta_actual
                    )
                    imagen_add.save()

                # eliminamos las anteriores imagenes
                for imagen_eliminar in lista_eliminar:
                    venta_imagen_db = apps.get_model('ventas', 'VentasImagenes').objects.get(pk=imagen_eliminar['venta_imagen_id'])
                    venta_imagen_db.delete()
                    os.remove(imagen_eliminar['imagen'])
                    os.remove(imagen_eliminar['imagen_thumb'])

                # actualizamos el stock
                stock_actual = apps.get_model('inventarios', 'Stock').objects.get(pk=datos['stock_id'])
                stock_actual.vendida = 1
                stock_actual.updated_at = datos['updated_at']
                stock_actual.save()

                # registramos el ingreso a caja
                datos_ingreso = {}
                datos_ingreso['caja_id'] = datos['caja_id']
                datos_ingreso['punto_id'] = venta_actual.punto_id
                datos_ingreso['user_perfil_id'] = datos['user_perfil_id']
                datos_ingreso['status_id'] = self.status_activo
                datos_ingreso['fecha'] = datos['updated_at']
                datos_ingreso['concepto'] = 'Pago a cuenta, venta: ' + str(venta_actual.numero_venta)
                datos_ingreso['monto'] = venta_actual.a_cuenta
                datos_ingreso['venta_id'] = venta_actual.venta_id
                datos_ingreso['pago_inicial'] = 1
                datos_ingreso['created_at'] = 'now'
                datos_ingreso['updated_at'] = 'now'

                if venta_actual.tipo_venta == 'contado':
                    ci_controller = CajasIngresosController()
                    if not ci_controller.add_db(**datos_ingreso):
                        self.error_operation = 'Error al registrar el ingreso a caja'
                        transaction.set_rollback(True)
                        return False
                else:
                    # creamos el plan de pagos
                    campos_pp = {}
                    campos_pp['venta_id'] = venta_actual
                    campos_pp['cliente_id'] = venta_actual.cliente_id.cliente_id
                    campos_pp['punto_id'] = venta_actual.punto_id.punto_id
                    campos_pp['fecha'] = datos['fecha_planpagos']
                    campos_pp['concepto'] = 'Plan de Pagos, venta: ' + str(venta_actual.numero_venta)
                    campos_pp['numero_cuotas'] = int(datos['cuotas_planpagos'])
                    campos_pp['monto_total'] = venta_actual.total
                    campos_pp['cuota_inicial'] = 0
                    campos_pp['saldo'] = venta_actual.total
                    campos_pp['mensual_dias'] = 'tipo_dias'

                    campos_pp['fecha_fija'] = datos['fecha_planpagos']
                    campos_pp['dias'] = datos['dias_planpagos']

                    # if datos['tipo_pp'] == 'tipo_fecha':
                    #     campos_pp['dia_mensual'] = int(get_day_from_date(datos['fecha_fija'], formato_ori='yyyy-mm-dd HH:ii:ss'))
                    #     campos_pp['tiempo_dias'] = 0
                    # else:
                    campos_pp['dia_mensual'] = 0
                    campos_pp['tiempo_dias'] = int(datos['dias_planpagos'])

                    campos_pp['status_id'] = self.status_activo
                    campos_pp['user_perfil_id'] = datos['user_perfil_id']
                    campos_pp['created_at'] = datos['updated_at']
                    campos_pp['updated_at'] = datos['updated_at']

                    plan_pago_create = PlanPagosCreate()
                    if not plan_pago_create.add_plan_pago_db(**campos_pp):
                        self.error_operation = 'Error al agregar el plan de pagos'
                        transaction.set_rollback(True)
                        return False

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros add venta, '+str(ex))
            return False

    def save_finalizado(self, **datos):
        """aniadimos a la base de datos"""
        try:
            if not self.permission_operation(datos['user_perfil_id'], datos['operation']):
                self.error_operation = 'no puede realizar esta operacion'
                return False

            venta = Ventas.objects.get(pk=datos['id'])
            if venta.status_id != self.status_venta:
                self.error_operation = 'esta operacion no es una venta'
                return False

            with transaction.atomic():
                campos_add = {}
                campos_add['user_perfil_id_finaliza'] = datos['user_perfil_id'].user_perfil_id
                campos_add['fecha_finaliza'] = datos['updated_at']
                campos_add['updated_at'] = datos['updated_at']
                campos_add['status_id'] = self.status_finalizado

                venta_actual = Ventas.objects.filter(pk=datos['id'])
                venta_actual.update(**campos_add)

                # recuperamos la venta
                venta_actual = Ventas.objects.get(pk=datos['id'])

                # imagenes
                lista_imagenes = datos['lista_imagenes']
                lista_eliminar = []
                # recuperamos las imagenes para eliminar
                imagenes_db = apps.get_model('ventas', 'VentasImagenes').objects.filter(venta_id=venta_actual)
                for imagen_db in imagenes_db:
                    full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen_db.imagen)
                    full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', imagen_db.imagen_thumb)
                    dato_eliminar = {}
                    dato_eliminar['imagen'] = full_filename
                    dato_eliminar['imagen_thumb'] = full_filename_thumb
                    dato_eliminar['venta_imagen_id'] = imagen_db.venta_imagen_id
                    lista_eliminar.append(dato_eliminar)

                for imagen in lista_imagenes:
                    # copiamos a venta y borramos de tmp
                    uploaded_filename = imagen['imagen']
                    system_controller = SystemController()
                    aux = system_controller.nombre_imagen('ventas', uploaded_filename)
                    full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', aux['nombre_archivo'])
                    full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'ventas', aux['nombre_archivo_thumb'])

                    full_filename_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', imagen['imagen'])
                    full_filename_thumb_ori = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tmp', imagen['imagen_thumb'])

                    shutil.move(full_filename_ori, full_filename)
                    shutil.move(full_filename_thumb_ori, full_filename_thumb)

                    # creamos el registro
                    imagen_add = apps.get_model('ventas', 'VentasImagenes').objects.create(
                        imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'], status_id=self.status_activo,
                        created_at='now', updated_at='now', venta_id=venta_actual
                    )
                    imagen_add.save()

                # eliminamos las anteriores imagenes
                for imagen_eliminar in lista_eliminar:
                    venta_imagen_db = apps.get_model('ventas', 'VentasImagenes').objects.get(pk=imagen_eliminar['venta_imagen_id'])
                    venta_imagen_db.delete()
                    os.remove(imagen_eliminar['imagen'])
                    os.remove(imagen_eliminar['imagen_thumb'])

                if venta_actual.tipo_venta == 'contado':
                    ci_controller = CajasIngresosController()
                    # registramos el ingreso a caja
                    datos_ingreso = {}
                    datos_ingreso['caja_id'] = datos['caja_id']
                    datos_ingreso['punto_id'] = venta_actual.punto_id
                    datos_ingreso['user_perfil_id'] = datos['user_perfil_id']
                    datos_ingreso['status_id'] = self.status_activo
                    datos_ingreso['fecha'] = datos['updated_at']
                    datos_ingreso['concepto'] = 'Pago finalizacion, venta: ' + str(venta_actual.numero_venta)
                    datos_ingreso['monto'] = self.saldo_venta(venta_actual.venta_id)
                    datos_ingreso['venta_id'] = venta_actual.venta_id
                    datos_ingreso['pago_final'] = 1
                    datos_ingreso['created_at'] = 'now'
                    datos_ingreso['updated_at'] = 'now'

                    if not ci_controller.add_db(**datos_ingreso):
                        self.error_operation = 'Error al registrar el ingreso a caja'
                        transaction.set_rollback(True)
                        return False

                if venta_actual.tipo_venta == 'planpagos':
                    saldo = self.saldo_venta(venta_actual.venta_id)
                    if saldo > 0:
                        self.error_operation = "El saldo del plan de pagos de la venta debe ser cero"
                        transaction.set_rollback(True)
                        return False

                # notificacion del cliente
                cliente = apps.get_model('clientes', 'Clientes').objects.get(pk=venta_actual.cliente_id.cliente_id)
                cliente.notificar = int(datos['notificar'])
                cliente.save()

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'error de argumentos, ' + str(ex)
            print('ERROR registros salida almacen, '+str(ex))
            return False

    def add_gasto(self, venta_id, caja, request):
        try:
            caja_controller = CajasController()
            ce_controller = CajasEgresosController()
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)

            saldo_dia = caja_controller.day_balance(fecha=current_date(), Cajas=caja, formato_ori='yyyy-mm-dd')

            monto = validate_number_decimal('monto', request.POST['monto'])
            concepto = validate_string('concepto', request.POST['concepto'], remove_specials='yes')

            if monto > saldo_dia[caja.caja_id]:
                self.error_operation = 'El monto no debe ser mayor a ' + str(saldo_dia[caja.caja_id])
                return False

            # registramos el egreso de caja
            datos_egreso = {}
            datos_egreso['caja_id'] = caja
            datos_egreso['punto_id'] = punto
            datos_egreso['user_perfil_id'] = user_perfil
            datos_egreso['status_id'] = self.status_activo
            datos_egreso['fecha'] = get_date_to_db(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss')
            datos_egreso['concepto'] = concepto
            datos_egreso['monto'] = monto
            datos_egreso['venta_id'] = venta_id
            datos_egreso['created_at'] = 'now'
            datos_egreso['updated_at'] = 'now'

            if not ce_controller.add_db(**datos_egreso):
                self.error_operation = 'Error al registrar el gasto'
                return False

            self.error_operation = ''
            return True

        except Exception as ex:
            self.error_operation = 'Error de registro de gasto, ' + str(ex)
            return False

    def anular_gasto(self, venta_id, caja, request):
        try:
            ce_controller = CajasEgresosController()
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)

            motivo_anula = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')
            ce_id = validate_number_int('caja egreso', request.POST['ce_id'])

            datos_egreso = {}
            datos_egreso['user_perfil_id_anula'] = user_perfil
            datos_egreso['status_id'] = self.status_anulado
            datos_egreso['motivo_anula'] = motivo_anula
            datos_egreso['deleted_at'] = 'now'

            if not ce_controller.delete_db(ce_id, **datos_egreso):
                self.error_operation = 'Error al anular el gasto'
                return False

            self.error_operation = ''
            return True

        except Exception as ex:
            self.error_operation = 'Error al anular el gasto, ' + str(ex)
            return False

    def add_cobro(self, venta_id, caja, request):
        try:
            with transaction.atomic():
                ci_controller = CajasIngresosController()
                user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
                punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)

                monto = validate_number_decimal('monto', request.POST['monto'])
                concepto = validate_string('concepto', request.POST['concepto'], remove_specials='yes')

                saldo_venta = self.saldo_venta(venta_id)
                if saldo_venta == -1000000:
                    return False

                if monto > saldo_venta:
                    self.error_operation = 'El saldo de la venta es ' + str(saldo_venta)
                    return False

                # registramos el egreso de caja
                datos_ingreso = {}
                datos_ingreso['caja_id'] = caja
                datos_ingreso['punto_id'] = punto
                datos_ingreso['user_perfil_id'] = user_perfil
                datos_ingreso['status_id'] = self.status_activo
                datos_ingreso['fecha'] = get_date_to_db(fecha=current_date(), formato_ori='yyyy-mm-dd', formato='yyyy-mm-dd HH:ii:ss')
                datos_ingreso['concepto'] = concepto
                datos_ingreso['monto'] = monto
                datos_ingreso['venta_id'] = venta_id
                datos_ingreso['created_at'] = 'now'
                datos_ingreso['updated_at'] = 'now'

                if not ci_controller.add_db(**datos_ingreso):
                    self.error_operation = 'Error al registrar el cobro'
                    transaction.set_rollback(True)
                    return False

                self.error_operation = ''
                return True

        except Exception as ex:
            self.error_operation = 'Error de registro de cobro, ' + str(ex)
            return False

    def saldo_venta(self, venta_id):
        try:
            venta = Ventas.objects.get(pk=venta_id)
            saldo_venta = venta.total

            # lista de gastos
            lista_ingresos = apps.get_model('cajas', 'CajasIngresos').objects.filter(venta_id=venta.venta_id, status_id=self.status_activo).order_by('caja_ingreso_id')

            cant_ingresos = 0
            for ingreso in lista_ingresos:
                cant_ingresos += 1
                saldo_venta = saldo_venta - ingreso.monto

            return saldo_venta
        except Exception as ex:
            self.error_operation = 'Error al recuperar el saldo de la venta'
            return -1000000

    def anular_cobro(self, venta_id, caja, request):
        try:
            ci_controller = CajasIngresosController()
            user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)

            motivo_anula = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')
            ci_id = validate_number_int('caja ingreso', request.POST['ci_id'])

            datos_ingreso = {}
            datos_ingreso['user_perfil_id_anula'] = user_perfil
            datos_ingreso['status_id'] = self.status_anulado
            datos_ingreso['motivo_anula'] = motivo_anula
            datos_ingreso['deleted_at'] = 'now'

            if not ci_controller.delete_db(ci_id, **datos_ingreso):
                self.error_operation = 'Error al anular el cobro'
                return False

            self.error_operation = ''
            return True

        except Exception as ex:
            self.error_operation = 'Error al anular el cobro, ' + str(ex)
            return False

    def can_anular(self, id, usuario_perfil):
        """verificando si se puede eliminar o no la tabla"""
        try:
            # puede anular el usuario con permiso de la sucursal
            venta = apps.get_model('ventas', 'Ventas').objects.get(pk=id)
            # print('venta: ', venta.status_id.status_id, ' self: ', self.venta)
            permisos = get_permissions_user(usuario_perfil.user_id, settings.MOD_VENTAS)

            venta = Ventas.objects.get(pk=id)
            if venta.status_id.status_id == self.anulado:
                self.error_operation = 'el registro ya esta anulado'
                return False

            if not self.permission_operation(usuario_perfil, 'anular'):
                self.error_operation = 'no tiene permiso para anular este registro'
                return False

            if venta.status_id.status_id == self.venta:
                # verificamos cobros y gastos
                cant_gastos = apps.get_model('cajas', 'CajasEgresos').objects.filter(venta_id=venta.venta_id, status_id=self.status_activo).count()
                if cant_gastos > 0:
                    self.error_operation = 'primero debe anular los gastos de esta venta'
                    return False

                # cantidad de ingresos que sean pago_inicial=0
                cant_ingresos = apps.get_model('cajas', 'CajasIngresos').objects.filter(venta_id=venta.venta_id, status_id=self.status_activo, pago_inicial=0).count()
                if cant_ingresos > 0:
                    self.error_operation = 'primero debe anular los ingresos de esta venta'
                    return False

            if permisos.anular:
                return True

            return False

        except Exception as ex:
            print('error can anular: ', str(ex))
            return False

    def anular(self, request, id):
        """anulando el registro"""
        try:
            usuario_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=request.user)
            if self.can_anular(id, usuario_perfil):

                status_anular = self.status_anulado
                operation = validate_number_int('operation', request.POST['operation'], len_zero='yes')
                if operation == self.preventa:
                    motivo_a = ''
                else:
                    motivo_a = validate_string('motivo anula', request.POST['motivo_anula'], remove_specials='yes')

                campos_update = {}
                almacen = get_almacen_user(request.user)
                campos_update['almacen_id'] = almacen
                campos_update['user_perfil_id'] = usuario_perfil
                campos_update['user_perfil_id_anula'] = usuario_perfil.user_perfil_id
                campos_update['motivo_anula'] = motivo_a
                campos_update['operation'] = operation
                campos_update['status_id'] = status_anular
                campos_update['deleted_at'] = 'now'

                if self.anular_db(id, **campos_update):
                    self.error_operation = ''
                    return True
                else:
                    return False

            else:
                self.error_operation = 'No tiene permiso para anular este registro'
                return False

        except Exception as ex:
            print('Error anular ingreso almacen: ' + str(ex))
            self.error_operation = 'Error al anular el registro, ' + str(ex)
            return False

    def anular_db(self, id, **datos):
        """ anulamos en la bd """
        try:
            if self.can_anular(id, datos['user_perfil_id']):
                with transaction.atomic():
                    if datos['operation'] == self.preventa:
                        campos_update = {}
                        campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                        campos_update['motivo_anula'] = datos['motivo_anula']
                        campos_update['status_id'] = datos['status_id']
                        campos_update['deleted_at'] = datos['deleted_at']

                        # registramos
                        venta_update = Ventas.objects.filter(pk=id)
                        venta_update.update(**campos_update)

                        self.error_operation = ''
                        return True

                    if datos['operation'] == self.venta:
                        campos_update = {}
                        campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                        campos_update['motivo_anula'] = datos['motivo_anula']
                        campos_update['status_id'] = self.status_preventa
                        campos_update['updated_at'] = datos['deleted_at']
                        campos_update['caja_id'] = 0

                        # registramos
                        venta_update = Ventas.objects.filter(pk=id)
                        venta_update.update(**campos_update)

                        venta = Ventas.objects.get(pk=id)

                        # stock
                        stock = apps.get_model('inventarios', 'Stock').objects.get(pk=venta.stock_id)
                        stock.vendida = 0
                        stock.updated_at = datos['deleted_at']
                        stock.save()

                        # ingreso a caja
                        if venta.tipo_venta == 'contado':
                            datos_ingreso = {}
                            datos_ingreso['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                            datos_ingreso['status_id'] = self.status_anulado
                            datos_ingreso['motivo_anula'] = datos['motivo_anula']
                            datos_ingreso['deleted_at'] = datos['deleted_at']

                            # el primer ingreso a caja de la venta
                            caja_ingreso = apps.get_model('cajas', 'CajasIngresos').objects.get(venta_id=venta.venta_id, status_id=self.status_activo, pago_inicial=1)
                            ci_controller = CajasIngresosController()
                            if not ci_controller.delete_db(caja_ingreso.caja_ingreso_id, **datos_ingreso):
                                self.error_operation = 'Error al anular el ingreso a caja'
                                transaction.set_rollback(True)
                                return False

                        if venta.tipo_venta == 'planpagos':
                            # eliminamos el plan de pagos
                            plan_pagos = apps.get_model('ventas', 'PlanPagos').objects.get(venta_id=venta, status_id=self.status_activo)
                            datos_pp = {}
                            datos_pp['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                            datos_pp['status_id'] = self.status_anulado
                            datos_pp['motivo_anula'] = datos['motivo_anula']
                            datos_pp['deleted_at'] = datos['deleted_at']
                            plan_pago_create = PlanPagosCreate()
                            if not plan_pago_create.anular_db(plan_pagos.plan_pago_id, **datos_pp):
                                self.error_operation = 'Error al anular el plan de pagos'
                                transaction.set_rollback(True)
                                return False

                        self.error_operation = ''
                        return True

                    if datos['operation'] == self.finalizado:
                        campos_update = {}
                        campos_update['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                        campos_update['motivo_anula'] = datos['motivo_anula']
                        campos_update['status_id'] = self.status_venta
                        campos_update['updated_at'] = datos['deleted_at']

                        # registramos
                        venta_update = Ventas.objects.filter(pk=id)
                        venta_update.update(**campos_update)

                        # todos los aumentos si es el caso
                        venta = Ventas.objects.get(pk=id)

                        # ingreso a caja
                        if venta.tipo_venta == 'contado':
                            datos_ingreso = {}
                            datos_ingreso['user_perfil_id_anula'] = datos['user_perfil_id_anula']
                            datos_ingreso['status_id'] = self.status_anulado
                            datos_ingreso['motivo_anula'] = datos['motivo_anula']
                            datos_ingreso['deleted_at'] = datos['deleted_at']

                            # el primer ingreso a caja de la venta
                            caja_ingreso = apps.get_model('cajas', 'CajasIngresos').objects.get(venta_id=venta.venta_id, status_id=self.status_activo, pago_final=1)
                            ci_controller = CajasIngresosController()
                            if not ci_controller.delete_db(caja_ingreso.caja_ingreso_id, **datos_ingreso):
                                self.error_operation = 'Error al anular el registro de caja'
                                transaction.set_rollback(True)
                                return False

                        self.error_operation = ''
                        return True

                    self.error_operation = 'operation no valid'
                    return False
            else:
                self.error_operation = 'No tiene permiso para anular este registro'
                return False

        except Exception as ex:
            print('Error anular venta db: ' + str(ex))
            self.error_operation = 'Error de argumentos, ' + str(ex)
            return False

    def get_historias(self, cliente_id):
        # recuperamos las ventas del cliente en estado finalizado
        listado = []
        cliente = apps.get_model('clientes', 'Clientes').objects.get(pk=cliente_id)
        lista_ventas = apps.get_model('ventas', 'Ventas').objects.filter(cliente_id=cliente, status_id=self.status_finalizado).order_by('fecha_preventa')
        for venta in lista_ventas:
            detalles = apps.get_model('ventas', 'VentasDetalles').objects.filter(venta_id=venta)
            tipo_montura = ''
            materiales = []
            for detalle in detalles:
                if detalle.tipo_montura_id == 0:
                    material = apps.get_model('configuraciones', 'Materiales').objects.get(pk=detalle.material_id)
                    dato = {}
                    dato['material_id'] = material.material_id
                    dato['material'] = material.material
                    materiales.append(dato)
                else:
                    obj_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=detalle.tipo_montura_id)
                    tipo_montura = obj_montura.proveedor_id.proveedor + ' - ' + obj_montura.tipo_montura

            laboratorio = ''
            tecnico = ''
            oftalmologo = ''
            if venta.laboratorio_id != 0:
                obj_lab = apps.get_model('configuraciones', 'Laboratorios').objects.get(pk=venta.laboratorio_id)
                laboratorio = obj_lab.laboratorio
            if venta.tecnico_id != 0:
                obj_tec = apps.get_model('configuraciones', 'Tecnicos').objects.get(pk=venta.tecnico_id)
                tecnico = obj_tec.tecnico
            if venta.oftalmologo_id != 0:
                obj_oft = apps.get_model('configuraciones', 'Oftalmologos').objects.get(pk=venta.oftalmologo_id)
                oftalmologo = obj_oft.oftalmologo

            # lista de imagenes
            lista_imagenes = []
            listado_imagenes = apps.get_model('ventas', 'VentasImagenes').objects.filter(venta_id=venta).order_by('venta_imagen_id')
            for imagen in listado_imagenes:
                dato_img = {}
                dato_img['imagen_id'] = imagen.venta_imagen_id
                dato_img['imagen'] = imagen.imagen
                dato_img['imagen_thumb'] = imagen.imagen_thumb
                lista_imagenes.append(dato_img)

            # unimos de 2 en 2
            lista_par = []
            index = 0
            while index < len(lista_imagenes)-1:
                dato_img = {}
                dato_img['imagen_id'] = lista_imagenes[index]['imagen_id']
                dato_img['imagen'] = lista_imagenes[index]['imagen']
                dato_img['imagen_thumb'] = lista_imagenes[index]['imagen_thumb']
                # col 2
                dato_img2 = {}
                dato_img2['imagen_id'] = lista_imagenes[index+1]['imagen_id']
                dato_img2['imagen'] = lista_imagenes[index+1]['imagen']
                dato_img2['imagen_thumb'] = lista_imagenes[index+1]['imagen_thumb']

                new_data = {}
                new_data['col1'] = dato_img
                new_data['col2'] = dato_img2
                lista_par.append(new_data)

                index += 2

            if len(lista_imagenes) > 0 and index < len(lista_imagenes):
                # queda un registro sin par
                dato_img = {}
                dato_img['imagen_id'] = lista_imagenes[index]['imagen_id']
                dato_img['imagen'] = lista_imagenes[index]['imagen']
                dato_img['imagen_thumb'] = lista_imagenes[index]['imagen_thumb']
                # col 2
                dato_img2 = {}
                dato_img2['imagen_id'] = 0
                dato_img2['imagen'] = ''
                dato_img2['imagen_thumb'] = ''

                new_data = {}
                new_data['col1'] = dato_img
                new_data['col2'] = dato_img2
                lista_par.append(new_data)

            data = {}
            data['venta_id'] = venta.venta_id
            data['nombres'] = venta.nombres
            data['apellidos'] = venta.apellidos
            data['fecha_preventa'] = venta.fecha_preventa
            data['total'] = venta.total

            data['tipo_montura'] = tipo_montura
            data['materiales'] = materiales
            data['laboratorio'] = laboratorio
            data['tecnico'] = tecnico
            data['oftalmologo'] = oftalmologo
            data['nota'] = venta.nota
            data['lejos_di'] = venta.lejos_di
            data['lejos_od_esf'] = venta.lejos_od_esf
            data['lejos_od_cli'] = venta.lejos_od_cli
            data['lejos_od_eje'] = venta.lejos_od_eje
            data['lejos_oi_esf'] = venta.lejos_oi_esf
            data['lejos_oi_cli'] = venta.lejos_oi_cli
            data['lejos_oi_eje'] = venta.lejos_oi_eje
            data['cerca_di'] = venta.cerca_di
            data['cerca_od_esf'] = venta.cerca_od_esf
            data['cerca_od_cli'] = venta.cerca_od_cli
            data['cerca_od_eje'] = venta.cerca_od_eje
            data['cerca_oi_esf'] = venta.cerca_oi_esf
            data['cerca_oi_cli'] = venta.cerca_oi_cli
            data['cerca_oi_eje'] = venta.cerca_oi_eje
            data['lista_imagenes'] = lista_par

            listado.append(data)

        return listado
