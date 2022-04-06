from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from utils.validators import validate_number_int, validate_string
from controllers.SystemController import SystemController
import os
import shutil
from os import remove

# imagenes
from django.core.files.base import ContentFile
from PIL import Image


class LaboratoriosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Laboratorios'
        self.modelo_id = 'laboratorio_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_LABORATORIOS

        # variables de session
        self.modulo_session = "laboratorios"
        self.columnas.append('laboratorio')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_laboratorio')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_laboratorio'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'ventas': 'Ventas'}

        # control del formulario
        self.control_form = "txt|2|S|laboratorio|Laboratorio"
        self.control_form += ";txt|2|S|codigo|Codigo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # laboratorio
        if self.variables_filtros_values['search_laboratorio'].strip() != "":
            self.filtros_modulo['laboratorio__icontains'] = self.variables_filtros_values['search_laboratorio'].strip()

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
        filtros['laboratorio__in'] = [nuevo_valor]
        if id > 0:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos una nueva laboratorio"""
        system_controller = SystemController()

        try:
            laboratorio_txt = validate_string('laboratorio', request.POST['laboratorio'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            descripcion = validate_string('descripcion', request.POST['descripcion'], remove_specials='yes', len_zero='yes')
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            if not self.is_in_db(id, laboratorio_txt):
                if 'activo' in request.POST.keys():
                    status_laboratorio = self.status_activo
                else:
                    status_laboratorio = self.status_inactivo

                aux = {}
                aux['nombre_archivo'] = ''
                aux['nombre_archivo_thumb'] = ''
                if 'imagen1' in request.FILES.keys() and request.FILES['imagen1'].name.strip() != '':
                    uploaded_filename = request.FILES['imagen1'].name.strip()
                    aux = system_controller.nombre_imagen('laboratorios', uploaded_filename)

                    full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'laboratorios', aux['nombre_archivo'])
                    full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'laboratorios', aux['nombre_archivo_thumb'])

                    fout = open(full_filename, 'wb+')
                    file_content = ContentFile(request.FILES['imagen1'].read())
                    for chunk in file_content.chunks():
                        fout.write(chunk)
                    fout.close()

                    # creamos el thumb
                    imagen = Image.open(full_filename)
                    max_size = (settings.PRODUCTOS_THUMB_WIDTH, settings.PRODUCTOS_THUMB_HEIGHT)
                    imagen.thumbnail(max_size)
                    imagen.save(full_filename_thumb)
                else:
                    if type == 'add':
                        aux = system_controller.nombre_imagen('laboratorios', settings.PRODUCTOS_NO_IMAGE)
                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'laboratorios', aux['nombre_archivo'])
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'laboratorios', aux['nombre_archivo_thumb'])

                        shutil.copyfile(os.path.join(settings.STATIC_ROOT_APP, 'img', settings.PRODUCTOS_NO_IMAGE), full_filename)
                        shutil.copyfile(os.path.join(settings.STATIC_ROOT_APP, 'img', settings.PRODUCTOS_NO_IMAGE), full_filename_thumb)

                if type == 'add':
                    laboratorio = apps.get_model('configuraciones', 'Laboratorios').objects.create(laboratorio=laboratorio_txt, codigo=codigo_txt,
                                                                                                   descripcion=descripcion, imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'],
                                                                                                   status_id=status_laboratorio, created_at='now', updated_at='now')
                    laboratorio.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    laboratorio = apps.get_model('configuraciones', 'Laboratorios').objects.get(pk=id)

                    # verificamos imagen
                    if aux['nombre_archivo'] != '':
                        # se cambio de imagen
                        if laboratorio.imagen != '':
                            full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'laboratorios', laboratorio.imagen)
                            full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'laboratorios', laboratorio.imagen_thumb)

                            if os.path.exists(full_filename):
                                remove(full_filename)
                            if os.path.exists(full_filename_thumb):
                                remove(full_filename_thumb)

                        # guardamos la nueva imagen
                        laboratorio.imagen = aux['nombre_archivo']
                        laboratorio.imagen_thumb = aux['nombre_archivo_thumb']

                    # datos
                    laboratorio.status_id = status_laboratorio
                    laboratorio.laboratorio = laboratorio_txt
                    laboratorio.codigo = codigo_txt
                    laboratorio.descripcion = descripcion
                    laboratorio.updated_at = 'now'
                    laboratorio.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operation no valid'
                return False

            else:
                self.error_operation = "Ya existe este laboratorio: " + laboratorio_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el laboratorio, " + str(ex)
            return False
