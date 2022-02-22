from django.db import models
from django.conf import settings

from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome, DateFieldCustome
from configuraciones.models import Puntos, Almacenes, Cajas, Sucursales
from clientes.models import Clientes
from productos.models import Productos


class Cupones(models.Model):
    cupon_id = models.AutoField(primary_key=True, db_column='cupon_id')
    cupon = models.CharField(max_length=150, null=False, blank=False, default='', db_column='cupon')
    numero_usos = models.IntegerField(null=False, blank=False, default=1)
    numero_actual_uso = models.IntegerField(null=False, blank=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'cupones'


class Ventas(models.Model):
    venta_id = models.AutoField(primary_key=True, db_column='venta_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    caja_id = models.ForeignKey(Cajas, to_field='caja_id', on_delete=models.PROTECT, db_column='caja_id')
    almacen_id = models.ForeignKey(Almacenes, to_field='almacen_id', on_delete=models.PROTECT, db_column='almacen_id')
    cliente_id = models.ForeignKey(Clientes, to_field='cliente_id', on_delete=models.PROTECT, db_column='cliente_id')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.PROTECT, db_column='user_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    cupon_id = models.IntegerField(null=False, blank=False, default=0)
    cupon = models.CharField(max_length=150, null=False, blank=False, default='')

    apellidos = models.CharField(max_length=150, blank=False, null=False)
    nombres = models.CharField(max_length=150, blank=False, null=False)
    ci_nit = models.CharField(max_length=150, blank=False, null=False)
    telefonos = models.CharField(max_length=150, blank=False, null=False)

    tipo_venta = models.CharField(max_length=50, blank=False, null=False)
    numero_venta = models.IntegerField(blank=False, null=False, default=0)

    fecha = DateTimeFieldCustome(null=True, blank=True)
    user_id_fecha = models.IntegerField(blank=False, null=False, default=0)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    concepto = models.CharField(max_length=250, blank=False, null=False)

    user_id_anula = models.IntegerField(blank=True, null=True)
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

    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = 'ventas_detalles'


class Dosificaciones(models.Model):
    dosificacion_id = models.AutoField(primary_key=True, db_column='dosificacion_id')
    sucursal_id = models.ForeignKey(Sucursales, to_field='sucursal_id', on_delete=models.PROTECT, db_column='sucursal_id')
    dosificacion = models.CharField(max_length=250, null=False, blank=False)
    fecha_inicio = DateFieldCustome(null=True, blank=True)
    fecha_fin = DateFieldCustome(null=True, blank=True)
    numero_autorizacion = models.CharField(max_length=250, blank=False, null=False)
    llave = models.CharField(max_length=250, blank=False, null=False)
    numero_actual = models.IntegerField(blank=False, null=False)

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.PROTECT, db_column='user_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_id_anula = models.IntegerField(blank=True, null=True)
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
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.PROTECT, db_column='user_id')
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

    user_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'facturas'
        unique_together = ('dosificacion_id', 'numero_factura',)
