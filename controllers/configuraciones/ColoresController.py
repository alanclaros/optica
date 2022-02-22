from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from utils.validators import validate_number_int, validate_string
from controllers.SystemController import SystemController
import os
from os import remove

# imagenes
from django.core.files.base import ContentFile
from PIL import Image


class ColoresController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Colores'
        self.modelo_id = 'color_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_COLORES

        # variables de session
        self.modulo_session = "colores"
        self.columnas.append('color')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_color')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_color'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'productos': 'Productos'}

        # control del formulario
        self.control_form = "txt|2|S|color|Color"
        self.control_form += ";txt|2|S|codigo|Codigo"
        self.control_form += ";txt|6|S|color_hex|Color Hexadecimal"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # color
        if self.variables_filtros_values['search_color'].strip() != "":
            self.filtros_modulo['color__icontains'] = self.variables_filtros_values['search_color'].strip()

        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['codigo__icontains'] = self.variables_filtros_values['search_codigo'].strip()

        # paginacion, paginas y definiendo el LIMIT *,*
        self.pagination()
        # asigamos la paginacion a la session
        request.session[self.modulo_session]['pages_list'] = self.pages_list

        # recuperamos los datos
        return self.get_list()

    def is_in_db(self, id, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['color__in'] = [nuevo_valor]
        if id > 0:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos una nueva color"""
        system_controller = SystemController()

        try:
            color_txt = validate_string('color', request.POST['color'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            color_hex = validate_string('color_hex', request.POST['color_hex'], remove_specials='yes', len_zero='yes')
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            if not self.is_in_db(id, color_txt):
                if 'activo' in request.POST.keys():
                    status_color = self.status_activo
                else:
                    status_color = self.status_inactivo

                if type == 'add':
                    color = apps.get_model('configuraciones', 'Colores').objects.create(color=color_txt, codigo=codigo_txt,
                                                                                        color_hex=color_hex, status_id=status_color, created_at='now', updated_at='now')
                    color.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    color = apps.get_model('configuraciones', 'Colores').objects.get(pk=id)

                    # datos
                    color.status_id = status_color
                    color.color = color_txt
                    color.codigo = codigo_txt
                    color.color_hex = color_hex
                    color.updated_at = 'now'
                    color.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operation no valid'
                return False

            else:
                self.error_operation = "Ya existe este color: " + color_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el color, " + str(ex)
            return False
