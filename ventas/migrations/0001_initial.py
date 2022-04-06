# Generated by Django 4.0.2 on 2022-03-07 15:05

from django.db import migrations, models
import django.db.models.deletion
import utils.custome_db_types


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dosificaciones',
            fields=[
                ('dosificacion_id', models.AutoField(db_column='dosificacion_id', primary_key=True, serialize=False)),
                ('dosificacion', models.CharField(max_length=250)),
                ('fecha_inicio', utils.custome_db_types.DateFieldCustome(blank=True, null=True)),
                ('fecha_fin', utils.custome_db_types.DateFieldCustome(blank=True, null=True)),
                ('numero_autorizacion', models.CharField(max_length=250)),
                ('llave', models.CharField(max_length=250)),
                ('numero_actual', models.IntegerField()),
                ('user_perfil_id_anula', models.IntegerField(blank=True, null=True)),
                ('motivo_anula', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('sucursal_id', models.ForeignKey(db_column='sucursal_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.sucursales')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'dosificaciones',
            },
        ),
        migrations.CreateModel(
            name='PlanPagos',
            fields=[
                ('plan_pago_id', models.AutoField(db_column='plan_pago_id', primary_key=True, serialize=False)),
                ('cliente_id', models.IntegerField(default=0)),
                ('punto_id', models.IntegerField(default=0)),
                ('fecha', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('concepto', models.CharField(max_length=250)),
                ('numero_cuotas', models.IntegerField(default=1)),
                ('monto_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cuota_inicial', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('saldo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('mensual_dias', models.CharField(max_length=20)),
                ('dia_mensual', models.IntegerField(default=1)),
                ('tiempo_dias', models.IntegerField(default=1)),
                ('user_perfil_id_anula', models.IntegerField(blank=True, null=True)),
                ('motivo_anula', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'plan_pagos',
            },
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('venta_id', models.AutoField(db_column='venta_id', primary_key=True, serialize=False)),
                ('fecha_preventa', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('user_perfil_id_venta', models.IntegerField(default=0)),
                ('fecha_venta', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('user_perfil_id_finaliza', models.IntegerField(default=0)),
                ('fecha_finaliza', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('cupon_id', models.IntegerField(default=0)),
                ('cupon', models.CharField(default='', max_length=50)),
                ('caja_id', models.IntegerField(default=0)),
                ('laboratorio_id', models.IntegerField(default=0)),
                ('tecnico_id', models.IntegerField(default=0)),
                ('oftalmologo_id', models.IntegerField(default=0)),
                ('stock_id', models.IntegerField(default=0)),
                ('nombres', models.CharField(max_length=150)),
                ('apellidos', models.CharField(max_length=150)),
                ('ci_nit', models.CharField(max_length=150)),
                ('telefonos', models.CharField(max_length=150)),
                ('direccion', models.CharField(max_length=250)),
                ('factura_a', models.CharField(max_length=250)),
                ('lejos_od_esf', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('lejos_od_cli', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('lejos_od_eje', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('lejos_oi_esf', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('lejos_oi_cli', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('lejos_oi_eje', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('lejos_di', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cerca_od_esf', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cerca_od_cli', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cerca_od_eje', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cerca_oi_esf', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cerca_oi_cli', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cerca_oi_eje', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cerca_di', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('tipo_venta', models.CharField(max_length=50)),
                ('plan_pago', models.IntegerField(default=0)),
                ('numero_venta', models.IntegerField(default=0)),
                ('precio_montura', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('precio_material', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('porcentaje_descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('a_cuenta', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('saldo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('nota', models.CharField(max_length=250)),
                ('user_perfil_id_anula', models.IntegerField(blank=True, null=True)),
                ('motivo_anula', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('almacen_id', models.ForeignKey(db_column='almacen_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.almacenes')),
                ('cliente_id', models.ForeignKey(db_column='cliente_id', on_delete=django.db.models.deletion.PROTECT, to='clientes.clientes')),
                ('punto_id', models.ForeignKey(db_column='punto_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.puntos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('user_perfil_id_preventa', models.ForeignKey(db_column='user_perfil_id_preventa', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'ventas',
            },
        ),
        migrations.CreateModel(
            name='VentasImagenes',
            fields=[
                ('venta_imagen_id', models.AutoField(db_column='venta_imagen_id', primary_key=True, serialize=False)),
                ('imagen', models.CharField(default='', max_length=250, unique=True)),
                ('imagen_thumb', models.CharField(default='', max_length=250, unique=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('venta_id', models.ForeignKey(db_column='venta_id', on_delete=django.db.models.deletion.PROTECT, to='ventas.ventas')),
            ],
            options={
                'db_table': 'ventas_imagenes',
            },
        ),
        migrations.CreateModel(
            name='VentasDetalles',
            fields=[
                ('venta_detalle_id', models.AutoField(db_column='venta_detalle_id', primary_key=True, serialize=False)),
                ('tipo_montura_id', models.IntegerField(default=0)),
                ('material_id', models.IntegerField(default=0)),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('costo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('porcentaje_descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('punto_id', models.ForeignKey(db_column='punto_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.puntos')),
                ('venta_id', models.ForeignKey(db_column='venta_id', on_delete=django.db.models.deletion.PROTECT, to='ventas.ventas')),
            ],
            options={
                'db_table': 'ventas_detalles',
            },
        ),
        migrations.CreateModel(
            name='PlanPagosPagos',
            fields=[
                ('plan_pago_pago_id', models.AutoField(db_column='plan_pago_pago_id', primary_key=True, serialize=False)),
                ('numero_cuota', models.IntegerField(default=1)),
                ('fecha', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('saldo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('user_perfil_id_paga', models.IntegerField(default=0)),
                ('cliente_id_paga', models.IntegerField(default=0)),
                ('persona_paga', models.CharField(max_length=250)),
                ('user_perfil_id_anula', models.IntegerField(blank=True, null=True)),
                ('motivo_anula', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('plan_pago_id', models.ForeignKey(db_column='plan_pago_id', on_delete=django.db.models.deletion.PROTECT, to='ventas.planpagos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'plan_pagos_pagos',
            },
        ),
        migrations.CreateModel(
            name='PlanPagosDetalles',
            fields=[
                ('plan_pago_detalle_id', models.AutoField(db_column='plan_pago_detalle_id', primary_key=True, serialize=False)),
                ('numero_cuota', models.IntegerField(default=1)),
                ('fecha', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('saldo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('user_perfil_id_anula', models.IntegerField(blank=True, null=True)),
                ('motivo_anula', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('plan_pago_id', models.ForeignKey(db_column='plan_pago_id', on_delete=django.db.models.deletion.PROTECT, to='ventas.planpagos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'plan_pagos_detalles',
            },
        ),
        migrations.AddField(
            model_name='planpagos',
            name='venta_id',
            field=models.ForeignKey(db_column='venta_id', on_delete=django.db.models.deletion.PROTECT, to='ventas.ventas'),
        ),
        migrations.CreateModel(
            name='Facturas',
            fields=[
                ('factura_id', models.AutoField(db_column='factura_id', primary_key=True, serialize=False)),
                ('apellidos', models.CharField(max_length=150)),
                ('nombres', models.CharField(max_length=150)),
                ('ci_nit', models.CharField(max_length=150)),
                ('telefonos', models.CharField(max_length=150)),
                ('nit', models.CharField(max_length=150)),
                ('factura_a', models.CharField(max_length=250)),
                ('numero_factura', models.IntegerField()),
                ('numero_autorizacion', models.CharField(max_length=250)),
                ('llave', models.CharField(max_length=250)),
                ('codigo_control', models.CharField(max_length=250)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('porcentaje_descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('fecha', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('user_perfil_id_anula', models.IntegerField(blank=True, null=True)),
                ('motivo_anula', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('caja_id', models.ForeignKey(db_column='caja_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.cajas')),
                ('cliente_id', models.ForeignKey(db_column='cliente_id', on_delete=django.db.models.deletion.PROTECT, to='clientes.clientes')),
                ('dosificacion_id', models.ForeignKey(db_column='dosificacion_id', on_delete=django.db.models.deletion.PROTECT, to='ventas.dosificaciones')),
                ('punto_id', models.ForeignKey(db_column='punto_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.puntos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
                ('venta_id', models.ForeignKey(db_column='venta_id', on_delete=django.db.models.deletion.PROTECT, to='ventas.ventas')),
            ],
            options={
                'db_table': 'facturas',
                'unique_together': {('dosificacion_id', 'numero_factura')},
            },
        ),
    ]
