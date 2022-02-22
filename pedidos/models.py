from django.db import models
from django.conf import settings

from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome
from productos.models import Productos


class Pedidos(models.Model):
    pedido_id = models.AutoField(primary_key=True, db_column='pedido_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    cliente_id = models.IntegerField(blank=False, null=False, default=0)
    venta_id = models.IntegerField(blank=False, null=False, default=0)
    ci_nit = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=250, blank=False, null=False)
    nombres = models.CharField(max_length=250, blank=False, null=False)
    telefonos = models.CharField(max_length=250, blank=False, null=False)
    direccion = models.CharField(max_length=250, blank=False, null=False)
    email = models.CharField(max_length=250, blank=False, null=False)
    mensaje = models.TextField(null=False, blank=False)
    tipo_pedido = models.CharField(max_length=50, blank=False, null=False)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    cupon_id = models.IntegerField(blank=False, null=False, default=0)
    cupon = models.CharField(max_length=150, blank=False, null=False)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    user_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, blank=True, null=True)

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'pedidos'


class PedidosDetalles(models.Model):
    pedido_detalle_id = models.AutoField(primary_key=True, db_column='pedido_detalle_id')
    pedido_id = models.ForeignKey(Pedidos, to_field='pedido_id', on_delete=models.PROTECT, db_column='pedido_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    producto_id = models.ForeignKey(Productos, to_field='producto_id', on_delete=models.PROTECT, db_column='producto_id')

    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)

    class Meta:
        db_table = 'pedidos_detalles'
