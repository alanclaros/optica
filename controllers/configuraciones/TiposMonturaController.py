from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from utils.validators import validate_number_int, validate_string, validate_number_decimal
from controllers.SystemController import SystemController
import os
import shutil
from os import remove

# imagenes
from django.core.files.base import ContentFile
from PIL import Image


class TiposMonturaController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'TiposMontura'
        self.modelo_id = 'tipo_montura_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_TIPOS_MONTURA

        # variables de session
        self.modulo_session = "tipos_montura"
        self.columnas.append('tipo_montura')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_tipo_montura')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_tipo_montura'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'productos': 'Productos'}

        # control del formulario
        self.control_form = "txt|2|S|tipo_montura|Tipo Montura"
        self.control_form += ";txt|2|S|codigo|Codigo"
        #self.control_form += ";txt|1|S|costo|Costo"
        self.control_form += ";txt|1|S|numero_actual|Numero Actual"
        self.control_form += ";cbo|0|S|proveedor_id|Proveedor"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # tipo_montura
        if self.variables_filtros_values['search_tipo_montura'].strip() != "":
            self.filtros_modulo['tipo_montura__icontains'] = self.variables_filtros_values['search_tipo_montura'].strip()

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
        filtros['tipo_montura__in'] = [nuevo_valor]
        if id > 0:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos una nueva tipo_montura"""
        system_controller = SystemController()

        try:
            tipo_montura_txt = validate_string('tipo_montura', request.POST['tipo_montura'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            costo_txt = validate_number_decimal('costo', request.POST['costo'], len_zero='yes')
            descripcion = validate_string('descripcion', request.POST['descripcion'], remove_specials='yes', len_zero='yes')
            numero_actual = validate_number_int('numero actual', request.POST['numero_actual'], len_zero='yes')
            proveedor_id = validate_number_int('proveedor_id', request.POST['proveedor_id'])
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            proveedor = apps.get_model('configuraciones', 'Proveedores').objects.get(pk=proveedor_id)

            if not self.is_in_db(id, tipo_montura_txt):
                if 'activo' in request.POST.keys():
                    status_tipo_montura = self.status_activo
                else:
                    status_tipo_montura = self.status_inactivo

                aux = {}
                aux['nombre_archivo'] = ''
                aux['nombre_archivo_thumb'] = ''
                if 'imagen1' in request.FILES.keys() and request.FILES['imagen1'].name.strip() != '':
                    uploaded_filename = request.FILES['imagen1'].name.strip()
                    aux = system_controller.nombre_imagen('tipos_montura', uploaded_filename)

                    full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tipos_montura', aux['nombre_archivo'])
                    full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tipos_montura', aux['nombre_archivo_thumb'])

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
                        aux = system_controller.nombre_imagen('tipos_montura', settings.PRODUCTOS_NO_IMAGE)
                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tipos_montura', aux['nombre_archivo'])
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tipos_montura', aux['nombre_archivo_thumb'])

                        shutil.copyfile(os.path.join(settings.STATIC_ROOT_APP, 'img', settings.PRODUCTOS_NO_IMAGE), full_filename)
                        shutil.copyfile(os.path.join(settings.STATIC_ROOT_APP, 'img', settings.PRODUCTOS_NO_IMAGE), full_filename_thumb)

                if type == 'add':
                    tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.create(tipo_montura=tipo_montura_txt, codigo=codigo_txt, costo=costo_txt, proveedor_id=proveedor, numero_actual=numero_actual,
                                                                                                    descripcion=descripcion, imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'], status_id=status_tipo_montura, created_at='now', updated_at='now')
                    tipo_montura.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=id)
                    # verificamos imagen
                    if aux['nombre_archivo'] != '':
                        # se cambio de imagen
                        if tipo_montura.imagen != '':
                            full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tipos_montura', tipo_montura.imagen)
                            full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'tipos_montura', tipo_montura.imagen_thumb)

                            if os.path.exists(full_filename):
                                remove(full_filename)
                            if os.path.exists(full_filename_thumb):
                                remove(full_filename_thumb)

                        # guardamos la nueva imagen
                        tipo_montura.imagen = aux['nombre_archivo']
                        tipo_montura.imagen_thumb = aux['nombre_archivo_thumb']

                    # datos
                    tipo_montura.status_id = status_tipo_montura
                    tipo_montura.tipo_montura = tipo_montura_txt
                    tipo_montura.codigo = codigo_txt
                    tipo_montura.costo = costo_txt
                    tipo_montura.proveedor_id = proveedor
                    tipo_montura.descripcion = descripcion
                    tipo_montura.numero_actual = numero_actual
                    tipo_montura.updated_at = 'now'
                    tipo_montura.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operation no valid'
                return False

            else:
                self.error_operation = "Ya existe este tipo de montura: " + tipo_montura_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el tipo de montura, " + str(ex)
            return False
