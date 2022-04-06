from urllib import request
from django.apps.registry import apps
from reportlab.lib.pagesizes import letter
from reportlab.lib import pagesizes
#from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# imagen
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# cabecera
from reportes.cabecera import cabecera

# modelos
from configuraciones.models import Puntos
from permisos.models import UsersPerfiles

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings, report_date

# clases
from controllers.reportes.ReportesController import ReportesController

import os

# tamanio de pagina
pagesize = pagesizes.portrait(pagesizes.letter)
RPT_SUCURSAL_ID = 0
DATO_CAJA = ''


def myFirstPage(canvas, doc):
    canvas.saveState()

    datosReporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    datosReporte['titulo'] = 'Stock de Productos ' + DATO_CAJA
    datosReporte['fecha_impresion'] = report_date()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datosReporte['logo'] = dir_img

    cabecera(canvas, **datosReporte)

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))

    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))
    canvas.restoreState()


def rptStockProductos(buffer_pdf, usuario, tipo_montura_id, almacen_id, vendidas, sin_vender):
    # pdf
    #pdf = canvas.Canvas(buffer, pagesize=letter)

    # datos sucursal
    user_perfil = UsersPerfiles.objects.get(user_id=usuario)
    #permisos = get_permisos_usuario(usuario, settings.MOD_REPORTES)
    punto = Puntos.objects.get(pk=user_perfil.punto_id)
    sucursal_id_user = punto.sucursal_id.sucursal_id
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = sucursal_id_user

    styles = getSampleStyleSheet()
    # personalizamos
    style_almacen = ParagraphStyle('almacen',
                                   fontName="Helvetica-Bold",
                                   fontSize=12,
                                   parent=styles['Normal'],
                                   alignment=1,
                                   spaceAfter=10)

    doc = SimpleDocTemplate(buffer_pdf, pagesize=letter, leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    """datos del reporte"""
    #reporte_controller = ReportesController()
    #datos_reporte = reporte_controller.datos_stock_productos(usuario, linea_id=linea_id, almacen_id=almacen_id)
    reporte_controller = ReportesController()
    datos_stock = reporte_controller.datos_stock_productos(usuario, tipo_montura_id, almacen_id, vendidas, sin_vender)

    Story = []
    Story.append(Spacer(100*mm, 22*mm))

    almacen_actual = ''
    datos_tabla = []
    data = []
    filas = 0
    bande = 0

    #data.append(['Tipo Montura', 'Nombre Montura', 'Cantidad'])
    for dato in datos_stock:
        if almacen_actual != dato['almacen']:
            bande += 1
            # primera vuelta, no se cierra tabla
            if bande > 1:
                # cerramos tabla anterior y aniadimos
                if len(data) > 0:
                    #datos_tabla = ['', '', '', 'Totales: ', str(subtotal), str(descuento), str(total), str(en_ingresos)]
                    data.append(datos_tabla)

                    # ancho columnas
                    tabla_datos = Table(data, colWidths=[60*mm, 80*mm, 20*mm], repeatRows=1)
                    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (2, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                                     ('ALIGN', (2, 0), (2, filas), 'RIGHT'),
                                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                                     ('FONTSIZE', (0, 0), (2, 0), 10),
                                                     ('FONTSIZE', (0, 1), (-1, -1), 9),
                                                     ('FONTNAME', (0, 0), (2, 0), 'Helvetica'),
                                                     ('FONTNAME', (0, 1), (2, filas), 'Helvetica'),
                                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
                    # aniadimos la tabla
                    Story.append(Paragraph(almacen_actual, style_almacen))
                    Story.append(tabla_datos)
                    Story.append(Spacer(100*mm, 5*mm))

            # texto nombre de la caja
            #Story.append(Paragraph(dato['punto'] + ' - ' + dato['caja'], style_punto))
            almacen_actual = dato['almacen']

            # creamos tabla para esta caja
            data = []

            data.append(['Tipo Montura', 'Nombre Montura', 'Cantidad'])
            filas = 0

        # seguimos llenando de datos la tabla hasta cambiar de caja, sucursal o ciudad
        tipo_montura = Paragraph(dato['tipo_montura'])
        nombre_montura = Paragraph(dato['nombre_montura'])

        datos_tabla = [tipo_montura, nombre_montura, str(dato['cantidad'])]
        data.append(datos_tabla)
        filas += 1

    # datos de la ultima tabla
    if len(data) > 0:
        tabla_datos = Table(data, colWidths=[60*mm, 80*mm, 20*mm], repeatRows=1)
        tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (2, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                         ('ALIGN', (2, 0), (2, filas), 'RIGHT'),
                                         ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                         ('FONTSIZE', (0, 0), (2, 0), 10),
                                         ('FONTSIZE', (0, 1), (-1, -1), 9),
                                         ('FONTNAME', (0, 0), (2, 0), 'Helvetica'),
                                         ('FONTNAME', (0, 1), (2, filas), 'Helvetica'),
                                         ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                         ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                         ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                         ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
        # aniadimos la tabla
        Story.append(Paragraph(almacen_actual, style_almacen))
        Story.append(tabla_datos)

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
