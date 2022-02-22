# Generated by Django 4.0.2 on 2022-02-17 15:59

from django.db import migrations, models
import django.db.models.deletion
import utils.custome_db_types


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cajas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('producto_id', models.AutoField(db_column='producto_id', primary_key=True, serialize=False)),
                ('producto', models.CharField(max_length=250, unique=True)),
                ('codigo', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('stock_minimo', models.IntegerField(default=0)),
                ('descripcion1', models.CharField(max_length=250)),
                ('descripcion2', models.CharField(max_length=250)),
                ('descripcion3', models.CharField(max_length=250)),
                ('descripcion4', models.CharField(max_length=250)),
                ('descripcion5', models.CharField(max_length=250)),
                ('descripcion6', models.CharField(max_length=250)),
                ('descripcion7', models.CharField(max_length=250)),
                ('descripcion8', models.CharField(max_length=250)),
                ('descripcion9', models.CharField(max_length=250)),
                ('descripcion10', models.CharField(max_length=250)),
                ('novedad', models.BooleanField(default=False)),
                ('mas_vendido', models.BooleanField(default=False)),
                ('oferta', models.BooleanField(default=False)),
                ('precio_oferta', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('color_id', models.ForeignKey(db_column='color_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.colores')),
                ('disenio_lente_id', models.ForeignKey(db_column='disenio_lente_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.diseniolentes')),
                ('linea_id', models.ForeignKey(db_column='linea_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.lineas')),
                ('marca_id', models.ForeignKey(db_column='marca_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.marcas')),
                ('material_id', models.ForeignKey(db_column='material_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.materiales')),
                ('proveedor_id', models.ForeignKey(db_column='proveedor_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.proveedores')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('tipo_montura_id', models.ForeignKey(db_column='tipo_montura_id', on_delete=django.db.models.deletion.PROTECT, to='configuraciones.tiposmontura')),
                ('user_perfil_id', models.ForeignKey(db_column='user_perfil_id', on_delete=django.db.models.deletion.PROTECT, to='permisos.usersperfiles')),
            ],
            options={
                'db_table': 'productos',
            },
        ),
        migrations.CreateModel(
            name='ProductosRelacionados',
            fields=[
                ('producto_relacionado_id', models.AutoField(db_column='producto_relacionado_id', primary_key=True, serialize=False)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('producto_id', models.ForeignKey(db_column='producto_id', on_delete=django.db.models.deletion.PROTECT, related_name='primer_prodr', to='productos.productos', verbose_name='prod1r')),
                ('producto_relacion_id', models.ForeignKey(db_column='producto_relacion_id', on_delete=django.db.models.deletion.PROTECT, related_name='segundo_prodr', to='productos.productos', verbose_name='prod2r')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'productos_relacionados',
            },
        ),
        migrations.CreateModel(
            name='ProductosImagenes',
            fields=[
                ('producto_imagen_id', models.AutoField(db_column='producto_imagen_id', primary_key=True, serialize=False)),
                ('imagen', models.CharField(default='', max_length=250, unique=True)),
                ('imagen_thumb', models.CharField(default='', max_length=250, unique=True)),
                ('posicion', models.IntegerField(default=1)),
                ('created_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('updated_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('deleted_at', utils.custome_db_types.DateTimeFieldCustome(blank=True, null=True)),
                ('producto_id', models.ForeignKey(db_column='producto_id', on_delete=django.db.models.deletion.PROTECT, to='productos.productos')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.PROTECT, to='status.status')),
            ],
            options={
                'db_table': 'productos_imagenes',
            },
        ),
    ]
