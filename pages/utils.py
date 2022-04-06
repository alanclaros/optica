from django.apps import apps
from utils.permissions import get_system_settings
# cursor
from django.db import connection


def reemplazar_codigo_html(cadena):
    retorno = cadena
    retorno = retorno.replace('&', "&#38;")
    retorno = retorno.replace('#', "&#35;")

    retorno = retorno.replace("'", "&#39;")
    retorno = retorno.replace('"', "&#34;")
    retorno = retorno.replace('á', "&#225;")
    retorno = retorno.replace('é', "&#233;")
    retorno = retorno.replace('í', "&#237;")
    retorno = retorno.replace('ó', "&#243;")
    retorno = retorno.replace('ú', "&#250;")
    retorno = retorno.replace('Á', "&#193;")
    retorno = retorno.replace('É', "&#201;")
    retorno = retorno.replace('Í', "&#205;")
    retorno = retorno.replace('Ó', "&#211;")
    retorno = retorno.replace('Ú', "&#218;")
    retorno = retorno.replace('!', "&#33;")

    retorno = retorno.replace('$', "&#36;")
    retorno = retorno.replace('%', "&#37;")
    retorno = retorno.replace('*', "&#42;")
    retorno = retorno.replace('+', "&#43;")
    retorno = retorno.replace('-', "&#45;")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")
    retorno = retorno.replace('', "")

    return retorno


def get_lista_session(session_var):
    lista_select = []
    if len(session_var) > 0:
        div_lista = session_var.split(',')
        for dato in div_lista:
            lista_select.append(dato.strip())

    return lista_select


def get_lista_cuadros(col_name, lista_session, lista_select, borde_nomal, borde_resaltado):

    # listado
    listado = []
    if len(lista_session) > 0:
        for ax_d in lista_session:
            dato = {}
            dato[col_name] = ax_d
            existe = 0
            for lcs in lista_select:
                if str(lcs) == str(ax_d):
                    existe = 1

            if existe == 0:
                dato['borde'] = borde_nomal
            else:
                dato['borde'] = borde_resaltado

            listado.append(dato)

    return listado


def link_linea(linea_id):
    try:
        linea = apps.get_model('configuraciones', 'Lineas').objects.get(pk=int(linea_id))
        retorno = ''
        if linea.linea_principal == 1:
            retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'

        else:
            # linea principal antes
            linea_sup1 = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea.linea_superior_id)

            if linea_sup1.linea_principal == 1:
                retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup1.linea_id) + "'" + ');">' + linea_sup1.linea + '</span>'
                retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'
            else:
                # otra linea superior antes
                linea_sup2 = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea_sup1.linea_superior_id)

                if linea_sup2.linea_principal == 1:
                    retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup2.linea_id) + "'" + ');">' + linea_sup2.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup1.linea_id) + "'" + ');">' + linea_sup1.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'
                else:
                    linea_sup3 = apps.get_model('configuraciones', 'Lineas').objects.get(pk=linea_sup2.linea_superior_id)
                    retorno = ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup3.linea_id) + "'" + ');">' + linea_sup3.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup2.linea_id) + "'" + ');">' + linea_sup2.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea_sup1.linea_id) + "'" + ');">' + linea_sup1.linea + '</span>'
                    retorno += ' / <span class="link_lineas pointer" onclick="escogerLinea(' + "'" + str(linea.linea_id) + "'" + ');">' + linea.linea + '</span>'

        return retorno

    except Exception as ex:
        retorno = ''
        return retorno


