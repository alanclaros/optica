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


class DisenioLentesController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'DisenioLentes'
        self.modelo_id = 'disenio_lente_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_DISENIO_LENTES

        # variables de session
        self.modulo_session = "disenio_lentes"
        self.columnas.append('disenio_lente')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_disenio_lente')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_disenio_lente'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'productos': 'Productos'}

        # control del formulario
        self.control_form = "txt|2|S|disenio_lente|Disenio Lentes"
        self.control_form += ";txt|2|S|codigo|Codigo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # disenio_lente
        if self.variables_filtros_values['search_disenio_lente'].strip() != "":
            self.filtros_modulo['disenio_lente__icontains'] = self.variables_filtros_values['search_disenio_lente'].strip()

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
        filtros['disenio_lente__in'] = [nuevo_valor]
        if id > 0:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos una nueva disenio_lente"""
        system_controller = SystemController()

        try:
            disenio_lente_txt = validate_string('disenio_lente', request.POST['disenio_lente'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            descripcion = validate_string('descripcion', request.POST['descripcion'], remove_specials='yes', len_zero='yes')
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            if not self.is_in_db(id, disenio_lente_txt):
                if 'activo' in request.POST.keys():
                    status_disenio_lente = self.status_activo
                else:
                    status_disenio_lente = self.status_inactivo

                aux = {}
                aux['nombre_archivo'] = ''
                aux['nombre_archivo_thumb'] = ''
                if 'imagen1' in request.FILES.keys():
                    uploaded_filename = request.FILES['imagen1'].name.strip()

                    if uploaded_filename != '':
                        aux = system_controller.nombre_imagen('disenio_lentes', uploaded_filename)
                        # aux = system_controller self.nombre_imagen(uploaded_filename)

                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'disenio_lentes', aux['nombre_archivo'])
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'disenio_lentes', aux['nombre_archivo_thumb'])

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

                if type == 'add':
                    disenio_lente = apps.get_model('configuraciones', 'DisenioLentes').objects.create(disenio_lente=disenio_lente_txt, codigo=codigo_txt,
                                                                                                      descripcion=descripcion, imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'], status_id=status_disenio_lente, created_at='now', updated_at='now')
                    disenio_lente.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    disenio_lente = apps.get_model('configuraciones', 'DisenioLentes').objects.get(pk=id)
                    # verificamos imagen
                    if disenio_lente.imagen != '':
                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'disenio_lentes', disenio_lente.imagen)
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'disenio_lentes', disenio_lente.imagen_thumb)

                        if os.path.exists(full_filename):
                            remove(full_filename)
                        if os.path.exists(full_filename_thumb):
                            remove(full_filename_thumb)

                    if aux['nombre_archivo'] != '':
                        # guardamos la nueva imagen
                        disenio_lente.imagen = aux['nombre_archivo']
                        disenio_lente.imagen_thumb = aux['nombre_archivo_thumb']

                    # datos
                    disenio_lente.status_id = status_disenio_lente
                    disenio_lente.disenio_lente = disenio_lente_txt
                    disenio_lente.codigo = codigo_txt
                    disenio_lente.descripcion = descripcion
                    disenio_lente.updated_at = 'now'
                    disenio_lente.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operation no valid'
                return False

            else:
                self.error_operation = "Ya existe este disenio de lentes: " + disenio_lente_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el disenio de lentes, " + str(ex)
            return False
