# Generated by Django 4.0.2 on 2022-02-10 16:47

from django.db import migrations

from configuraciones.models import Puntos
from status.models import Status
from clientes.models import Clientes
from permisos.models import UsersPerfiles


def load_data(apps, schema_editor):
    punto1 = Puntos.objects.get(pk=1)
    status_activo = Status.objects.get(pk=1)
    user_perfil = UsersPerfiles.objects.get(pk=1)

    cliente1 = Clientes.objects.create(nombres='', apellidos='SIN NOMBRE', razon_social='SIN NOMBRE', factura_a='SIN NOMBRE', ci_nit='0', telefonos='',
                                       direccion='', email='', notificar=0, created_at='now', updated_at='now', punto_id=punto1, user_perfil_id=user_perfil, status_id=status_activo)
    cliente1.save()


def delete_data(apps, schema_editor):
    clientes_lista = apps.get_model('clientes', 'Clientes')
    clientes_lista.objects.all().delete


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data, delete_data),
    ]
