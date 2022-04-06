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

    # fuente
    canvas.setFont("Helvetica", 10)
    canvas.setFillColorRGB(51/255, 51/255, 51/255)

    # venta
    venta = Ventas.objects.get(pk=int(DATO_REGISTRO))
    venta_detalles = VentasDetalles.objects.filter(venta_id=venta)

    # fecha
    posx_fecha = 158
    posy_fecha = 265.5
    fecha_preventa = get_date_show(venta.fecha_preventa, formato_ori='yyyy-mm-dd HH:ii:ss', formato='dd-MMM-yyyy')
    aux_div = fecha_preventa.split('-')
    p_dia = aux_div[0]
    p_mes = aux_div[1]
    p_anio = aux_div[2]
    canvas.drawString(posx_fecha*mm, posy_fecha*mm, p_dia)
    canvas.drawString((posx_fecha+12)*mm, posy_fecha*mm, p_mes)
    canvas.drawString((posx_fecha+26)*mm, posy_fecha*mm, p_anio)

    # totales
    posx_totales = 195
    posy_totales = 255.5
    canvas.drawRightString(posx_totales*mm, posy_totales*mm, str(venta.total) + ' Bs.')
    canvas.drawRightString(posx_totales*mm, 247.5*mm, str(venta.a_cuenta) + ' Bs.')
    canvas.drawRightString(posx_totales*mm, 239.5*mm, str(venta.saldo) + ' Bs.')

    # nombre
    posx_nombre = 18
    posy_nombre = 232.5
    canvas.drawString(posx_nombre*mm, posy_nombre*mm, venta.nombres + ' ' + venta.apellidos)

    # material empleado
    posx_material = 14
    posy_material = 220
    p_material = ""
    for detalle in venta_detalles:
        if detalle.material_id > 0:
            material = apps.get_model('configuraciones', 'Materiales').objects.get(pk=detalle.material_id)
            p_material += material.material + ', '
    if len(p_material) > 0:
        p_material = p_material[0:len(p_material)-2]
    # dividiendo en lineas
    texto_material = lineas_cadena(p_material, 44)
    descuento = 0
    for texto in texto_material:
        canvas.drawString(posx_material*mm, (posy_material+descuento)*mm, texto.strip())
        descuento = descuento-5

    # montura
    posx_montura = 158.5
    posy_montura = 219.5
    p_montura = ""
    for detalle in venta_detalles:
        if detalle.tipo_montura_id > 0:
            tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=detalle.tipo_montura_id)
            p_montura += tipo_montura.tipo_montura + ', '
    if len(p_montura) > 0:
        p_montura = p_montura[0:len(p_montura)-2]
    # division en lineas
    texto_montura = lineas_cadena(p_montura, 30)
    descuento = 0
    for texto in texto_montura:
        canvas.drawString(posx_montura*mm, (posy_montura+descuento)*mm, texto.strip())
        descuento = descuento-5

    # copia
    # copia
    # fecha
    posx_fecha = 158
    posy_fecha = 195.5
    canvas.drawString(posx_fecha*mm, posy_fecha*mm, p_dia)
    canvas.drawString((posx_fecha+12)*mm, posy_fecha*mm, p_mes)
    canvas.drawString((posx_fecha+26)*mm, posy_fecha*mm, p_anio)

    # totales
    posx_totales = 195
    #posy_totales = 188
    canvas.drawRightString(posx_totales*mm, 186.5*mm, str(venta.total) + ' Bs.')
    canvas.drawRightString(posx_totales*mm, 178.5*mm, str(venta.a_cuenta) + ' Bs.')
    canvas.drawRightString(posx_totales*mm, 170.5*mm, str(venta.saldo) + ' Bs.')

    # nombre
    posx_nombre = 44
    posy_nombre = 155.5
    canvas.drawString(posx_nombre*mm, posy_nombre*mm, venta.nombres + ' ' + venta.apellidos)

    # telefonos
    posx_telefonos = 167
    posy_telefonos = 155.5
    canvas.drawString(posx_telefonos*mm, posy_telefonos*mm, venta.telefonos)

    # material empleado
    posx_material = 14
    posy_material = 144
    descuento = 0
    for texto in texto_material:
        canvas.drawString(posx_material*mm, (posy_material+descuento)*mm, texto.strip())
        descuento = descuento-5

    # montura
    posx_montura = 160
    posy_montura = 144
    descuento = 0
    for texto in texto_montura:
        canvas.drawString(posx_montura*mm, (posy_montura+descuento)*mm, texto.strip())
        descuento = descuento-5

    # seleccion de materiales
    posx_check = 42.5
    desc_check = 5.5
    posx_check2 = 85
    desc_check2 = 7

    posy_check = 135
    posy_check2 = 134

    canvas.drawString(posx_check*mm, posy_check*mm, 'X')
    canvas.drawString(posx_check*mm, (posy_check-desc_check)*mm, 'X')
    canvas.drawString(posx_check*mm, (posy_check-2*desc_check)*mm, 'X')
    canvas.drawString(posx_check*mm, (posy_check-3*desc_check)*mm, 'X')
    canvas.drawString(posx_check*mm, (posy_check-4*desc_check)*mm, 'X')
    canvas.drawString(posx_check*mm, (posy_check-5*desc_check)*mm, 'X')
    canvas.drawString(posx_check*mm, (posy_check-6*desc_check)*mm, 'X')
    canvas.drawString(posx_check*mm, (posy_check-7*desc_check)*mm, 'X')
    canvas.drawString(posx_check*mm, (posy_check-8*desc_check)*mm, 'X')
    canvas.drawString(posx_check*mm, (posy_check-9*desc_check)*mm, 'X')
    canvas.drawString(posx_check*mm, (posy_check-10*desc_check)*mm, 'X')

    canvas.drawString(posx_check2*mm, posy_check2*mm, 'X')
    canvas.drawString(posx_check2*mm, (posy_check2-desc_check2)*mm, 'X')
    canvas.drawString(posx_check2*mm, (posy_check2-2*desc_check2)*mm, 'X')
    canvas.drawString(posx_check2*mm, (posy_check2-3*desc_check2)*mm, 'X')
    canvas.drawString(posx_check2*mm, (posy_check2-4*desc_check2)*mm, 'X')
    canvas.drawString(posx_check2*mm, (posy_check2-5*desc_check2)*mm, 'X')
    canvas.drawString(posx_check2*mm, (posy_check2-6*desc_check2)*mm, 'X')
    canvas.drawString(posx_check2*mm, (posy_check2-7*desc_check2)*mm, 'X')
    canvas.drawString(posx_check2*mm, (posy_check2-8*desc_check2)*mm, 'X')

    # laboratorio
    posx_laboratorio = 97
    posy_laboratorio = 123
    canvas.drawString(posx_laboratorio*mm, posy_laboratorio*mm, 'Laboratorio')

    # tecnico
    posx_tecnico = 97
    posy_tecnico = 103
    canvas.drawString(posx_tecnico*mm, posy_tecnico*mm, 'Tecnico')

    # oftalmologo
    posx_oftalmologo = 97
    posy_oftalmologo = 83
    canvas.drawString(posx_oftalmologo*mm, posy_oftalmologo*mm, 'Oftalmologo')

    # medidas
    # lejos
    posx_medidas_lejos = 141.5
    posy_medidas_lejos = 116.5
    canvas.drawString(posx_medidas_lejos*mm, posy_medidas_lejos*mm, str(venta.lejos_od_esf))
    canvas.drawString((posx_medidas_lejos+15)*mm, posy_medidas_lejos*mm, str(venta.lejos_od_cli))
    canvas.drawString((posx_medidas_lejos+30)*mm, posy_medidas_lejos*mm, str(venta.lejos_od_eje))
    canvas.drawString((posx_medidas_lejos+47)*mm, posy_medidas_lejos*mm, str(venta.lejos_di))
    # izquierdo
    posy_medidas_lejos2 = 100
    canvas.drawString(posx_medidas_lejos*mm, posy_medidas_lejos2*mm, str(venta.lejos_oi_esf))
    canvas.drawString((posx_medidas_lejos+18)*mm, posy_medidas_lejos2*mm, str(venta.lejos_oi_cli))
    canvas.drawString((posx_medidas_lejos+37)*mm, posy_medidas_lejos2*mm, str(venta.lejos_oi_eje))

    # cerca
    posx_medidas_cerca = 141.5
    posy_medidas_cerca = 72
    canvas.drawString(posx_medidas_cerca*mm, posy_medidas_cerca*mm, str(venta.lejos_od_esf))
    canvas.drawString((posx_medidas_cerca+15)*mm, posy_medidas_cerca*mm, str(venta.lejos_od_cli))
    canvas.drawString((posx_medidas_cerca+30)*mm, posy_medidas_cerca*mm, str(venta.lejos_od_eje))
    canvas.drawString((posx_medidas_cerca+47)*mm, posy_medidas_cerca*mm, str(venta.lejos_di))
    # izquierdo
    posy_medidas_cerca2 = 53
    canvas.drawString(posx_medidas_cerca*mm, posy_medidas_cerca2*mm, str(venta.lejos_oi_esf))
    canvas.drawString((posx_medidas_cerca+18)*mm, posy_medidas_cerca2*mm, str(venta.lejos_oi_cli))
    canvas.drawString((posx_medidas_cerca+37)*mm, posy_medidas_cerca2*mm, str(venta.lejos_oi_eje))

    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()

    canvas.setFont('Times-Italic', 8)
    canvas.drawRightString(pagesize[0] - 15 * mm, 10 * mm, "pag. %d" % (doc.page,))
    canvas.restoreState()


def rptVentasPreImpreso(buffer_pdf, usuario, venta_id):

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
    # armamos
    Story = []
    if RPT_ANULADO == '':
        Story.append(Spacer(100*mm, 61*mm))
    else:
        Story.append(Spacer(100*mm, 66*mm))

    if AUMENTO_Y == 4:
        Story.append(Spacer(100*mm, 4*mm))
    if AUMENTO_Y == 8:
        Story.append(Spacer(100*mm, 8*mm))
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
