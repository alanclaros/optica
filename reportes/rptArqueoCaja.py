from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import pagesizes
#from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

from datetime import datetime

# imagen
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate  # BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# cabecera
from reportes.cabecera import cabecera

# modelos
from configuraciones.models import Cajas, Puntos, Sucursales, TiposMonedas, Monedas

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings, report_date
from utils.dates_functions import get_date_system, get_date_show

# clases
from controllers.reportes.ReportesController import ReportesController

import os


# tamanio de pagina
# vertical
#pagesize = pagesizes.portrait(pagesizes.letter)
# horizontal
pagesize = pagesizes.landscape(pagesizes.letter)

RPT_SUCURSAL_ID = 0
NOMBRE_CAJA = ''


def myFirstPage(canvas, doc):
    canvas.saveState()

    # canvas.setFont('Times-Bold', 16)
    # canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    # canvas.setFont('Times-Roman', 9)
    # canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)

    datosReporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    datosReporte['titulo'] = 'Arqueo de Caja: ' + NOMBRE_CAJA
    datosReporte['fecha_impresion'] = report_date()
    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    datosReporte['logo'] = dir_img

    cabecera(canvas, posY=206.5, **datosReporte)

    # canvas.setFont('Helvetica', 8)
    # canvas.drawString(15 * mm, 10 * mm, "footer todas las hojas %d" % (doc.page,))
    # canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "Created: %s" % datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))

    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()

    canvas.setFont('Times-Italic', 8)
    #canvas.drawString(15 * mm, 10 * mm, "footer todas las hojas %d" % (doc.page,))
    #canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "Created: %s" % datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))
    canvas.restoreState()


def rptArqueoCaja(buffer_pdf, caja_id, fecha):
    # pdf
    #pdf = canvas.Canvas(buffer, pagesize=letter)

    # datos de la caja
    caja_actual = Cajas.objects.select_related('punto_id').select_related('punto_id__sucursal_id').get(pk=caja_id)
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = caja_actual.punto_id.sucursal_id.sucursal_id
    global NOMBRE_CAJA
    NOMBRE_CAJA = caja_actual.punto_id.punto + '-' + caja_actual.caja

    doc = SimpleDocTemplate(buffer_pdf, pagesize=landscape(letter), leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    """datos del reporte"""
    reporte_controller = ReportesController()
    datos_reporte = reporte_controller.datos_arqueo_caja(caja_id=caja_id, fecha=fecha)

    # tabla
    data = []
    data.append(['Hora', 'Paciente', 'Montura', 'Material', 'DR.', 'Lab', 'Tec', 'Concepto', 'Monto'])
    filas = 0
    total = 0

    for dato in datos_reporte:
        total += dato['monto']
        hora = dato['fecha']
        paciente = Paragraph(dato['paciente'])
        montura = Paragraph(dato['montura'])
        material = Paragraph(dato['material'])
        doctor = Paragraph(dato['doctor'])
        laboratorio = Paragraph(dato['laboratorio'])
        tecnico = Paragraph(dato['tecnico'])
        concepto = Paragraph(dato['concepto'])

        datos = [hora, paciente, montura, material, doctor, laboratorio, tecnico, concepto, str(dato['monto'])]

        data.append(datos)
        filas += 1

    # aniadimos el total
    datos = ['', '', '', '', '', '', '', 'Total: ', str(total)]
    data.append(datos)
    align_right_start = 8
    align_right_end = 8
    cols_count = 8

    tabla_datos = Table(data, colWidths=[12*mm, 40*mm, 40*mm, 40*mm, 20*mm, 20*mm, 20*mm, 55*mm, 18*mm], repeatRows=1)
    tabla_datos.setStyle(TableStyle([('BACKGROUND', (0, 0), (cols_count, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                     ('ALIGN', (align_right_start, 0), (align_right_end, filas+1), 'RIGHT'),
                                     ('ALIGN', (align_right_end-1, filas+1), (align_right_end-1, filas+1), 'RIGHT'),
                                     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ('FONTSIZE', (0, 0), (cols_count, 0), 10),
                                     ('FONTSIZE', (0, 1), (-1, -1), 9),
                                     ('FONTNAME', (0, 0), (cols_count, 0), 'Helvetica'),
                                     ('FONTNAME', (0, 1), (cols_count, filas), 'Helvetica'),
                                     ('FONTNAME', (0, filas+1), (cols_count, filas+1), 'Helvetica-Bold'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 2),
                                     ('RIGHTPADDING', (0, 1), (-1, -1), 1),
                                     ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))

    #table = Table(tdata, colWidths=colwidths, repeatRows=2)
    # table.setStyle(TableStyle(tstyledata))

    Story = []
    Story.append(Spacer(100*mm, 22*mm))
    Story.append(tabla_datos)

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
