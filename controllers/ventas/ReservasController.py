from controllers.DefaultValues import DefaultValues
from django.apps import apps
from django.conf import settings
from datetime import datetime

from utils.dates_functions import get_calendario_actividades


class ReservasController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Reservas'
        self.modelo_id = 'reserva_id'
        self.modelo_app = 'reservas'
        self.modulo_id = settings.MOD_RESERVAS

        # variables de session
        self.modulo_session = "reservas"
        self.columnas.append('fecha_inicio')
        self.columnas.append('nombres')
        self.columnas.append('apellidos')
        self.columnas.append('telefonos')

        self.variables_filtros.append('search_periodo')
        self.variables_filtros.append('search_nombres')
        self.variables_filtros.append('search_apellidos')
        self.variables_filtros.append('search_telefonos')

        self.variables_filtros_defecto['search_apellidos'] = ''
        self.variables_filtros_defecto['search_nombres'] = ''
        self.variables_filtros_defecto['search_telefonos'] = ''

        anio = '20' + str(datetime.now().year) if len(str(datetime.now().year)) == 2 else str(datetime.now().year)
        mes = '0' + str(datetime.now().month) if len(str(datetime.now().month)) == 1 else str(datetime.now().month)
        self.variables_filtros_defecto['search_periodo'] = anio + mes

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

        periodo = self.variables_filtros_values['search_periodo'].strip()
        nombres = self.variables_filtros_values['search_nombres'].strip()
        apellidos = self.variables_filtros_values['search_apellidos'].strip()
        telefonos = self.variables_filtros_values['search_telefonos'].strip()

        calendario = get_calendario_actividades(periodo, nombres, apellidos, telefonos)

        # recuperamos los datos
        return calendario

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
