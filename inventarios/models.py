from django.db import models

from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome
from configuraciones.models import Puntos, Almacenes, TiposMontura
from permisos.models import UsersPerfiles


class Registros(models.Model):
    registro_id = models.AutoField(primary_key=True, db_column='registro_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    almacen_id = models.ForeignKey(Almacenes, to_field='almacen_id', on_delete=models.PROTECT, db_column='almacen_id')
    tipo_montura_id = models.ForeignKey(TiposMontura, to_field='tipo_montura_id', on_delete=models.PROTECT, db_column='tipo_montura_id')
    almacen2_id = models.IntegerField(blank=False, null=False, default=0)
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    tipo_movimiento = models.CharField(max_length=50, blank=False, null=False)
    numero_registro = models.IntegerField(blank=False, null=False, default=0)
    cantidad_monturas = models.IntegerField(blank=False, null=False, default=1)
    fecha = DateTimeFieldCustome(null=True, blank=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    concepto = models.CharField(max_length=250, blank=False, null=False)
    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'registros'


class RegistrosDetalles(models.Model):
    registro_detalle_id = models.AutoField(primary_key=True, db_column='registro_detalle_id')
    registro_id = models.ForeignKey(Registros, to_field='registro_id', on_delete=models.PROTECT, db_column='registro_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')

    tipo_montura_id = models.ForeignKey(TiposMontura, to_field='tipo_montura_id', on_delete=models.PROTECT, db_column='tipo_montura_id')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    numero_montura = models.IntegerField(blank=False, null=False, default=0)
    nombre_montura = models.CharField(max_length=250, null=False, blank=False, default='')
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = 'registros_detalles'


class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True, db_column='stock_id')
    almacen_id = models.ForeignKey(Almacenes, to_field='almacen_id', on_delete=models.PROTECT, db_column='almacen_id')
    tipo_montura_id = models.ForeignKey(TiposMontura, to_field='tipo_montura_id', on_delete=models.PROTECT, db_column='tipo_montura_id')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    numero_montura = models.IntegerField(blank=False, null=False, default=0)
    nombre_montura = models.CharField(max_length=250, null=False, blank=False, default='')
    vendida = models.IntegerField(blank=False, null=False, default=0)

    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, null=True, blank=True)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'stock'
