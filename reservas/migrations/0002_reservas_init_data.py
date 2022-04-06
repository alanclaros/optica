from django.db import migrations
from reservas.models import ReservasDias, ReservasHoras
from status.models import Status


def load_data(apps, schema_editor):
    # configuraciones
    status_activo = Status.objects.get(pk=1)

    # dias
    reserva_dia = ReservasDias.objects.create(status_id=status_activo, dia='Lunes', posicion=1)
    reserva_dia.save()
    reserva_dia = ReservasDias.objects.create(status_id=status_activo, dia='Martes', posicion=2)
    reserva_dia.save()
    reserva_dia = ReservasDias.objects.create(status_id=status_activo, dia='Miercoles', posicion=3)
    reserva_dia.save()
    reserva_dia = ReservasDias.objects.create(status_id=status_activo, dia='Jueves', posicion=4)
    reserva_dia.save()
    reserva_dia = ReservasDias.objects.create(status_id=status_activo, dia='Viernes', posicion=5)
    reserva_dia.save()
    reserva_dia = ReservasDias.objects.create(status_id=status_activo, dia='Sabado', posicion=6)
    reserva_dia.save()
    reserva_dia = ReservasDias.objects.create(status_id=status_activo, dia='Domingo', posicion=7)
    reserva_dia.save()

    lunes = ReservasDias.objects.get(pk=1)
    martes = ReservasDias.objects.get(pk=2)
    miercoles = ReservasDias.objects.get(pk=3)
    jueves = ReservasDias.objects.get(pk=4)
    viernes = ReservasDias.objects.get(pk=5)
    sabado = ReservasDias.objects.get(pk=6)
    domingo = ReservasDias.objects.get(pk=7)

    # horas lunes
    horarios = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
                '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00']

    # lunes
    posicion = 1
    for hora in horarios:
        hora_add = ReservasHoras.objects.create(reserva_dia_id=lunes, status_id=status_activo, posicion=posicion, hora=hora)
        hora_add.save()
        posicion += 1

    # martes
    posicion = 1
    for hora in horarios:
        hora_add = ReservasHoras.objects.create(reserva_dia_id=martes, status_id=status_activo, posicion=posicion, hora=hora)
        hora_add.save()
        posicion += 1

    # miercoles
    posicion = 1
    for hora in horarios:
        hora_add = ReservasHoras.objects.create(reserva_dia_id=miercoles, status_id=status_activo, posicion=posicion, hora=hora)
        hora_add.save()
        posicion += 1

    # jueves
    posicion = 1
    for hora in horarios:
        hora_add = ReservasHoras.objects.create(reserva_dia_id=jueves, status_id=status_activo, posicion=posicion, hora=hora)
        hora_add.save()
        posicion += 1

    # viernes
    posicion = 1
    for hora in horarios:
        hora_add = ReservasHoras.objects.create(reserva_dia_id=viernes, status_id=status_activo, posicion=posicion, hora=hora)
        hora_add.save()
        posicion += 1

    horarios = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
                '14:30', '15:00']
    # sabado
    posicion = 1
    for hora in horarios:
        hora_add = ReservasHoras.objects.create(reserva_dia_id=sabado, status_id=status_activo, posicion=posicion, hora=hora)
        hora_add.save()
        posicion += 1

    # domingo
    posicion = 1
    for hora in horarios:
        hora_add = ReservasHoras.objects.create(reserva_dia_id=domingo, status_id=status_activo, posicion=posicion, hora=hora)
        hora_add.save()
        posicion += 1


def delete_data(apps, schema_editor):
    horas_del = apps.get_model('reservas', 'ReservasHoras')
    horas_del.objects.all().delete

    dias_del = apps.get_model('reservas', 'ReservasDias')
    dias_del.objects.all().delete


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data, delete_data),
    ]
