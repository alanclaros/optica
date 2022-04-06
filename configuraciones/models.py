from pyexpat import model
from django.db import models

from status.models import Status
from permisos.models import UsersPerfiles
from utils.custome_db_types import DateFieldCustome, DateTimeFieldCustome


class Configuraciones(models.Model):
    configuracion_id = models.IntegerField(primary_key=True)
    cant_per_page = models.IntegerField(blank=False, null=False)
    cant_productos_home = models.IntegerField(blank=False, null=False)
    usar_fecha_servidor = models.CharField(max_length=20, blank=False, null=False, default='si')
    fecha_sistema = DateFieldCustome(null=True, blank=True)
    numero_actual_venta = models.IntegerField(blank=False, null=False, default=0)

    # notificaciones laboratorio
    minutos_aviso_entregar = models.IntegerField(blank=False, null=False)
    minutos_aviso_entregar_tarde = models.IntegerField(blank=False, null=False)

    # recoger laboratorio
    minutos_aviso_recoger = models.IntegerField(blank=False, null=False)
    minutos_aviso_recoger_tarde = models.IntegerField(blank=False, null=False)

    # entrega de lentes
    minutos_aviso_finalizar = models.IntegerField(blank=False, null=False)
    minutos_aviso_finalizar_tarde = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = 'configuraciones'


class Paises(models.Model):
    pais_id = models.IntegerField(primary_key=True, db_column='pais_id')
    pais = models.CharField(max_length=150, blank=False)

    class Meta:
        db_table = 'paises'


