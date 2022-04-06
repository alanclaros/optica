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


class MaterialesController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Materiales'
        self.modelo_id = 'material_id'
        self.modelo_app = 'configuraciones'
        self.modulo_id = settings.MOD_MATERIALES

        # variables de session
        self.modulo_session = "materiales"
        self.columnas.append('material')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_material')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_material'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'productos': 'Productos'}

        # control del formulario
        self.control_form = "txt|2|S|material|Material"
        self.control_form += ";txt|2|S|codigo|Codigo"
        self.control_form += ";cbo|0|S|proveedor_id|Proveedor"
        #self.control_form += ";txt|1|S|costo|Costo"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]

        # material
        if self.variables_filtros_values['search_material'].strip() != "":
            self.filtros_modulo['material__icontains'] = self.variables_filtros_values['search_material'].strip()

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
        filtros['material__in'] = [nuevo_valor]
        if id > 0:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        # si no existe
        if cantidad > 0:
            return True

        return False

    def save(self, request, type='add'):
        """aniadimos una nueva material"""
        system_controller = SystemController()

        try:
            material_txt = validate_string('material', request.POST['material'], remove_specials='yes')
            codigo_txt = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            costo_txt = validate_number_decimal('costo', request.POST['costo'], len_zero='yes')
            descripcion = validate_string('descripcion', request.POST['descripcion'], remove_specials='yes', len_zero='yes')
            proveedor_id = validate_number_int('proveedor_id', request.POST['proveedor_id'])
            id = validate_number_int('id', request.POST['id'], len_zero='yes')

            proveedor = apps.get_model('configuraciones', 'Proveedores').objects.get(pk=proveedor_id)

            if not self.is_in_db(id, material_txt):
                if 'activo' in request.POST.keys():
                    status_material = self.status_activo
                else:
                    status_material = self.status_inactivo

                aux = {}
                aux['nombre_archivo'] = ''
                aux['nombre_archivo_thumb'] = ''
                if 'imagen1' in request.FILES.keys() and request.FILES['imagen1'].name.strip() != '':
                    uploaded_filename = request.FILES['imagen1'].name.strip()
                    aux = system_controller.nombre_imagen('materiales', uploaded_filename)

                    full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'materiales', aux['nombre_archivo'])
                    full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'materiales', aux['nombre_archivo_thumb'])

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
                        aux = system_controller.nombre_imagen('materiales', settings.PRODUCTOS_NO_IMAGE)
                        full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'materiales', aux['nombre_archivo'])
                        full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'materiales', aux['nombre_archivo_thumb'])

                        shutil.copyfile(os.path.join(settings.STATIC_ROOT_APP, 'img', settings.PRODUCTOS_NO_IMAGE), full_filename)
                        shutil.copyfile(os.path.join(settings.STATIC_ROOT_APP, 'img', settings.PRODUCTOS_NO_IMAGE), full_filename_thumb)

                if type == 'add':
                    material = apps.get_model('configuraciones', 'Materiales').objects.create(material=material_txt, codigo=codigo_txt, costo=costo_txt, proveedor_id=proveedor,
                                                                                              descripcion=descripcion, imagen=aux['nombre_archivo'], imagen_thumb=aux['nombre_archivo_thumb'], status_id=status_material, created_at='now', updated_at='now')
                    material.save()
                    self.error_operation = ""
                    return True

                if type == 'modify':
                    material = apps.get_model('configuraciones', 'Materiales').objects.get(pk=id)
                    # verificamos imagen
                    if aux['nombre_archivo'] != '':
                        # se cambio de archivo
                        if material.imagen != '':
                            full_filename = os.path.join(settings.STATIC_ROOT_APP, 'media', 'materiales', material.imagen)
                            full_filename_thumb = os.path.join(settings.STATIC_ROOT_APP, 'media', 'materiales', material.imagen_thumb)

                            if os.path.exists(full_filename):
                                remove(full_filename)
                            if os.path.exists(full_filename_thumb):
                                remove(full_filename_thumb)

                        # guardamos la nueva imagen
                        material.imagen = aux['nombre_archivo']
                        material.imagen_thumb = aux['nombre_archivo_thumb']

                    # datos
                    material.status_id = status_material
                    material.material = material_txt
                    material.codigo = codigo_txt
                    material.costo = costo_txt
                    material.descripcion = descripcion
                    material.proveedor_id = proveedor
                    material.updated_at = 'now'
                    material.save()
                    self.error_operation = ""
                    return True

                self.error_operation = 'Operation no valid'
                return False

            else:
                self.error_operation = "Ya existe este material: " + material_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar el material, " + str(ex)
            return False
