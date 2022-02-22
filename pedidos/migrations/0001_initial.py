# Generated by Django 4.0.2 on 2022-02-22 12:06

from django.db import migrations, models
import django.db.models.deletion
import utils.custome_db_types


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('pedido_id', models.AutoField(db_column='pedido_id', primary_key=True, serialize=False)),
                ('cliente_id', models.IntegerField(default=0)),
                ('venta_id', models.IntegerField(default=0)),
                ('ci_nit', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=250)),
                ('nombres', models.CharField(max_length=250)),
                ('telefonos', models.CharField(max_length=250)),
                ('direccion', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('mensaje', models.TextField()),
                ('tipo_pedido', models.CharField(max_length=50)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cupon_id', models.IntegerField(default=0)),
                ('cupon', models.CharField(max_length=150)),
                ('porcentaje_descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('user_id_anula', models.IntegerField(blank=True, null=True)),
                ('motivo_anula', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'pedidos',
            },
        ),
        migrations.CreateModel(
            name='PedidosDetalles',
            fields=[
                ('pedido_detalle_id', models.AutoField(db_column='pedido_detalle_id', primary_key=True, serialize=False)),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('costo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('porcentaje_descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('pedido_id', models.ForeignKey(db_column='pedido_id', on_delete=django.db.models.deletion.PROTECT, to='pedidos.pedidos')),
                ('producto_id', models.ForeignKey(db_column='producto_id', on_delete=django.db.models.deletion.PROTECT, to='productos.productos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'pedidos_detalles',
            },
        ),
    ]