class Ciudades(models.Model):
    ciudad_id = models.AutoField(primary_key=True, db_column='ciudad_id')
    pais_id = models.ForeignKey(Paises, to_field='pais_id', on_delete=models.PROTECT, db_column='pais_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    ciudad = models.CharField(max_length=150, blank=False)
    codigo = models.CharField(max_length=50, blank=False)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'ciudades'


class Sucursales(models.Model):
    sucursal_id = models.AutoField(primary_key=True, db_column='sucursal_id')
    ciudad_id = models.ForeignKey(Ciudades, to_field='ciudad_id', on_delete=models.PROTECT, db_column='ciudad_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    sucursal = models.CharField(max_length=250, blank=False)
    codigo = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=250, blank=False)
    empresa = models.CharField(max_length=250, blank=False)
    direccion = models.CharField(max_length=250, blank=False)
    ciudad = models.CharField(max_length=250, blank=False)
    telefonos = models.CharField(max_length=250, blank=False)
    actividad = models.CharField(max_length=250, blank=False)

    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'sucursales'


class Puntos(models.Model):
    punto_id = models.AutoField(primary_key=True, db_column='punto_id')
    sucursal_id = models.ForeignKey(Sucursales, to_field='sucursal_id', on_delete=models.PROTECT, db_column='sucursal_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    punto = models.CharField(max_length=150, blank=False)
    codigo = models.CharField(max_length=50, blank=False)
    impresora_reportes = models.CharField(max_length=250, blank=False)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'puntos'


class TiposMonedas(models.Model):
    tipo_moneda_id = models.IntegerField(primary_key=True, db_column='tipo_moneda_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    tipo_moneda = models.CharField(max_length=150, blank=False)
    codigo = models.CharField(max_length=50, blank=False)

    class Meta:
        db_table = 'tipos_monedas'


class Monedas(models.Model):
    moneda_id = models.IntegerField(primary_key=True, db_column='moneda_id')
    tipo_moneda_id = models.ForeignKey(TiposMonedas, to_field='tipo_moneda_id', on_delete=models.PROTECT, db_column='tipo_moneda_id')
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')

    class Meta:
        db_table = 'monedas'


class Cajas(models.Model):
    caja_id = models.AutoField(primary_key=True, db_column='caja_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    tipo_moneda_id = models.ForeignKey(TiposMonedas, to_field='tipo_moneda_id', on_delete=models.PROTECT, db_column='tipo_moneda_id')
    user_perfil_id = models.ForeignKey(UsersPerfiles, to_field='user_perfil_id', on_delete=models.PROTECT, db_column='user_perfil_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    caja = models.CharField(max_length=150, blank=False)
    codigo = models.CharField(max_length=50, blank=False)
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'cajas'


class Almacenes(models.Model):
    almacen_id = models.AutoField(primary_key=True, db_column='almacen_id')
    almacen = models.CharField(max_length=150, blank=False, null=False, default='')
    codigo = models.CharField(max_length=20, blank=False, null=False, default='')
    sucursal_id = models.ForeignKey(Sucursales, to_field='sucursal_id', on_delete=models.PROTECT, db_column='sucursal_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'almacenes'


class Lineas(models.Model):
    linea_id = models.AutoField(primary_key=True, db_column='linea_id')
    linea = models.CharField(max_length=150, blank=False, null=False, default='')
    codigo = models.CharField(max_length=150, blank=False, null=False, default='')
    posicion = models.IntegerField(null=False, blank=False, default=1)
    linea_principal = models.IntegerField(blank=False, null=False, default=0)
    linea_superior_id = models.IntegerField(blank=False, null=False, default=0)
    descripcion = models.CharField(max_length=250, blank=False, null=False, default='')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'lineas'


class PuntosAlmacenes(models.Model):
    punto_almacen_id = models.AutoField(primary_key=True, db_column='punto_almacen_id')
    punto_id = models.ForeignKey(Puntos, to_field='punto_id', on_delete=models.PROTECT, db_column='punto_id')
    almacen_id = models.ForeignKey(Almacenes, to_field='almacen_id', on_delete=models.PROTECT, db_column='almacen_id')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = 'puntos_almacenes'


class Proveedores(models.Model):
    proveedor_id = models.AutoField(primary_key=True, db_column='proveedor_id')
    proveedor = models.CharField(max_length=150, blank=False, null=False, default='')
    codigo = models.CharField(max_length=50, blank=False, null=False, default='')
    descripcion = models.CharField(max_length=250, blank=False, null=False, default='')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = "proveedores"


class Materiales(models.Model):
    material_id = models.AutoField(primary_key=True, db_column='material_id')
    proveedor_id = models.ForeignKey(Proveedores, to_field='proveedor_id', on_delete=models.PROTECT, db_column='proveedor_id')
    material = models.CharField(max_length=150, blank=False, null=False, default='')
    codigo = models.CharField(max_length=150, blank=False, null=False, default='')
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descripcion = models.CharField(max_length=250, blank=False, null=False, default='')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = "materiales"


class TiposMontura(models.Model):
    tipo_montura_id = models.AutoField(primary_key=True, db_column='tipo_montura_id')
    proveedor_id = models.ForeignKey(Proveedores, to_field='proveedor_id', on_delete=models.PROTECT, db_column='proveedor_id')
    tipo_montura = models.CharField(max_length=150, blank=False, null=False, default='')
    codigo = models.CharField(max_length=150, blank=False, null=False, default='')
    costo = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0)
    descripcion = models.CharField(max_length=250, blank=False, null=False, default='')
    numero_actual = models.IntegerField(blank=False, null=False, default=0)
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = "tipos_montura"


class Laboratorios(models.Model):
    laboratorio_id = models.AutoField(primary_key=True, db_column='laboratorio_id')
    laboratorio = models.CharField(max_length=150, blank=False, null=False, default='')
    codigo = models.CharField(max_length=50, blank=False, null=False, default='')
    descripcion = models.CharField(max_length=250, blank=False, null=False, default='')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = "laboratorios"


class Tecnicos(models.Model):
    tecnico_id = models.AutoField(primary_key=True, db_column='tecnico_id')
    tecnico = models.CharField(max_length=150, blank=False, null=False, default='')
    codigo = models.CharField(max_length=50, blank=False, null=False, default='')
    descripcion = models.CharField(max_length=250, blank=False, null=False, default='')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = "tecnicos"


class Oftalmologos(models.Model):
    oftalmologo_id = models.AutoField(primary_key=True, db_column='oftalmologo_id')
    oftalmologo = models.CharField(max_length=150, blank=False, null=False, default='')
    codigo = models.CharField(max_length=50, blank=False, null=False, default='')
    descripcion = models.CharField(max_length=250, blank=False, null=False, default='')
    imagen = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    imagen_thumb = models.CharField(max_length=250, unique=True, null=False, blank=False, default='')
    status_id = models.ForeignKey(Status, to_field='status_id', on_delete=models.PROTECT, db_column='status_id')
    created_at = DateTimeFieldCustome(null=True, blank=True)
    updated_at = DateTimeFieldCustome(null=True, blank=True)
    deleted_at = DateTimeFieldCustome(null=True, blank=True)

    class Meta:
        db_table = "oftalmologos"


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
