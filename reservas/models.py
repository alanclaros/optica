from django.db import models
from django.conf import settings

from status.models import Status
from utils.custome_db_types import DateTimeFieldCustome


class ReservasDias(models.Model):
    reserva_dia_id = models.AutoField(primary_key=True, db_column='reserva_dia_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    dia = models.CharField(max_length=50, blank=False, null=False)
    posicion = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = 'reservas_dias'


class ReservasHoras(models.Model):
    reserva_hora_id = models.AutoField(primary_key=True, db_column='reserva_hora_id')
    reserva_dia_id = models.ForeignKey(ReservasDias, to_field='reserva_dia_id', on_delete=models.PROTECT, db_column='reserva_dia_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    hora = models.CharField(max_length=50, blank=False, null=False)
    posicion = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = 'reservas_horas'


class Reservas(models.Model):
    reserva_id = models.AutoField(primary_key=True, db_column='reserva_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    reserva_dia_id = models.ForeignKey(ReservasDias, to_field='reserva_dia_id', on_delete=models.PROTECT, db_column='reserva_dia_id')
    reserva_hora_id = models.ForeignKey(ReservasHoras, to_field='reserva_hora_id', on_delete=models.PROTECT, db_column='reserva_hora_id')

    cliente_id = models.IntegerField(blank=False, null=False, default=0)
    ci_nit = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=250, blank=False, null=False)
    nombres = models.CharField(max_length=250, blank=False, null=False)
    telefonos = models.CharField(max_length=250, blank=False, null=False)
    direccion = models.CharField(max_length=250, blank=False, null=False)
    email = models.CharField(max_length=250, blank=False, null=False)
    mensaje = models.TextField(null=False, blank=False)

    fecha_inicio = DateTimeFieldCustome(null=True, blank=True)
    fecha_fin = DateTimeFieldCustome(null=True, blank=True)

    user_perfil_id_anula = models.IntegerField(blank=True, null=True)
    motivo_anula = models.CharField(max_length=250, blank=True, null=True)

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'reservas'
