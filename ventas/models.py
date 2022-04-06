from django.db import models
from django.conf import settings

from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome, DateFieldCustome
from configuraciones.models import Puntos, Almacenes, Cajas, Sucursales
from clientes.models import Clientes
from permisos.models import UsersPerfiles


class Ventas(models.Model):
    venta_id = models.AutoField(primary_key=True, db_column='venta_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    almacen_id = models.ForeignKey(Almacenes, to_field='almacen_id', on_delete=models.PROTECT, db_column='almacen_id')
    cliente_id = models.ForeignKey(Clientes, to_field='cliente_id', on_delete=models.PROTECT, db_column='cliente_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_preventa = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id_preventa')
    fecha_preventa = DateTimeFieldCustome(null=True, blank=True)

    user_perfil_id_venta = models.IntegerField(null=False, blank=False, default=0)
    fecha_venta = DateTimeFieldCustome(null=True, blank=True)

    user_perfil_id_finaliza = models.IntegerField(null=False, blank=False, default=0)
    fecha_finaliza = DateTimeFieldCustome(null=True, blank=True)

    cupon_id = models.IntegerField(null=False, blank=False, default=0)
    cupon = models.CharField(max_length=50, null=False, blank=False, default='')

    caja_id = models.IntegerField(null=False, blank=False, default=0)
    laboratorio_id = models.IntegerField(null=False, blank=False, default=0)
    tecnico_id = models.IntegerField(null=False, blank=False, default=0)
    oftalmologo_id = models.IntegerField(null=False, blank=False, default=0)
    stock_id = models.IntegerField(null=False, blank=False, default=0)

    nombres = models.CharField(max_length=150, blank=False, null=False)
    apellidos = models.CharField(max_length=150, blank=False, null=False)
    ci_nit = models.CharField(max_length=150, blank=False, null=False)
    telefonos = models.CharField(max_length=150, blank=False, null=False)
    direccion = models.CharField(max_length=250, blank=False, null=False)
    factura_a = models.CharField(max_length=250, blank=False, null=False)

    lejos_od_esf = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    lejos_od_cli = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    lejos_od_eje = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    lejos_oi_esf = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    lejos_oi_cli = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    lejos_oi_eje = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    lejos_di = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    cerca_od_esf = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cerca_od_cli = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cerca_od_eje = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cerca_oi_esf = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cerca_oi_cli = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cerca_oi_eje = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cerca_di = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    #qr, transferencia, tarjeta, efectivo
    tipo_venta = models.CharField(max_length=50, blank=False, null=False)
    # si la venta se pagara con plan de pagos
    plan_pago = models.IntegerField(blank=False, null=False, default=0)
    numero_venta = models.IntegerField(blank=False, null=False, default=0)

    precio_montura = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    precio_material = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    a_cuenta = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    nota = models.CharField(max_length=250, blank=False, null=False)

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'ventas'


class VentasDetalles(models.Model):
    venta_detalle_id = models.AutoField(primary_key=True, db_column='venta_detalle_id')
    venta_id = models.ForeignKey(Ventas, to_field='venta_id', on_delete=models.PROTECT, db_column='venta_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')

    tipo_montura_id = models.IntegerField(blank=False, null=False, default=0)
    material_id = models.IntegerField(blank=False, null=False, default=0)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = 'ventas_detalles'


class VentasImagenes(models.Model):
    venta_imagen_id = models.AutoField(primary_key=True, db_column='venta_imagen_id')
    venta_id = models.ForeignKey(Ventas, to_field='venta_id', on_delete=models.PROTECT, db_column='venta_id')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')

    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'ventas_imagenes'


class Dosificaciones(models.Model):
    dosificacion_id = models.AutoField(primary_key=True, db_column='dosificacion_id')
    sucursal_id = models.ForeignKey(Sucursales, to_field='sucursal_id', on_delete=models.PROTECT, db_column='sucursal_id')
    dosificacion = models.CharField(max_length=250, null=False, blank=False)
    fecha_inicio = DateFieldCustome(null=True, blank=True)
    fecha_fin = DateFieldCustome(null=True, blank=True)
    numero_autorizacion = models.CharField(max_length=250, blank=False, null=False)
    llave = models.CharField(max_length=250, blank=False, null=False)
    numero_actual = models.IntegerField(blank=False, null=False)

    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'dosificaciones'


class Facturas(models.Model):
    factura_id = models.AutoField(primary_key=True, db_column='factura_id')
    venta_id = models.ForeignKey(Ventas, to_field='venta_id', on_delete=models.PROTECT, db_column='venta_id')
    dosificacion_id = models.ForeignKey(Dosificaciones, to_field='dosificacion_id', on_delete=models.PROTECT, db_column='dosificacion_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    caja_id = models.ForeignKey(Cajas, to_field='caja_id', on_delete=models.PROTECT, db_column='caja_id')
    cliente_id = models.ForeignKey(Clientes, to_field='cliente_id', on_delete=models.PROTECT, db_column='cliente_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    apellidos = models.CharField(max_length=150, blank=False, null=False)
    nombres = models.CharField(max_length=150, blank=False, null=False)
    ci_nit = models.CharField(max_length=150, blank=False, null=False)
    telefonos = models.CharField(max_length=150, blank=False, null=False)
    nit = models.CharField(max_length=150, blank=False, null=False)
    factura_a = models.CharField(max_length=250, blank=False, null=False)
    numero_factura = models.IntegerField(blank=False, null=False)

    numero_autorizacion = models.CharField(max_length=250, blank=False, null=False)
    llave = models.CharField(max_length=250, blank=False, null=False)
    codigo_control = models.CharField(max_length=250, blank=False, null=False)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    fecha = DateTimeFieldCustome(null=True, blank=True)

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'facturas'
        unique_together = ('dosificacion_id', 'numero_factura',)


class PlanPagos(models.Model):
    plan_pago_id = models.AutoField(primary_key=True, db_column='plan_pago_id')
    venta_id = models.ForeignKey(Ventas, to_field='venta_id', on_delete=models.PROTECT, db_column='venta_id')
    cliente_id = models.IntegerField(blank=False, null=False, default=0)
    punto_id = models.IntegerField(blank=False, null=False, default=0)

    fecha = DateTimeFieldCustome(null=True, blank=True)
    concepto = models.CharField(max_length=250, blank=False, null=False)
    numero_cuotas = models.IntegerField(blank=False, null=False, default=1)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cuota_inicial = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    mensual_dias = models.CharField(max_length=20, blank=False, null=False)
    dia_mensual = models.IntegerField(blank=False, null=False, default=1)
    tiempo_dias = models.IntegerField(blank=False, null=False, default=1)

    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'plan_pagos'


class PlanPagosDetalles(models.Model):
    plan_pago_detalle_id = models.AutoField(primary_key=True, db_column='plan_pago_detalle_id')
    plan_pago_id = models.ForeignKey(PlanPagos, to_field='plan_pago_id', on_delete=models.PROTECT, db_column='plan_pago_id')
    numero_cuota = models.IntegerField(blank=False, null=False, default=1)
    fecha = DateTimeFieldCustome(null=True, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'plan_pagos_detalles'


class PlanPagosPagos(models.Model):
    plan_pago_pago_id = models.AutoField(primary_key=True, db_column='plan_pago_pago_id')
    plan_pago_id = models.ForeignKey(PlanPagos, to_field='plan_pago_id', on_delete=models.PROTECT, db_column='plan_pago_id')

    numero_cuota = models.IntegerField(blank=False, null=False, default=1)
    fecha = DateTimeFieldCustome(null=True, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_paga = models.IntegerField(blank=False, null=False, default=0)
    cliente_id_paga = models.IntegerField(blank=False, null=False, default=0)
    persona_paga = models.CharField(max_length=250, blank=False, null=False)

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'plan_pagos_pagos'