def lista_productos(request, linea_id=0, producto_nombre='', novedad='0', mas_vendido='0', oferta='0', tipo_montura='', material=''):
    #print('color...', color)
    producto = reemplazar_codigo_html(producto_nombre.strip())

    """lista de productos segun linea o ubicacion"""
    settings_sistema = get_system_settings()
    cant_per_page = settings_sistema['cant_productos_home']

    # verificamos si escribo busqueda o selecciono combo
    sql_add = "AND p.status_id='1' AND l.status_id='1' "

    if len(tipo_montura) > 0:
        div_tipo = tipo_montura.split(',')
        sql_add += f"AND ("
        for dato in div_tipo:
            sql_add += f"p.tipo_montura_id LIKE '%{dato}%' OR "
        sql_add = sql_add[0:len(sql_add)-4] + ') '

    if len(material) > 0:
        div_material = material.split(',')
        sql_add += f"AND ("
        for dato in div_material:
            sql_add += f"p.material_id LIKE '%{dato}%' OR "
        sql_add = sql_add[0:len(sql_add)-4] + ') '

    if oferta == '1' or novedad == '1' or mas_vendido == '1':
        sql_add += "AND ("

        if oferta == '1':
            sql_add += "p.oferta='1' OR "

        if novedad == '1':
            sql_add += "p.novedad='1' OR "

        if mas_vendido == '1':
            sql_add += "p.mas_vendido='1' OR "

        # quitamos el ultimo OR
        sql_add = sql_add[0:len(sql_add)-4] + ') '

    # linea
    # if linea_id != 0:
    #     sql_add = f"AND l.linea_id='{linea_id}' "
        #sql_add_filtro += f"AND l.linea_id='{linea_id}' "

    if producto != '':
        division = producto.split(' ')
        if len(division) == 1:
            sql_add += f"AND p.producto LIKE '%{producto}%' "

        elif len(division) == 2:
            sql_add += f"AND (p.producto LIKE '%{division[0]}%{division[1]}%' OR p.producto LIKE '%{division[1]}%{division[0]}%' "
            sql_add += ') '

        # if len(division) == 3:
        elif len(division) == 3:
            sql_add += f"AND (p.producto LIKE '%{division[0]}%{division[1]}%{division[2]}%' "
            sql_add += f"OR p.producto LIKE '%{division[0]}%{division[2]}%{division[1]}%' "

            sql_add += f"OR p.producto LIKE '%{division[1]}%{division[0]}%{division[2]}%' "
            sql_add += f"OR p.producto LIKE '%{division[1]}%{division[2]}%{division[0]}%' "

            sql_add += f"OR p.producto LIKE '%{division[2]}%{division[0]}%{division[1]}%' "
            sql_add += f"OR p.producto LIKE '%{division[2]}%{division[1]}%{division[0]}%' "

            sql_add += ') '
        else:
            nuevo_p = '%'
            for i in range(len(division)):
                nuevo_p += division[i] + '%'

            sql_add += f"AND p.producto LIKE '{nuevo_p}' "

    if not 'productosinicio' in request.session.keys():
        request.session['productosinicio'] = {}
        request.session['productosinicio']['producto'] = ''
        request.session['productosinicio']['linea'] = 0

        request.session['productosinicio']['tipos_montura_select'] = ''
        request.session['productosinicio']['materiales_select'] = ''
        request.session['productosinicio']['oferta'] = '0'
        request.session['productosinicio']['mas_vendido'] = '0'
        request.session['productosinicio']['novedad'] = '0'
        # pagina
        request.session['productosinicio']['pagina'] = 1
        request.session['productosinicio']['pages_list'] = []

        request.session.modified = True

    pages_limit_bottom = (int(request.session['productosinicio']['pagina']) - 1) * cant_per_page
    pages_limit_top = cant_per_page

    # listado de productos
    lista_pp = []
    cant_total = 0

    # listados generales de color, marca, etc producto o linea
    # sin contar los otros filtros, para que el usuario pueda filtrar solo de este grupo
    listado_tipos_montura = []
    listado_materiales = []

    # listado por defecto
    status_activo = apps.get_model('status', 'Status').objects.get(pk=1)
    tipos_montura_db = apps.get_model('configuraciones', 'TiposMontura').objects.filter(status_id=status_activo).order_by('tipo_montura')
    materiales_db = apps.get_model('configuraciones', 'Materiales').objects.filter(status_id=status_activo).order_by('material')

    # busqueda por de texto de productos
    if linea_id == 0:
        sql = "SELECT l.linea, p.producto, p.codigo, p.precio, p.precio_oferta, p.producto_id, l.linea_id, "
        sql += "p.tipo_montura_id, p.material_id, p.novedad, p.mas_vendido, p.oferta "
        sql += "FROM productos p, lineas l WHERE p.linea_id=l.linea_id " + sql_add
        sql += "ORDER BY l.linea, p.producto "
        #print('sql: ', sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                cant_total = cant_total + 1
                # imagen del producto
                sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row[5]}' ORDER BY posicion LIMIT 0,1 "
                imagen = ''
                imagen_thumb = ''
                with connection.cursor() as cursor2:
                    cursor2.execute(sql_imagen)
                    row_imagen = cursor2.fetchone()
                    if row_imagen:
                        imagen = row_imagen[0]
                        imagen_thumb = row_imagen[1]

                # para el listado de monturas
                listado_tipos_montura = set_lista_monturas(row[7], listado_tipos_montura, tipos_montura_db)

                # para el listado de materiales
                listado_materiales = set_lista_materiales(row[8], listado_materiales, materiales_db)

                dato_producto = {}
                dato_producto['linea'] = row[0]
                dato_producto['producto'] = reemplazar_codigo_html(row[1])
                dato_producto['codigo'] = row[2]
                dato_producto['precio'] = row[3]
                dato_producto['precio_oferta'] = row[4]
                dato_producto['imagen'] = imagen
                dato_producto['imagen_thumb'] = imagen_thumb
                dato_producto['producto_id'] = row[5]

                dato_producto['tipo_montura_id'] = row[7]
                dato_producto['material_id'] = row[8]
                dato_producto['novedad'] = row[9]
                dato_producto['mas_vendido'] = row[10]
                dato_producto['oferta'] = row[11]

                lista_pp.append(dato_producto)

    # busqueda por seleccion de linea
    # busqueda por seleccion de linea
    if linea_id != 0:
        # entramos un nivel
        sql = "SELECT l.linea, p.producto, p.codigo, p.precio, p.precio_oferta, p.producto_id, l.linea_id, "
        sql += "p.tipo_montura_id, p.material_id, p.novedad, p.mas_vendido, p.oferta "
        sql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{linea_id}' "
        sql += sql_add
        sql += "ORDER BY l.linea, p.producto "
        print('sql: ', sql)

        with connection.cursor() as cursor22:
            cursor22.execute(sql)
            rows2 = cursor22.fetchall()

            for row2 in rows2:
                cant_total = cant_total + 1
                # imagen del producto
                sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row2[5]}' ORDER BY posicion LIMIT 0,1 "
                imagen = ''
                imagen_thumb = ''
                with connection.cursor() as cursor33:
                    cursor33.execute(sql_imagen)
                    row_imagen3 = cursor33.fetchone()
                    if row_imagen3:
                        imagen = row_imagen3[0]
                        imagen_thumb = row_imagen3[1]

                # para el listado de monturas
                listado_tipos_montura = set_lista_monturas(row2[7], listado_tipos_montura, tipos_montura_db)
                # para el listado de materiales
                listado_materiales = set_lista_materiales(row2[8], listado_materiales, materiales_db)

                dato_producto = {}
                dato_producto['linea'] = row2[0]
                dato_producto['producto'] = reemplazar_codigo_html(row2[1])
                dato_producto['codigo'] = row2[2]
                dato_producto['precio'] = row2[3]
                dato_producto['precio_oferta'] = row2[4]
                dato_producto['imagen'] = imagen
                dato_producto['imagen_thumb'] = imagen_thumb
                dato_producto['producto_id'] = row2[5]

                dato_producto['tipo_montura_id'] = row2[7]
                dato_producto['material_id'] = row2[8]
                dato_producto['novedad'] = row2[9]
                dato_producto['mas_vendido'] = row2[10]
                dato_producto['oferta'] = row2[11]

                lista_pp.append(dato_producto)

        # lineas inferior segundo nivel
        sql = f"SELECT linea_id FROM lineas WHERE linea_superior_id='{linea_id}' "
        with connection.cursor() as cursor10:
            cursor10.execute(sql)
            rows10 = cursor10.fetchall()
            for row10 in rows10:
                # segundo nivel
                sql = "SELECT l.linea, p.producto, p.codigo, p.precio, p.precio_oferta, p.producto_id, l.linea_id, "
                sql += "p.tipo_montura_id, p.material_id, p.novedad, p.mas_vendido, p.oferta "
                sql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{row10[0]}' "
                sql += sql_add
                sql += "ORDER BY l.linea, p.producto "
                #print('sql2: ', sql)
                with connection.cursor() as cursor44:
                    cursor44.execute(sql)
                    rows4 = cursor44.fetchall()
                    for row4 in rows4:
                        cant_total = cant_total + 1

                        # imagen del producto
                        sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row4[5]}' ORDER BY posicion LIMIT 0,1 "
                        imagen = ''
                        imagen_thumb = ''
                        with connection.cursor() as cursor55:
                            cursor55.execute(sql_imagen)
                            row_imagen5 = cursor55.fetchone()
                            if row_imagen5:
                                imagen = row_imagen5[0]
                                imagen_thumb = row_imagen5[1]

                        # para el listado de monturas
                        listado_tipos_montura = set_lista_monturas(row4[7], listado_tipos_montura, tipos_montura_db)
                        # para el listado de materiales
                        listado_materiales = set_lista_materiales(row4[8], listado_materiales, materiales_db)

                        dato_producto = {}
                        dato_producto['linea'] = row4[0]
                        dato_producto['producto'] = reemplazar_codigo_html(row4[1])
                        dato_producto['codigo'] = row4[2]
                        dato_producto['precio'] = row4[3]
                        dato_producto['precio_oferta'] = row4[4]
                        dato_producto['imagen'] = imagen
                        dato_producto['imagen_thumb'] = imagen_thumb
                        dato_producto['producto_id'] = row4[5]

                        dato_producto['tipo_montura_id'] = row4[7]
                        dato_producto['material_id'] = row4[8]
                        dato_producto['novedad'] = row4[9]
                        dato_producto['mas_vendido'] = row4[10]
                        dato_producto['oferta'] = row4[11]

                        lista_pp.append(dato_producto)

                # tercer nivel
                sql = f"SELECT linea_id FROM lineas WHERE linea_superior_id='{row10[0]}' "
                with connection.cursor() as cursor20:
                    cursor20.execute(sql)
                    rows20 = cursor20.fetchall()
                    for row20 in rows20:
                        # tercer nivel
                        sql = "SELECT l.linea, p.producto, p.codigo, p.precio, p.precio_oferta, p.producto_id, l.linea_id, "
                        sql += "p.tipo_montura_id, p.material_id, p.novedad, p.mas_vendido, p.oferta "
                        sql += f"FROM productos p, lineas l WHERE p.linea_id=l.linea_id AND l.linea_id='{row20[0]}' "
                        sql += sql_add
                        sql += "ORDER BY l.linea, p.producto "
                        #print('sql 3: ', sql)
                        with connection.cursor() as cursor66:
                            cursor66.execute(sql)
                            rows6 = cursor66.fetchall()
                            for row6 in rows6:
                                cant_total = cant_total + 1

                                # imagen del producto
                                sql_imagen = f"SELECT imagen, imagen_thumb FROM productos_imagenes WHERE producto_id='{row6[5]}' ORDER BY posicion LIMIT 0,1 "
                                imagen = ''
                                imagen_thumb = ''
                                with connection.cursor() as cursor77:
                                    cursor77.execute(sql_imagen)
                                    row_imagen7 = cursor77.fetchone()
                                    if row_imagen7:
                                        imagen = row_imagen7[0]
                                        imagen_thumb = row_imagen7[1]

                                # para el listado de monturas
                                listado_tipos_montura = set_lista_monturas(row6[7], listado_tipos_montura, tipos_montura_db)
                                # para el listado de materiales
                                listado_materiales = set_lista_materiales(row6[8], listado_materiales, materiales_db)

                                dato_producto = {}
                                dato_producto['linea'] = row6[0]
                                dato_producto['producto'] = reemplazar_codigo_html(row6[1])
                                dato_producto['codigo'] = row6[2]
                                dato_producto['precio'] = row6[3]
                                dato_producto['precio_oferta'] = row6[4]
                                dato_producto['imagen'] = imagen
                                dato_producto['imagen_thumb'] = imagen_thumb
                                dato_producto['producto_id'] = row6[5]

                                dato_producto['tipo_montura_id'] = row6[7]
                                dato_producto['material_id'] = row6[8]
                                dato_producto['novedad'] = row6[9]
                                dato_producto['mas_vendido'] = row6[10]
                                dato_producto['oferta'] = row6[11]

                                lista_pp.append(dato_producto)

    # listados generales
    # print('listado_colores: ', listado_colores)
    # print('listado_marcas: ', listado_marcas)
    # print('listado_tallas: ', listado_tallas)

    # paginacion
    #print('cant total: ', cant_total)
    j = 1
    i = 0
    pages_list = []
    while i < cant_total:
        pages_list.append(j)
        i = i + cant_per_page
        j += 1
        if j > 15:
            break

    request.session['productosinicio']['pages_list'] = pages_list
    request.session.modified = True

    # listado de retorno
    listado = []
    cant_fila = 3
    cant_actual = 0
    lista_fila = []
    contador = 0

    #print('lista prodd: ', lista_pp)
    #print('limit bottom: ', pages_limit_bottom, ' limit top: ', pages_limit_top)
    for producto_p in lista_pp:
        if contador >= pages_limit_bottom and contador < (pages_limit_bottom+pages_limit_top):
            if cant_actual < cant_fila:
                lista_fila.append(producto_p)

            # aumentamos la columna
            cant_actual += 1

            if cant_actual == cant_fila:
                listado.append(lista_fila)
                cant_actual = 0
                lista_fila = []

        contador += 1

    # registramos la session
    #print('listado tipos montura: ', listado_tipos_montura)
    #print('listado materiales: ', listado_materiales)
    request.session['productosinicio']['lista_tipos_montura'] = listado_tipos_montura
    request.session['productosinicio']['lista_materiales'] = listado_materiales
    request.session.modified = True

    # termina los productos
    if cant_actual > 0:
        # no termino de llenarse los datos de la fila
        for i in range(cant_actual, cant_fila):
            dato_producto = {}
            dato_producto['linea'] = ''
            dato_producto['producto'] = ''
            dato_producto['codigo'] = ''
            dato_producto['precio'] = ''
            dato_producto['precio_oferta'] = 0
            dato_producto['producto_id'] = 0
            lista_fila.append(dato_producto)

        # aniadimos a la lista principal
        listado.append(lista_fila)

    # devolvemos los productos
    #print('listado...: ', listado)
    return listado


