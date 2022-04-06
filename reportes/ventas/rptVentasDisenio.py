#from posixpath import split
#from turtle import width
from django.apps.registry import apps
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import pagesizes
# from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

from datetime import datetime

from reportlab.pdfbase.pdfmetrics import stringWidth

# imagen
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# cabecera
from reportes.cabecera import cabecera

# modelos
from ventas.models import Ventas, VentasDetalles

# settings
from django.conf import settings

# utils
from utils.permissions import get_sucursal_settings, report_date
from utils.dates_functions import get_date_show

from reportlab.platypus import PageBreak

import os
import copy

# tamanio de pagina
pagesize = pagesizes.portrait(pagesizes.letter)
# pagesize = pagesizes.landscape(pagesizes.letter)
RPT_SUCURSAL_ID = 0
DATO_REGISTRO = ''
RPT_CONTRATO = '#'
RPT_ESTADO = 'preventa'
RPT_ANULADO = ''

# aumento para la direccion y la observacion
AUMENTO_Y = 0


def myFirstPage(canvas, doc):
    canvas.saveState()

    # datosReporte = get_sucursal_settings(RPT_SUCURSAL_ID)
    # datosReporte['titulo'] = 'Venta, ' + DATO_REGISTRO
    # datosReporte['fecha_impresion'] = report_date()
    # dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    # datosReporte['logo'] = dir_img

    # # para horizontal
    # # posicionY = 207
    # # cabecera(canvas, posY=posicionY, **datosReporte)

    # # vertical
    # cabecera(canvas=canvas, **datosReporte)

    # cabecera
    posY = 244
    altoTxt = 6
    posX = 30
    posX2 = 160
    posX3 = 160

    venta = Ventas.objects.get(pk=int(DATO_REGISTRO))
    venta_detalles = VentasDetalles.objects.filter(venta_id=venta)

    dir_img = os.path.join(settings.STATIC_ROOT, 'img/logo.png')
    dir_img2 = os.path.join(settings.STATIC_ROOT, 'img/cabecera_reporte.jpg')
    dir_img_facebook = os.path.join(settings.STATIC_ROOT, 'img/facebook_30x30.jpg')
    dir_img_whatsapp = os.path.join(settings.STATIC_ROOT, 'img/whatsapp_50x50.jpg')
    canvas.drawImage(dir_img, 15*mm, (posY+18)*mm, width=77, height=35)
    canvas.drawImage(dir_img2, 5*mm, (posY+5)*mm, width=136, height=35)
    canvas.drawImage(dir_img_whatsapp, 132*mm, (posY+16)*mm, width=12, height=12)
    canvas.drawImage(dir_img_facebook, 95*mm, (posY+10.5)*mm, width=12, height=12)

    # estado de la venta
    estado_venta = 'PREVENTA'
    if venta.status_id.status_id == settings.STATUS_VENTA:
        estado_venta = 'VENTA'
    if venta.status_id.status_id == settings.STATUS_FINALIZADO:
        estado_venta = 'FINALIZADO'
    if venta.status_id.status_id == settings.STATUS_ANULADO:
        estado_venta = 'ANULADO'

    # datos optica
    posx_datos = 80
    posy_datos = 270
    canvas.setFont("Helvetica", 10)
    canvas.setFillColorRGB(51/255, 51/255, 51/255)
    canvas.drawString(posx_datos*mm, posy_datos*mm, 'Av. San Martín Nº 147 entre Heroinas')
    canvas.drawString((posx_datos+5)*mm, (posy_datos-5)*mm, 'y Colombia Edif. Principito P/B')
    canvas.drawString((posx_datos+4)*mm, (posy_datos-10)*mm, 'Telf.: ')
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString((posx_datos+12.5)*mm, (posy_datos-10)*mm, '4331765')
    canvas.setFont("Helvetica", 10)
    canvas.drawString((posx_datos+27)*mm, (posy_datos-10)*mm, 'Cel.: ')
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString((posx_datos+35)*mm, (posy_datos-10)*mm, '70791680')
    canvas.setFont("Helvetica", 10)
    canvas.drawString((posx_datos+20)*mm, (posy_datos-15)*mm, 'Optica Ideal')

    canvas.setFont("Helvetica", 10)
    # colores cabecera tabla
    canvas.setStrokeColorRGB(13/255, 166/255, 171/255)
    canvas.setFillColorRGB(13/255, 166/255, 171/255)

    # fecha con lineas
    canvas.roundRect(174*mm, 258*mm, 35*mm, 15*mm, 6, stroke=1, fill=0)
    # cabecera
    canvas.roundRect(174*mm, 266*mm, 35*mm, 8*mm, 6, stroke=1, fill=1)
    canvas.rect(174*mm, 266*mm, 35*mm, 2*mm, fill=1)
    # lineas
    canvas.line(184*mm, 258*mm, 184*mm, 270*mm)
    canvas.line(196*mm, 258*mm, 196*mm, 270*mm)

    # nombre
    posy_nombre = 234
    canvas.roundRect(4*mm, posy_nombre*mm, 130*mm, 12*mm, 6, stroke=1, fill=0)
    canvas.roundRect(4*mm, (posy_nombre+12-6)*mm, 130*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(4*mm, (posy_nombre+12-6)*mm, 130*mm, 2*mm, fill=1)

    # material empleado
    posy_material = 214
    ancho_material = 80
    canvas.roundRect(4*mm, posy_material*mm, ancho_material*mm, 18*mm, 6, stroke=1, fill=0)
    canvas.roundRect(4*mm, (posy_material+18-6)*mm, ancho_material*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(4*mm, (posy_material+18-6)*mm, ancho_material*mm, 2*mm, fill=1)

    # fecha entrega
    posy_fecha_entrega = 214
    ancho_fecha_entrega = 48
    canvas.roundRect(86*mm, posy_fecha_entrega*mm, ancho_fecha_entrega*mm, 18*mm, 6, stroke=1, fill=0)
    canvas.roundRect(86*mm, (posy_fecha_entrega+18-6)*mm, ancho_fecha_entrega*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(86*mm, (posy_fecha_entrega+18-6-6)*mm, ancho_fecha_entrega*mm, 8*mm, fill=1)
    # lineas fecha entrega
    canvas.line(96*mm, posy_fecha_entrega*mm, 96*mm, (posy_fecha_entrega+10)*mm)
    canvas.line(106*mm, posy_fecha_entrega*mm, 106*mm, (posy_fecha_entrega+10)*mm)
    canvas.line(118*mm, posy_fecha_entrega*mm, 118*mm, (posy_fecha_entrega+10)*mm)

    # tipo de montura
    posy_tipo_montura = 214
    ancho_tipo_montura = 74
    canvas.roundRect(136*mm, posy_tipo_montura*mm, ancho_tipo_montura*mm, 18*mm, 6, stroke=1, fill=0)
    canvas.roundRect(136*mm, (posy_tipo_montura+18-6)*mm, ancho_tipo_montura*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(136*mm, (posy_tipo_montura+18-6)*mm, ancho_tipo_montura*mm, 2*mm, fill=1)

    # cuadro total
    posy_cuadro_total = 235
    ancho_cuadro_total = 50
    posx_cuadro_total = 159
    #canvas.setStrokeColorRGB(13/255, 166/255, 171/255)
    canvas.setFillColorRGB(240/255, 240/255, 240/255)
    canvas.roundRect(posx_cuadro_total*mm, posy_cuadro_total*mm, ancho_cuadro_total*mm, 18*mm, 6, stroke=1, fill=1)
    #canvas.roundRect(posx_cuadro_total*mm, (posy_cuadro_total+18-6)*mm, ancho_cuadro_total*mm, 6*mm, 6, stroke=1, fill=1)
    #canvas.rect(posx_cuadro_total*mm, (posy_cuadro_total+18-6)*mm, ancho_cuadro_total*mm, 2*mm, fill=1)

    # cabecera fecha
    canvas.setFillColorRGB(255/255, 255/255, 255/255)
    canvas.drawString(176*mm, 268*mm, 'DIA')
    canvas.drawString(186*mm, 268*mm, 'MES')
    canvas.drawString(198*mm, 268*mm, 'AÑO')
    # nombre
    canvas.drawString(58*mm, (posy_nombre+8)*mm, 'NOMBRE')
    # material empleado
    canvas.drawString(23*mm, (posy_material+14)*mm, 'MATERIAL EMPLEADO')
    # fecha entrega
    canvas.drawString(95*mm, (posy_fecha_entrega+14)*mm, 'Fecha de Entrega')
    canvas.drawString(87*mm, (posy_fecha_entrega+8)*mm, 'DIA')
    canvas.drawString(97*mm, (posy_fecha_entrega+8)*mm, 'MES')
    canvas.drawString(108*mm, (posy_fecha_entrega+8)*mm, 'AÑO')
    canvas.drawString(122*mm, (posy_fecha_entrega+8)*mm, 'HRS')
    # tipo de montura
    canvas.drawString(158*mm, (posy_fecha_entrega+14)*mm, 'Tipo de Montura')

    # datos fecha
    fecha_preventa = get_date_show(venta.fecha_preventa, formato_ori='yyyy-mm-dd HH:ii:ss', formato='dd-MMM-yyyy')
    aux_div = fecha_preventa.split('-')
    p_dia = aux_div[0]
    p_mes = aux_div[1]
    p_anio = aux_div[2]

    canvas.setStrokeColorRGB(51/255, 51/255, 51/255)
    canvas.setFillColorRGB(51/255, 51/255, 51/255)
    canvas.drawString(177*mm, 260*mm, p_dia)
    canvas.drawString(187*mm, 260*mm, p_mes)
    canvas.drawString(198*mm, 260*mm, p_anio)
    # nombre
    canvas.drawString(18*mm, (posy_nombre+1.5)*mm, venta.nombres + ' ' + venta.apellidos + ', ' + venta.telefonos)

    # cuadro total
    p_total = set_puntos_string("Total", str(venta.total) + " Bs.", 20)
    p_a_cuenta = set_puntos_string("A cuenta", str(venta.a_cuenta) + " Bs.", 20)
    p_saldo = set_puntos_string("Saldo", str(venta.saldo) + " Bs.", 20)
    canvas.setFont("Courier", 10)
    canvas.drawRightString((posx_cuadro_total+ancho_cuadro_total-2)*mm, (posy_cuadro_total+13)*mm, p_total)
    canvas.drawRightString((posx_cuadro_total+ancho_cuadro_total-2)*mm, (posy_cuadro_total+8)*mm, p_a_cuenta)
    canvas.drawRightString((posx_cuadro_total+ancho_cuadro_total-2)*mm, (posy_cuadro_total+3)*mm, p_saldo)
    canvas.setFont("Helvetica", 10)

    # material
    p_material = ""
    for detalle in venta_detalles:
        if detalle.material_id > 0:
            material = apps.get_model('configuraciones', 'Materiales').objects.get(pk=detalle.material_id)
            p_material += material.material + ', '
    if len(p_material) > 0:
        p_material = p_material[0:len(p_material)-2]

    #canvas.drawString(5*mm, (posy_material+1.5+6)*mm, p_material)
    # p_material = "cr-39, cr-39 ar, policarbonato, poly ar, vidrio pgx, vidrio blanco, org. transition, poly transition, blue cut, blue blocker,  blue light shield"
    texto_material = lineas_cadena(p_material, 45)
    descuento = 0
    for texto in texto_material:
        canvas.drawString(5*mm, (posy_material+1.5+6+descuento)*mm, texto.strip())
        descuento = descuento-5

    # montura
    p_montura = ""
    for detalle in venta_detalles:
        if detalle.tipo_montura_id > 0:
            tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=detalle.tipo_montura_id)
            p_montura += tipo_montura.tipo_montura + ', '
    if len(p_montura) > 0:
        p_montura = p_montura[0:len(p_montura)-2]

    #canvas.drawString(138*mm, (posy_tipo_montura+1.5+6)*mm, p_montura)
    #p_montura = "cr-39, cr-39 ar, policarbonato, poly ar, vidrio pgx, vidrio blanco, org. transition, poly transition, blue cut, blue blocker,  blue light shield"
    texto_montura = lineas_cadena(p_montura, 40)
    descuento = 0
    for texto in texto_montura:
        canvas.drawString(138*mm, (posy_tipo_montura+1.5+6+descuento)*mm, texto.strip())
        descuento = descuento-5

    # numero de venta
    canvas.setFillColorRGB(191/255, 0/255, 0/255)
    canvas.drawString(150*mm, 270*mm, "N " + rellenar_numero(venta.numero_venta, 6))
    if venta.status_id.status_id == settings.STATUS_ANULADO:
        canvas.drawString(150*mm, 264*mm, "ANULADO")

    canvas.drawString(150*mm, 200*mm, "N " + rellenar_numero(venta.numero_venta, 6))
    if venta.status_id.status_id == settings.STATUS_ANULADO:
        canvas.drawString(150*mm, 194*mm, "ANULADO")

    # copia empresa
    # copia empresa
    # logos
    posY = 174
    canvas.drawImage(dir_img, 15*mm, (posY+18)*mm, width=77, height=35)
    canvas.drawImage(dir_img2, 5*mm, (posY+5)*mm, width=136, height=35)
    canvas.drawImage(dir_img_whatsapp, 132*mm, (posY+16)*mm, width=12, height=12)
    canvas.drawImage(dir_img_facebook, 95*mm, (posY+10.5)*mm, width=12, height=12)

    # datos optica
    posx_datos = 80
    posy_datos = 200
    canvas.setFont("Helvetica", 10)
    canvas.setFillColorRGB(51/255, 51/255, 51/255)
    canvas.drawString(posx_datos*mm, posy_datos*mm, 'Av. San Martín Nº 147 entre Heroinas')
    canvas.drawString((posx_datos+5)*mm, (posy_datos-5)*mm, 'y Colombia Edif. Principito P/B')
    canvas.drawString((posx_datos+4)*mm, (posy_datos-10)*mm, 'Telf.: ')
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString((posx_datos+12.5)*mm, (posy_datos-10)*mm, '4331765')
    canvas.setFont("Helvetica", 10)
    canvas.drawString((posx_datos+27)*mm, (posy_datos-10)*mm, 'Cel.: ')
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString((posx_datos+35)*mm, (posy_datos-10)*mm, '70791680')
    canvas.setFont("Helvetica", 10)
    canvas.drawString((posx_datos+20)*mm, (posy_datos-15)*mm, 'Optica Ideal')

    # canvas.drawString(posx_datos*mm, posy_datos*mm, 'Av. San Martín Nº 147 entre Heroinas')
    # canvas.drawString((posx_datos+5)*mm, (posy_datos-5)*mm, 'y Colombia Edif. Principito P/B')
    # canvas.drawString((posx_datos+4)*mm, (posy_datos-10)*mm, 'Telf.: 4331765 Cel.: 70791680')
    # canvas.drawString((posx_datos+17)*mm, (posy_datos-15)*mm, 'Optica Ideal')

    canvas.setFont("Helvetica", 10)
    # colores cabecera tabla
    canvas.setStrokeColorRGB(13/255, 166/255, 171/255)
    canvas.setFillColorRGB(13/255, 166/255, 171/255)

    # fecha preventa
    posy_fecha_preventa = 188
    posx_fecha_preventa = 174
    canvas.roundRect(posx_fecha_preventa*mm, posy_fecha_preventa*mm, 35*mm, 15*mm, 6, stroke=1, fill=0)
    # cabecera
    canvas.roundRect(posx_fecha_preventa*mm, (posy_fecha_preventa+8)*mm, 35*mm, 7*mm, 6, stroke=1, fill=1)
    canvas.rect(posx_fecha_preventa*mm, (posy_fecha_preventa+8)*mm, 35*mm, 2*mm, fill=1)
    # lineas
    canvas.line((posx_fecha_preventa+10)*mm, posy_fecha_preventa*mm, (posx_fecha_preventa+10)*mm, (posy_fecha_preventa+8)*mm)
    canvas.line((posx_fecha_preventa+10+12)*mm, posy_fecha_preventa*mm, (posx_fecha_preventa+10+12)*mm, (posy_fecha_preventa+8)*mm)

    # nombre
    posy_nombre = 163
    canvas.roundRect(4*mm, posy_nombre*mm, 130*mm, 12*mm, 6, stroke=1, fill=0)
    canvas.roundRect(4*mm, (posy_nombre+12-6)*mm, 130*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(4*mm, (posy_nombre+12-6)*mm, 130*mm, 2*mm, fill=1)

    # material empleado
    posy_material = 142
    ancho_material = 80
    canvas.roundRect(4*mm, posy_material*mm, ancho_material*mm, 18*mm, 6, stroke=1, fill=0)
    canvas.roundRect(4*mm, (posy_material+18-6)*mm, ancho_material*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(4*mm, (posy_material+18-6)*mm, ancho_material*mm, 2*mm, fill=1)

    # fecha entrega
    posy_fecha_entrega = 142
    ancho_fecha_entrega = 48
    canvas.roundRect(86*mm, posy_fecha_entrega*mm, ancho_fecha_entrega*mm, 18*mm, 6, stroke=1, fill=0)
    canvas.roundRect(86*mm, (posy_fecha_entrega+18-6)*mm, ancho_fecha_entrega*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(86*mm, (posy_fecha_entrega+18-6-6)*mm, ancho_fecha_entrega*mm, 8*mm, fill=1)
    # lineas fecha entrega
    canvas.line(96*mm, posy_fecha_entrega*mm, 96*mm, (posy_fecha_entrega+10)*mm)
    canvas.line(106*mm, posy_fecha_entrega*mm, 106*mm, (posy_fecha_entrega+10)*mm)
    canvas.line(118*mm, posy_fecha_entrega*mm, 118*mm, (posy_fecha_entrega+10)*mm)

    # tipo de montura
    posy_tipo_montura = 142
    ancho_tipo_montura = 74
    canvas.roundRect(136*mm, posy_tipo_montura*mm, ancho_tipo_montura*mm, 18*mm, 6, stroke=1, fill=0)
    canvas.roundRect(136*mm, (posy_tipo_montura+18-6)*mm, ancho_tipo_montura*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(136*mm, (posy_tipo_montura+18-6)*mm, ancho_tipo_montura*mm, 2*mm, fill=1)

    # cuadro total
    posy_cuadro_total = 163
    ancho_cuadro_total = 50
    posx_cuadro_total = 159
    canvas.setFillColorRGB(240/255, 240/255, 240/255)
    canvas.roundRect(posx_cuadro_total*mm, posy_cuadro_total*mm, ancho_cuadro_total*mm, 18*mm, 6, stroke=1, fill=1)
    #canvas.roundRect(posx_cuadro_total*mm, (posy_cuadro_total+18-6)*mm, ancho_cuadro_total*mm, 6*mm, 6, stroke=1, fill=1)
    #canvas.rect(posx_cuadro_total*mm, (posy_cuadro_total+18-6)*mm, ancho_cuadro_total*mm, 2*mm, fill=1)

    # cabecera fecha
    canvas.setFillColorRGB(255/255, 255/255, 255/255)
    canvas.drawString(176*mm, (posy_fecha_preventa+10)*mm, 'DIA')
    canvas.drawString(186*mm, (posy_fecha_preventa+10)*mm, 'MES')
    canvas.drawString(198*mm, (posy_fecha_preventa+10)*mm, 'AÑO')
    # nombre
    canvas.drawString(58*mm, (posy_nombre+8)*mm, 'NOMBRE')
    # material empleado
    canvas.drawString(23*mm, (posy_material+14)*mm, 'MATERIAL EMPLEADO')
    # fecha entrega
    canvas.drawString(95*mm, (posy_fecha_entrega+14)*mm, 'Fecha de Entrega')
    canvas.drawString(87*mm, (posy_fecha_entrega+8)*mm, 'DIA')
    canvas.drawString(97*mm, (posy_fecha_entrega+8)*mm, 'MES')
    canvas.drawString(108*mm, (posy_fecha_entrega+8)*mm, 'AÑO')
    canvas.drawString(122*mm, (posy_fecha_entrega+8)*mm, 'HRS')
    # tipo de montura
    canvas.drawString(158*mm, (posy_fecha_entrega+14)*mm, 'Tipo de Montura')

    # datos
    # datos fecha
    canvas.setStrokeColorRGB(51/255, 51/255, 51/255)
    canvas.setFillColorRGB(51/255, 51/255, 51/255)
    canvas.drawString(177*mm, (posy_fecha_preventa+2)*mm, p_dia)
    canvas.drawString(187*mm, (posy_fecha_preventa+2)*mm, p_mes)
    canvas.drawString(198*mm, (posy_fecha_preventa+2)*mm, p_anio)
    # nombre
    canvas.drawString(18*mm, (posy_nombre+1.5)*mm, venta.nombres + ' ' + venta.apellidos + ', ' + venta.telefonos)

    # cuadro total
    # canvas.drawRightString((posx_cuadro_total+ancho_cuadro_total-5)*mm, (posy_cuadro_total+13)*mm, "Total : " + str(venta.total) + " Bs.")
    # canvas.drawRightString((posx_cuadro_total+ancho_cuadro_total-5)*mm, (posy_cuadro_total+8)*mm, "A Cuenta : " + str(venta.a_cuenta) + " Bs.")
    # canvas.drawRightString((posx_cuadro_total+ancho_cuadro_total-5)*mm, (posy_cuadro_total+3)*mm, "Saldo : " + str(venta.saldo) + " Bs.")
    canvas.setFont("Courier", 10)
    canvas.drawRightString((posx_cuadro_total+ancho_cuadro_total-2)*mm, (posy_cuadro_total+13)*mm, p_total)
    canvas.drawRightString((posx_cuadro_total+ancho_cuadro_total-2)*mm, (posy_cuadro_total+8)*mm, p_a_cuenta)
    canvas.drawRightString((posx_cuadro_total+ancho_cuadro_total-2)*mm, (posy_cuadro_total+3)*mm, p_saldo)
    canvas.setFont("Helvetica", 10)

    # material
    #canvas.drawString(5*mm, (posy_material+1.5+6)*mm, p_material)
    descuento = 0
    for texto in texto_material:
        canvas.drawString(5*mm, (posy_material+1.5+6+descuento)*mm, texto.strip())
        descuento = descuento-5

    # montura
    # canvas.drawString(138*mm, (posy_tipo_montura+1.5+6)*mm, p_montura)
    descuento = 0
    for texto in texto_montura:
        canvas.drawString(138*mm, (posy_tipo_montura+1.5+6+descuento)*mm, texto.strip())
        descuento = descuento-5

    # datos laboratorio
    # datos laboratorio
    canvas.setFont("Helvetica", 10)
    canvas.setStrokeColorRGB(13/255, 166/255, 171/255)
    canvas.setFillColorRGB(13/255, 166/255, 171/255)

    # laboratorio
    posy_laboratorio = 123
    canvas.roundRect(4*mm, posy_laboratorio*mm, 130*mm, 12*mm, 6, stroke=1, fill=0)
    canvas.roundRect(4*mm, (posy_laboratorio+12-6)*mm, 130*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(4*mm, (posy_laboratorio+12-6)*mm, 130*mm, 2*mm, fill=1)

    # tecnico
    posy_tecnico = 108
    canvas.roundRect(4*mm, posy_tecnico*mm, 130*mm, 12*mm, 6, stroke=1, fill=0)
    canvas.roundRect(4*mm, (posy_tecnico+12-6)*mm, 130*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(4*mm, (posy_tecnico+12-6)*mm, 130*mm, 2*mm, fill=1)

    # oftalmologo
    posy_oftalmologo = 93
    canvas.roundRect(4*mm, posy_oftalmologo*mm, 130*mm, 12*mm, 6, stroke=1, fill=0)
    canvas.roundRect(4*mm, (posy_oftalmologo+12-6)*mm, 130*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(4*mm, (posy_oftalmologo+12-6)*mm, 130*mm, 2*mm, fill=1)

    # vendedor
    posy_vendedor = 78
    canvas.roundRect(4*mm, posy_vendedor*mm, 60*mm, 12*mm, 6, stroke=1, fill=0)
    canvas.roundRect(4*mm, (posy_vendedor+12-6)*mm, 60*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(4*mm, (posy_vendedor+12-6)*mm, 60*mm, 2*mm, fill=1)

    # entregado
    posy_entregado = 78
    canvas.roundRect((4+60+10)*mm, posy_entregado*mm, 60*mm, 12*mm, 6, stroke=1, fill=0)
    canvas.roundRect((4+60+10)*mm, (posy_entregado+12-6)*mm, 60*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect((4+60+10)*mm, (posy_entregado+12-6)*mm, 60*mm, 2*mm, fill=1)

    # nota
    posy_nota = 64
    canvas.roundRect(4*mm, posy_nota*mm, 205*mm, 12*mm, 6, stroke=1, fill=0)
    canvas.roundRect(4*mm, (posy_nota+12-6)*mm, 205*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(4*mm, (posy_nota+12-6)*mm, 205*mm, 2*mm, fill=1)

    # medidas del cliente, lejos
    posy_medidas_lejos = 111
    posx_medidas_lejos = 136.5
    ancho_medidas_lejos = 73
    canvas.roundRect(posx_medidas_lejos*mm, posy_medidas_lejos*mm, ancho_medidas_lejos*mm, 24*mm, 6, stroke=1, fill=0)
    canvas.roundRect(posx_medidas_lejos*mm, (posy_medidas_lejos+24-6)*mm, ancho_medidas_lejos*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(posx_medidas_lejos*mm, (posy_medidas_lejos+24-6-6)*mm, ancho_medidas_lejos*mm, 8*mm, fill=1)
    # lineas
    canvas.line((posx_medidas_lejos+10)*mm, posy_medidas_lejos*mm, (posx_medidas_lejos+10)*mm, (posy_medidas_lejos+12)*mm)
    canvas.line((posx_medidas_lejos+10+10)*mm, posy_medidas_lejos*mm, (posx_medidas_lejos+10+10)*mm, (posy_medidas_lejos+12)*mm)
    canvas.line((posx_medidas_lejos+10+10+10)*mm, posy_medidas_lejos*mm, (posx_medidas_lejos+10+10+10)*mm, (posy_medidas_lejos+12)*mm)
    canvas.line((posx_medidas_lejos+10+10+10+10)*mm, posy_medidas_lejos*mm, (posx_medidas_lejos+10+10+10+10)*mm, (posy_medidas_lejos+12)*mm)
    canvas.line((posx_medidas_lejos+10+10+10+10+10)*mm, posy_medidas_lejos*mm, (posx_medidas_lejos+10+10+10+10+10)*mm, (posy_medidas_lejos+12)*mm)
    canvas.line((posx_medidas_lejos+10+10+10+10+10+10)*mm, posy_medidas_lejos*mm, (posx_medidas_lejos+10+10+10+10+10+10)*mm, (posy_medidas_lejos+12)*mm)
    # linea divisoria
    canvas.line((posx_medidas_lejos)*mm, (posy_medidas_lejos+6)*mm, (posx_medidas_lejos+ancho_medidas_lejos)*mm, (posy_medidas_lejos+6)*mm)
    # titulos
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString((posx_medidas_lejos+2)*mm, (posy_medidas_lejos+7.5)*mm, 'Esf')
    canvas.drawString((posx_medidas_lejos+12)*mm, (posy_medidas_lejos+7.5)*mm, 'Cli')
    canvas.drawString((posx_medidas_lejos+22)*mm, (posy_medidas_lejos+7.5)*mm, 'Eje')
    canvas.drawString((posx_medidas_lejos+32)*mm, (posy_medidas_lejos+7.5)*mm, 'Esf')
    canvas.drawString((posx_medidas_lejos+42)*mm, (posy_medidas_lejos+7.5)*mm, 'Cli')
    canvas.drawString((posx_medidas_lejos+52)*mm, (posy_medidas_lejos+7.5)*mm, 'Eje')
    canvas.drawString((posx_medidas_lejos+62)*mm, (posy_medidas_lejos+7.5)*mm, 'D.I.')
    canvas.setFillColorRGB(0/255, 0/255, 0/255)
    # medidas cabeceras
    canvas.setFillColorRGB(255/255, 255/255, 255/255)
    canvas.setFont("Helvetica", 10)
    canvas.drawString((posx_medidas_lejos+24)*mm, (posy_medidas_lejos+19.5)*mm, 'MEDIDA LEJOS')
    # ojo derecho
    canvas.drawString((posx_medidas_lejos+14)*mm, (posy_medidas_lejos+14.5)*mm, 'O.D.')
    # ojo izquierdo
    canvas.drawString((posx_medidas_lejos+44)*mm, (posy_medidas_lejos+14.5)*mm, 'O.I.')

    # medidas del cliente, cerca
    posy_medidas_cerca = 84
    posx_medidas_cerca = 136.5
    ancho_medidas_cerca = 73
    canvas.setFillColorRGB(13/255, 166/255, 171/255)
    canvas.roundRect(posx_medidas_cerca*mm, posy_medidas_cerca*mm, ancho_medidas_cerca*mm, 24*mm, 6, stroke=1, fill=0)
    canvas.roundRect(posx_medidas_cerca*mm, (posy_medidas_cerca+24-6)*mm, ancho_medidas_cerca*mm, 6*mm, 6, stroke=1, fill=1)
    canvas.rect(posx_medidas_cerca*mm, (posy_medidas_cerca+24-6-6)*mm, ancho_medidas_cerca*mm, 8*mm, fill=1)
    # lineas
    canvas.line((posx_medidas_cerca+10)*mm, posy_medidas_cerca*mm, (posx_medidas_cerca+10)*mm, (posy_medidas_cerca+12)*mm)
    canvas.line((posx_medidas_cerca+10+10)*mm, posy_medidas_cerca*mm, (posx_medidas_cerca+10+10)*mm, (posy_medidas_cerca+12)*mm)
    canvas.line((posx_medidas_cerca+10+10+10)*mm, posy_medidas_cerca*mm, (posx_medidas_cerca+10+10+10)*mm, (posy_medidas_cerca+12)*mm)
    canvas.line((posx_medidas_cerca+10+10+10+10)*mm, posy_medidas_cerca*mm, (posx_medidas_cerca+10+10+10+10)*mm, (posy_medidas_cerca+12)*mm)
    canvas.line((posx_medidas_cerca+10+10+10+10+10)*mm, posy_medidas_cerca*mm, (posx_medidas_cerca+10+10+10+10+10)*mm, (posy_medidas_cerca+12)*mm)
    canvas.line((posx_medidas_cerca+10+10+10+10+10+10)*mm, posy_medidas_cerca*mm, (posx_medidas_cerca+10+10+10+10+10+10)*mm, (posy_medidas_cerca+12)*mm)
    # linea divisoria
    canvas.line((posx_medidas_cerca)*mm, (posy_medidas_cerca+6)*mm, (posx_medidas_cerca+ancho_medidas_cerca)*mm, (posy_medidas_cerca+6)*mm)
    # titulos
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString((posx_medidas_cerca+2)*mm, (posy_medidas_cerca+7.5)*mm, 'Esf')
    canvas.drawString((posx_medidas_cerca+12)*mm, (posy_medidas_cerca+7.5)*mm, 'Cli')
    canvas.drawString((posx_medidas_cerca+22)*mm, (posy_medidas_cerca+7.5)*mm, 'Eje')
    canvas.drawString((posx_medidas_cerca+32)*mm, (posy_medidas_cerca+7.5)*mm, 'Esf')
    canvas.drawString((posx_medidas_cerca+42)*mm, (posy_medidas_cerca+7.5)*mm, 'Cli')
    canvas.drawString((posx_medidas_cerca+52)*mm, (posy_medidas_cerca+7.5)*mm, 'Eje')
    canvas.drawString((posx_medidas_cerca+62)*mm, (posy_medidas_cerca+7.5)*mm, 'D.I.')

    # medidas cabeceras
    canvas.setFillColorRGB(255/255, 255/255, 255/255)
    canvas.setFont("Helvetica", 10)
    canvas.drawString((posx_medidas_cerca+24)*mm, (posy_medidas_cerca+19.5)*mm, 'MEDIDA CERCA')
    # ojo derecho
    canvas.drawString((posx_medidas_cerca+14)*mm, (posy_medidas_cerca+14.5)*mm, 'O.D.')
    # ojo izquierdo
    canvas.drawString((posx_medidas_cerca+44)*mm, (posy_medidas_cerca+14.5)*mm, 'O.I.')

    # laboratorio
    canvas.drawString(44*mm, (posy_laboratorio+8)*mm, 'Laboratorio')
    # tecnico
    canvas.drawString(44*mm, (posy_tecnico+8)*mm, 'Tecnico')
    # oftalmologo
    canvas.drawString(44*mm, (posy_oftalmologo+8)*mm, 'Oftalmologo')
    # vendedor
    canvas.drawString(24*mm, (posy_vendedor+8)*mm, 'Vendedor')
    # entregado
    canvas.drawString(90*mm, (posy_entregado+8)*mm, 'Entregado')
    # nota
    canvas.drawString(44*mm, (posy_nota+8)*mm, 'Nota')

    # datos
    canvas.setFillColorRGB(51/255, 51/255, 51/255)
    # laboratorio
    if venta.laboratorio_id > 0:
        laboratorio = apps.get_model('configuraciones', 'Laboratorios').objects.get(pk=venta.laboratorio_id)
        canvas.drawString(10*mm, (posy_laboratorio+1.5)*mm, laboratorio.laboratorio)
    # tecnico
    if venta.tecnico_id > 0:
        tecnico = apps.get_model('configuraciones', 'Tecnicos').objects.get(pk=venta.tecnico_id)
        canvas.drawString(10*mm, (posy_tecnico+1.5)*mm, tecnico.tecnico)
    # oftalmologo
    if venta.oftalmologo_id > 0:
        oftalmologo = apps.get_model('configuraciones', 'Oftalmologos').objects.get(pk=venta.oftalmologo_id)
        canvas.drawString(10*mm, (posy_oftalmologo+1.5)*mm, oftalmologo.oftalmologo)
    # vendedor
    canvas.drawString(10*mm, (posy_vendedor+1.5)*mm, venta.user_perfil_id_preventa.user_id.first_name+' '+venta.user_perfil_id_preventa.user_id.last_name)
    # entrega
    if venta.user_perfil_id_finaliza > 0:
        user_venta = apps.get_model('permisos', 'UsersPerfiles').objects.get(pk=venta.user_perfil_id_finaliza)
        canvas.drawString(80*mm, (posy_entregado+1.5)*mm, user_venta.user_id.first_name+' '+user_venta.user_id.last_name)
    # nota
    canvas.drawString(10*mm, (posy_nota+1.5)*mm, venta.nota)

    # medidas lejos
    canvas.setFont("Helvetica", 9)
    canvas.drawString((posx_medidas_lejos+1) * mm, (posy_medidas_lejos+1.5)*mm, str(venta.lejos_od_esf))
    canvas.drawString((posx_medidas_lejos+1+10) * mm, (posy_medidas_lejos+1.5)*mm, str(venta.lejos_od_cli))
    canvas.drawString((posx_medidas_lejos+1+20) * mm, (posy_medidas_lejos+1.5)*mm, str(venta.lejos_od_eje))
    canvas.drawString((posx_medidas_lejos+1+30) * mm, (posy_medidas_lejos+1.5)*mm, str(venta.lejos_oi_esf))
    canvas.drawString((posx_medidas_lejos+1+40) * mm, (posy_medidas_lejos+1.5)*mm, str(venta.lejos_oi_cli))
    canvas.drawString((posx_medidas_lejos+1+50) * mm, (posy_medidas_lejos+1.5)*mm, str(venta.lejos_oi_eje))
    canvas.drawString((posx_medidas_lejos+1+60) * mm, (posy_medidas_lejos+1.5)*mm, str(venta.lejos_di))

    # medidas cerca
    canvas.drawString((posx_medidas_cerca+1) * mm, (posy_medidas_cerca+1.5)*mm, str(venta.cerca_od_esf))
    canvas.drawString((posx_medidas_cerca+1+10) * mm, (posy_medidas_cerca+1.5)*mm, str(venta.cerca_od_cli))
    canvas.drawString((posx_medidas_cerca+1+20) * mm, (posy_medidas_cerca+1.5)*mm, str(venta.cerca_od_eje))
    canvas.drawString((posx_medidas_cerca+1+30) * mm, (posy_medidas_cerca+1.5)*mm, str(venta.cerca_oi_esf))
    canvas.drawString((posx_medidas_cerca+1+40) * mm, (posy_medidas_cerca+1.5)*mm, str(venta.cerca_oi_cli))
    canvas.drawString((posx_medidas_cerca+1+50) * mm, (posy_medidas_cerca+1.5)*mm, str(venta.cerca_oi_eje))
    canvas.drawString((posx_medidas_cerca+1+60) * mm, (posy_medidas_cerca+1.5)*mm, str(venta.cerca_di))

    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))
    canvas.restoreState()


def rptVentasDisenio(buffer_pdf, usuario, venta_id):

    # datos sucursal
    user_perfil = apps.get_model('permisos', 'UsersPerfiles').objects.get(user_id=usuario)
    punto = apps.get_model('configuraciones', 'Puntos').objects.get(pk=user_perfil.punto_id)
    sucursal_id_user = punto.sucursal_id.sucursal_id
    global RPT_SUCURSAL_ID
    RPT_SUCURSAL_ID = sucursal_id_user

    # venta
    venta = Ventas.objects.get(pk=venta_id)
    ventas_detalles = VentasDetalles.objects.filter(venta_id=venta)

    # verificamos si esta anulado
    dato_anulado = ''
    if venta.status_id.status_id == settings.STATUS_ANULADO:
        usuario_perfil_anula = apps.get_model('permisos', 'UsersPerfiles').objects.get(pk=venta.user_perfil_id_anula)
        motivo_anula = venta.motivo_anula
        dato_anulado = usuario_perfil_anula.user_id.username + ', ' + motivo_anula

    global DATO_REGISTRO, RPT_CONTRATO, RPT_ESTADO, RPT_ANULADO, AUMENTO_Y
    DATO_REGISTRO = str(venta.venta_id)
    RPT_CONTRATO = str(venta.numero_venta)
    RPT_ESTADO = 'PREVENTA'

    if len(venta.nota) > 120:
        AUMENTO_Y = 8
    else:
        AUMENTO_Y = 4

    if venta.status_id.status_id == settings.STATUS_VENTA:
        RPT_ESTADO = 'VENTA'
    if venta.status_id.status_id == settings.STATUS_FINALIZADO:
        RPT_ESTADO = 'FINALIZADO'
    RPT_ANULADO = dato_anulado

    styles = getSampleStyleSheet()
    # personalizamos
    style_tabla_datos = ParagraphStyle('tabla_datos',
                                       fontName="Helvetica",
                                       fontSize=8,
                                       parent=styles['Normal'],
                                       alignment=0,
                                       spaceAfter=0)

    style_firmas = ParagraphStyle('firmas',
                                  fontName="Helvetica",
                                  fontSize=10,
                                  parent=styles['Normal'],
                                  alignment=0,
                                  spaceAfter=0)

    # hoja vertical
    doc = SimpleDocTemplate(buffer_pdf, pagesize=letter, leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    # hoja horizontal
    # doc = SimpleDocTemplate(buffer_pdf, pagesize=landscape(letter), leftMargin=10 * mm, rightMargin=10 * mm, topMargin=10 * mm, bottomMargin=15 * mm)

    # PLAN DE PAGOS
    Story = []
    Story.append(Spacer(100*mm, 11*mm))

    if venta.plan_pago == 1:
        status_activo = apps.get_model('status', 'Status').objects.get(pk=settings.STATUS_ACTIVO)
        plan_pago = apps.get_model('ventas', 'PlanPagos').objects.get(venta_id=venta.venta_id, status_id=status_activo)
        plan_pago_detalles = apps.get_model('ventas', 'PlanPagosDetalles').objects.filter(plan_pago_id=plan_pago).order_by('numero_cuota')

        Story.append(PageBreak())
        # tabla
        datos_tabla = []
        data = []

        data.append(['Cuotas :', str(plan_pago.numero_cuotas), 'Monto :', str(plan_pago.monto_total) + ' Bs.'])
        data.append(['Fecha :', get_date_show(fecha=plan_pago.fecha, formato='dd-MMM-yyyy'), '', ''])

        tabla_datos = Table(data, colWidths=[25*mm, 30*mm, 25*mm, 30*mm], repeatRows=1)
        tabla_datos.setStyle(TableStyle([
                                        # ('BACKGROUND', (0, 0), (3, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                        # ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                                        ('ALIGN', (0, 0), (0, 1), 'RIGHT'),
                                        ('ALIGN', (1, 0), (1, 1), 'LEFT'),

                                        ('ALIGN', (2, 0), (2, 1), 'RIGHT'),
                                        ('ALIGN', (3, 0), (3, 1), 'LEFT'),

                                        #('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                        ('FONTSIZE', (0, 0), (-1, -1), 9),

                                        ('FONTNAME', (0, 0), (0, 1), 'Helvetica-Bold'),
                                        ('FONTNAME', (2, 0), (2, 1), 'Helvetica-Bold'),

                                        ('FONTNAME', (1, 0), (1, 1), 'Helvetica'),
                                        ('FONTNAME', (3, 0), (3, 1), 'Helvetica'),

                                        ('LEFTPADDING', (0, 0), (3, 1), 1),
                                        ('RIGHTPADDING', (0, 0), (3, 1), 1),
                                        ('VALIGN', (0, 0), (3, 1), 'TOP'),
                                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
        # aniadimos la tabla
        Story.append(tabla_datos)

        # tabla
        datos_tabla = []
        data = []

        # cabecera
        data.append(['Cuota', 'Fecha', 'Monto', 'Saldo'])
        filas = 0
        total = 0

        # cargamos los registros
        for detalle in plan_pago_detalles:
            datos_tabla = []
            datos_tabla = [str(detalle.numero_cuota), get_date_show(fecha=detalle.fecha, formato='dd-MMM-yyyy'), str(detalle.monto), str(detalle.saldo)]
            data.append(datos_tabla)
            filas += 1
            total += detalle.monto

        # aniadimos la tabla
        datos_tabla = ['', 'Total :', str(round(total, 2)), '']
        data.append(datos_tabla)

        tabla_datos = Table(data, colWidths=[20*mm, 30*mm, 25*mm, 25*mm], repeatRows=1)
        tabla_datos.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (3, 0), colors.Color(red=(204/255), green=(204/255), blue=(204/255))),
                                        ('ALIGN', (0, filas), (1, filas), 'LEFT'),
                                        ('ALIGN', (1, filas+1), (1, filas+1), 'RIGHT'),
                                        ('ALIGN', (2, 0), (3, filas+1), 'RIGHT'),

                                        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                        ('FONTSIZE', (0, 0), (-1, -1), 9),

                                        ('FONTNAME', (0, 0), (3, 0), 'Helvetica-Bold'),
                                        ('FONTNAME', (1, filas+1), (3, filas+1), 'Helvetica-Bold'),

                                        ('FONTNAME', (0, 1), (3, filas), 'Helvetica'),

                                        ('LEFTPADDING', (0, 0), (3, filas+1), 1),
                                        ('RIGHTPADDING', (0, 0), (3, filas+1), 1),
                                        ('VALIGN', (0, 0), (3, filas+1), 'TOP'),
                                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
        # aniadimos la tabla
        Story.append(tabla_datos)

    # creamos
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


def set_puntos_string(cadena, monto, longitud):
    len_monto = len(monto)
    len_cadena = len(cadena)
    suma = len_monto + len_cadena
    retorno = cadena
    while suma < longitud:
        retorno += "."
        suma += 1
    retorno += monto

    return retorno


def lineas_cadena(cadena, longitud):
    division = cadena.split(' ')
    retorno = []
    cont = 0
    pos = 0
    aux_cade = ""
    while cont < len(division):
        if(len(aux_cade) > longitud):
            retorno.append(aux_cade)
            aux_cade = division[pos] + " "
        else:
            aux_cade += division[pos] + " "

        cont += 1
        pos += 1

    if len(aux_cade) > 0:
        retorno.append(aux_cade)

    return retorno


def rellenar_numero(numero, longitud):
    retorno = str(numero)
    tam = len(retorno)
    while tam < longitud:
        retorno = "0" + retorno
        tam += 1

    return retorno
