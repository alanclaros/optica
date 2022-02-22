from decimal import Decimal
from controllers.DefaultValues import DefaultValues
from django.conf import settings
from django.apps import apps

from productos.models import Productos, ProductosRelacionados, ProductosImagenes
from permisos.models import UsersPerfiles
from configuraciones.models import Puntos, Lineas
from status.models import Status

from django.db import transaction

# conexion directa a la base de datos
from django.db import connection

from utils.validators import validate_string, validate_number_int, validate_number_decimal

from controllers.SystemController import SystemController


class ProductosController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)
        self.modelo_name = 'Productos'
        self.modelo_id = 'producto_id'
        self.modelo_app = 'productos'
        self.modulo_id = settings.MOD_PRODUCTOS

        # variables de session
        self.modulo_session = "productos"
        self.columnas.append('linea_id__linea')
        self.columnas.append('producto')
        self.columnas.append('codigo')

        self.variables_filtros.append('search_linea')
        self.variables_filtros.append('search_producto')
        self.variables_filtros.append('search_codigo')

        self.variables_filtros_defecto['search_linea'] = ''
        self.variables_filtros_defecto['search_producto'] = ''
        self.variables_filtros_defecto['search_codigo'] = ''

        self.variable_page = "page"
        self.variable_page_defecto = "1"
        self.variable_order = "search_order"
        self.variable_order_value = self.columnas[0]
        self.variable_order_type = "search_order_type"

        # tablas donde se debe verificar para eliminar
        self.modelos_eliminar = {'ventas': 'VentasDetalles'}

        # control del formulario
        self.control_form = "txt|2|S|producto|Producto;"
        self.control_form += "txt|2|S|codigo|Codigo;"
        self.control_form += "txt|1|S|precio|Precio;"
        self.control_form += "cbo|0|S|linea_id|Linea;"
        self.control_form += "cbo|0|S|tipo_montura_id|Tipo Montura;"
        self.control_form += "cbo|0|S|disenio_lente_id|Disenio Lentes;"
        self.control_form += "cbo|0|S|material_id|Material;"
        self.control_form += "cbo|0|S|marca_id|Marca;"
        self.control_form += "cbo|0|S|color_id|Color;"
        self.control_form += "cbo|0|S|proveedor_id|Proveedor"

    def index(self, request):
        DefaultValues.index(self, request)
        self.filtros_modulo.clear()
        # status
        self.filtros_modulo['status_id_id__in'] = [self.activo, self.inactivo]
        # linea
        if self.variables_filtros_values['search_linea'].strip() != "":
            self.filtros_modulo['linea_id__linea__icontains'] = self.variables_filtros_values['search_linea'].strip()
        # producto
        if self.variables_filtros_values['search_producto'].strip() != "":
            self.filtros_modulo['producto__icontains'] = self.variables_filtros_values['search_producto'].strip()
        # codigo
        if self.variables_filtros_values['search_codigo'].strip() != "":
            self.filtros_modulo['codigo__icontains'] = self.variables_filtros_values['search_codigo'].strip()

        # paginacion, paginas y definiendo el LIMIT *,*
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
        retorno = modelo.objects.select_related('linea_id').filter(**self.filtros_modulo).order_by(orden_enviar)[self.pages_limit_botton:self.pages_limit_top]
        # for key, value in retorno.__dict__.items():
        #     print('key:', key, ' value:', value)

        return retorno

    def is_in_db(self, id, nuevo_valor):
        """verificamos si existe en la base de datos"""
        modelo = apps.get_model(self.modelo_app, self.modelo_name)
        filtros = {}
        filtros['status_id_id__in'] = [self.activo, self.inactivo]
        filtros['producto__iexact'] = nuevo_valor

        if id:
            cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        else:
            cantidad = modelo.objects.filter(**filtros).count()

        #print('cantidad...: ', cantidad)
        # si no existe
        if cantidad > 0:
            return True

        return False

    def is_codigo_barras_db(self, id, codigo_barras):
        """verificando el codigo de barras"""

        # ahora sin control de codigo de barras
        # modelo = apps.get_model(self.modelo_app, self.modelo_name)
        # filtros = {}
        # filtros['status_id_id__in'] = [self.activo, self.inactivo]
        # filtros['codigo_barras__iexact'] = codigo_barras
        #
        # if id:
        #     cantidad = modelo.objects.filter(**filtros).exclude(pk=id).count()
        # else:
        #     cantidad = modelo.objects.filter(**filtros).count()
        #
        # # si no existe
        # if cantidad > 0:
        #     return True

        return False

    def save(self, request, type='add'):
        """aniadimos un nuevo producto"""
        try:
            linea_id = validate_number_int('linea', request.POST['linea_id'])
            producto_txt = validate_string('producto', request.POST['producto'], remove_specials='yes')
            codigo = validate_string('codigo', request.POST['codigo'], remove_specials='yes')
            precio = validate_number_decimal('precio', request.POST['precio'])
            precio_oferta = validate_number_decimal('precio_oferta', request.POST['precio_oferta'], len_zero='yes')
            tipo_montura_id = validate_number_int('tipo montura', request.POST['tipo_montura_id'])
            disenio_lente_id = validate_number_int('disenio lentes', request.POST['disenio_lente_id'])
            material_id = validate_number_int('material', request.POST['material_id'])
            marca_id = validate_number_int('marca', request.POST['marca_id'])
            color_id = validate_number_int('color', request.POST['color_id'])
            proveedor_id = validate_number_int('proveedor', request.POST['proveedor_id'])
            stock_minimo = validate_number_int('stock minimo', request.POST['stock_minimo'])
            activo = 1 if 'activo' in request.POST.keys() else 0
            novedad = 1 if 'novedad' in request.POST.keys() else 0
            mas_vendido = 1 if 'mas_vendido' in request.POST.keys() else 0
            oferta = 1 if 'oferta' in request.POST.keys() else 0

            descripcion1 = validate_string('descripcion 1', request.POST['descripcion1'], remove_specials='yes', len_zero='yes')
            descripcion2 = validate_string('descripcion 2', request.POST['descripcion2'], remove_specials='yes', len_zero='yes')
            descripcion3 = validate_string('descripcion 3', request.POST['descripcion3'], remove_specials='yes', len_zero='yes')
            descripcion4 = validate_string('descripcion 4', request.POST['descripcion4'], remove_specials='yes', len_zero='yes')
            descripcion5 = validate_string('descripcion 5', request.POST['descripcion5'], remove_specials='yes', len_zero='yes')
            descripcion6 = validate_string('descripcion 6', request.POST['descripcion6'], remove_specials='yes', len_zero='yes')
            descripcion7 = validate_string('descripcion 7', request.POST['descripcion7'], remove_specials='yes', len_zero='yes')
            descripcion8 = validate_string('descripcion 8', request.POST['descripcion8'], remove_specials='yes', len_zero='yes')
            descripcion9 = validate_string('descripcion 9', request.POST['descripcion9'], remove_specials='yes', len_zero='yes')
            descripcion10 = validate_string('descripcion 10', request.POST['descripcion10'], remove_specials='yes', len_zero='yes')

            id = validate_number_int('id', request.POST['id'], len_zero='yes')
            #print('producto id...', id)

            if not self.is_in_db(id, producto_txt):

                # activo
                if activo == 1:
                    status_producto = self.status_activo
                else:
                    status_producto = self.status_inactivo

                # punto
                usuario = request.user
                user_perfil = UsersPerfiles.objects.get(user_id=usuario)
                linea = Lineas.objects.get(pk=linea_id)
                tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=tipo_montura_id)
                disenio_lentes = apps.get_model('configuraciones', 'DisenioLentes').objects.get(pk=disenio_lente_id)
                material = apps.get_model('configuraciones', 'Materiales').objects.get(pk=material_id)
                color = apps.get_model('configuraciones', 'Colores').objects.get(pk=color_id)
                marca = apps.get_model('configuraciones', 'Marcas').objects.get(pk=marca_id)
                proveedor = apps.get_model('configuraciones', 'Proveedores').objects.get(pk=proveedor_id)

                datos = {}
                datos['id'] = id
                datos['producto'] = producto_txt
                datos['codigo'] = codigo
                datos['precio'] = precio
                datos['precio_oferta'] = precio_oferta
                datos['linea_id'] = linea
                datos['stock_minimo'] = stock_minimo
                datos['tipo_montura_id'] = tipo_montura
                datos['disenio_lente_id'] = disenio_lentes
                datos['material_id'] = material
                datos['marca_id'] = marca
                datos['color_id'] = color
                datos['proveedor_id'] = proveedor

                datos['novedad'] = novedad
                datos['oferta'] = oferta
                datos['mas_vendido'] = mas_vendido

                datos['descripcion1'] = descripcion1
                datos['descripcion2'] = descripcion2
                datos['descripcion3'] = descripcion3
                datos['descripcion4'] = descripcion4
                datos['descripcion5'] = descripcion5
                datos['descripcion6'] = descripcion6
                datos['descripcion7'] = descripcion7
                datos['descripcion8'] = descripcion8
                datos['descripcion9'] = descripcion9
                datos['descripcion10'] = descripcion10

                datos['created_at'] = 'now'
                datos['updated_at'] = 'now'
                datos['user_perfil_id'] = user_perfil
                datos['status_id'] = status_producto
                #datos['punto_id'] = punto

                # datos relacionados
                datos_relacionados = []

                if 'lista_relacionado' in request.session.keys():
                    lista_relacionado = request.session['lista_relacionado']
                    for relacionado in lista_relacionado:
                        dato_producto = {}
                        dato_producto['producto_id'] = relacionado['producto_relacionado_id']
                        datos_relacionados.append(dato_producto)

                #print('datos relacionado:', datos_relacionados)
                datos['datos_relacionados'] = datos_relacionados

                if self.save_db(type, **datos):
                    self.error_operation = ""
                    return True
                else:
                    return False

            else:
                self.error_operation = "Ya existe este producto: " + producto_txt
                return False

        except Exception as ex:
            self.error_operation = "Error al agregar producto, " + str(ex)
            print('Error: ', str(ex))
            return False

    def save_db(self, type='add', **datos):
        """aniadimos a la base de datos"""
        try:

            if not self.is_in_db(datos['id'], datos['producto']):

                if type == 'add':

                    with transaction.atomic():
                        campos_add = {}
                        campos_add['producto'] = datos['producto']
                        campos_add['codigo'] = datos['codigo']
                        campos_add['precio'] = datos['precio']
                        campos_add['precio_oferta'] = datos['precio_oferta']
                        campos_add['linea_id'] = datos['linea_id']
                        campos_add['stock_minimo'] = datos['stock_minimo']

                        campos_add['tipo_montura_id'] = datos['tipo_montura_id']
                        campos_add['disenio_lente_id'] = datos['disenio_lente_id']
                        campos_add['material_id'] = datos['material_id']
                        campos_add['color_id'] = datos['color_id']
                        campos_add['marca_id'] = datos['marca_id']
                        campos_add['proveedor_id'] = datos['proveedor_id']

                        campos_add['novedad'] = datos['novedad']
                        campos_add['mas_vendido'] = datos['mas_vendido']
                        campos_add['oferta'] = datos['oferta']

                        campos_add['descripcion1'] = datos['descripcion1']
                        campos_add['descripcion2'] = datos['descripcion2']
                        campos_add['descripcion3'] = datos['descripcion3']
                        campos_add['descripcion4'] = datos['descripcion4']
                        campos_add['descripcion5'] = datos['descripcion5']
                        campos_add['descripcion6'] = datos['descripcion6']
                        campos_add['descripcion7'] = datos['descripcion7']
                        campos_add['descripcion8'] = datos['descripcion8']
                        campos_add['descripcion9'] = datos['descripcion9']
                        campos_add['descripcion10'] = datos['descripcion10']

                        campos_add['created_at'] = datos['created_at']
                        campos_add['updated_at'] = datos['updated_at']
                        campos_add['user_perfil_id'] = datos['user_perfil_id']
                        campos_add['status_id'] = datos['status_id']

                        producto_add = Productos.objects.create(**campos_add)
                        producto_add.save()

                        # borramos antes de insertar productos relacionados
                        productos_relacionados_lista = ProductosRelacionados.objects.filter(producto_id=producto_add)
                        productos_relacionados_lista.delete()

                        for producto in datos['datos_relacionados']:
                            producto_relacion = Productos.objects.get(pk=producto['producto_id'])
                            producto_relacionado = ProductosRelacionados.objects.create(producto_id=producto_add, producto_relacion_id=producto_relacion,
                                                                                        status_id=datos['status_id'], created_at='now', updated_at='now')
                            producto_relacionado.save()

                        self.error_operation = ''
                        return True

                if type == 'modify':
                    with transaction.atomic():
                        campos_update = {}
                        campos_update['producto'] = datos['producto']
                        campos_update['codigo'] = datos['codigo']
                        campos_update['precio'] = datos['precio']
                        campos_update['precio_oferta'] = datos['precio_oferta']
                        campos_update['linea_id'] = datos['linea_id']
                        campos_update['stock_minimo'] = datos['stock_minimo']

                        campos_update['tipo_montura_id'] = datos['tipo_montura_id']
                        campos_update['disenio_lente_id'] = datos['disenio_lente_id']
                        campos_update['material_id'] = datos['material_id']
                        campos_update['color_id'] = datos['color_id']
                        campos_update['marca_id'] = datos['marca_id']
                        campos_update['proveedor_id'] = datos['proveedor_id']

                        campos_update['novedad'] = datos['novedad']
                        campos_update['mas_vendido'] = datos['mas_vendido']
                        campos_update['oferta'] = datos['oferta']

                        campos_update['descripcion1'] = datos['descripcion1']
                        campos_update['descripcion2'] = datos['descripcion2']
                        campos_update['descripcion3'] = datos['descripcion3']
                        campos_update['descripcion4'] = datos['descripcion4']
                        campos_update['descripcion5'] = datos['descripcion5']
                        campos_update['descripcion6'] = datos['descripcion6']
                        campos_update['descripcion7'] = datos['descripcion7']
                        campos_update['descripcion8'] = datos['descripcion8']
                        campos_update['descripcion9'] = datos['descripcion9']
                        campos_update['descripcion10'] = datos['descripcion10']

                        campos_update['updated_at'] = datos['updated_at']
                        campos_update['status_id'] = datos['status_id']

                        producto_update = Productos.objects.filter(pk=datos['id'])
                        producto_update.update(**campos_update)

                        producto_actual = Productos.objects.get(pk=datos['id'])

                        # borramos antes de insertar productos relacionados
                        productos_relacionados_lista = ProductosRelacionados.objects.filter(producto_id=producto_actual)
                        productos_relacionados_lista.delete()

                        for producto in datos['datos_relacionados']:
                            producto_relacion = Productos.objects.get(pk=producto['producto_id'])
                            producto_relacionado = ProductosRelacionados.objects.create(producto_id=producto_actual, producto_relacion_id=producto_relacion,
                                                                                        status_id=datos['status_id'], created_at='now', updated_at='now')
                            producto_relacionado.save()

                        self.error_operation = ''
                        return True

                self.error_operation = 'operation no valid db'
                return False
            else:
                self.error_operation = "Ya existe este producto: " + datos['producto']
                return False

        except Exception as ex:
            self.error_operation = 'error de argumentos,' + str(ex)
            print('ERROR productos add, ' + str(ex))
            return False

    def buscar_producto(self, linea='', producto='', codigo='', operation='', pid=''):
        """busqueda de productos"""
        filtros = {}
        filtros['status_id__in'] = [self.activo]
        #filtros['es_combo'] = False

        if linea.strip() != '':
            filtros['linea_id__linea__icontains'] = linea
        if producto.strip() != '':
            filtros['producto__icontains'] = producto
        if codigo.strip() != '':
            filtros['codigo__icontains'] = codigo

        if operation == 'modify':
            productos_lista = Productos.objects.select_related('linea_id').filter(**filtros).exclude(pk=int(pid)).order_by('linea_id__linea', 'producto')[0:30]
        else:
            productos_lista = Productos.objects.select_related('linea_id').filter(**filtros).order_by('linea_id__linea', 'producto')[0:30]

        return productos_lista

    def save_images(self, request, producto_id):
        """guardamos las posiciones de las imagenes"""
        try:
            producto = Productos.objects.get(pk=producto_id)
            productos_imagenes = ProductosImagenes.objects.filter(producto_id=producto)

            for producto_imagen in productos_imagenes:
                aux = 'posicion_' + str(producto_imagen.producto_imagen_id)
                #print('aux: ', aux)
                if aux in request.POST.keys():
                    valor = 0 if request.POST[aux].strip() == '' else int(request.POST[aux].strip())
                    producto_imagen.posicion = valor
                    producto_imagen.save()

            return True

        except Exception as e:
            print('error guardar posicion imagen: ', str(e))
            self.error_operation = 'Error al guardar posiciones de imagen'
            return False

    def lista_productos(self, linea_id=0, punto_id=0):
        """lista de productos por linea seleccionada o todos"""
        datos_productos = []

        try:
            if linea_id == 0:
                sql_add = ''
            else:
                sql_add = f"AND l.linea_id='{linea_id}' "

            msql = f"SELECT l.linea, p.producto, p.codigo, p.precio, p.precio_oferta, p.producto_id "
            msql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.status_id='{self.activo}' AND p.status_id='{self.activo}' "
            msql += sql_add
            msql += f"ORDER BY l.linea, p.producto "
            #print('msql ', msql)

            with connection.cursor() as cursor:
                cursor.execute(msql)
                rows = cursor.fetchall()
                for row in rows:
                    datos_productos.append({'linea': row[0], 'producto': row[1], 'codigo': row[2], 'precio': row[3], 'precio_oferta': row[4],
                                            'producto_id': row[5]})

            return datos_productos

        except Exception as e:
            print('error lista productos: ', str(e))
            self.error_operation = 'Error al recuperar lista productos'
            return False

    def crear_descripcion(self, producto):
        texto_mostrar = ''

        des1 = producto.descripcion1.strip()
        des2 = producto.descripcion2.strip()
        des3 = producto.descripcion3.strip()
        des4 = producto.descripcion4.strip()
        des5 = producto.descripcion5.strip()
        des6 = producto.descripcion6.strip()
        des7 = producto.descripcion7.strip()
        des8 = producto.descripcion8.strip()
        des9 = producto.descripcion9.strip()
        des10 = producto.descripcion10.strip()

        texto1 = self.verificar_texto(des1)
        texto2 = self.verificar_texto(des2)
        texto3 = self.verificar_texto(des3)
        texto4 = self.verificar_texto(des4)
        texto5 = self.verificar_texto(des5)
        texto6 = self.verificar_texto(des6)
        texto7 = self.verificar_texto(des7)
        texto8 = self.verificar_texto(des8)
        texto9 = self.verificar_texto(des9)
        texto10 = self.verificar_texto(des10)

        texto_mostrar = texto1 + texto2 + texto3 + texto4 + texto5 + texto6 + texto7 + texto8 + texto9 + texto10

        return texto_mostrar

    def verificar_texto(self, descripcion):
        if descripcion == '':
            return ''
        else:
            return descripcion + '<br>'