def set_lista_monturas(columna_db, lista, datos_db):
    # para el listado de monturas
    if columna_db and columna_db != '':
        div_aux = columna_db.split(',')
        for dato in div_aux:
            bande = 0
            for tipo_montura in lista:
                if tipo_montura['tipo_montura_id'] == dato:
                    bande = 1
                    break
            if bande == 0:
                dato_obj = {}
                dato_obj['tipo_montura_id'] = dato
                nombre_montura = ''
                for tm_db in datos_db:
                    if '|' + str(tm_db.tipo_montura_id) + '|' == dato:
                        nombre_montura = tm_db.tipo_montura
                        break
                dato_obj['tipo_montura'] = nombre_montura
                # aniadimos
                lista.append(dato_obj)

    ordenado = sorted(lista, key=lambda tipo_montura: tipo_montura['tipo_montura'])
    return ordenado


def set_lista_materiales(columna_db, lista, datos_db):
    # para el listado de materiales
    if columna_db and columna_db != '':
        div_aux = columna_db.split(',')
        for dato in div_aux:
            bande = 0
            for material in lista:
                if material['material_id'] == dato:
                    bande = 1
                    break
            if bande == 0:
                dato_obj = {}
                dato_obj['material_id'] = dato
                nombre_material = ''
                for material_db in datos_db:
                    if '|' + str(material_db.material_id) + '|' == dato:
                        nombre_material = material_db.material
                        break
                dato_obj['material'] = nombre_material
                # aniadimos
                lista.append(dato_obj)

    ordenado = sorted(lista, key=lambda material: material['material'])
    return ordenado
