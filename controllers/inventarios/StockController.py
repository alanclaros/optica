from productos.models import Productos
from inventarios.models import Stock
from configuraciones.models import Almacenes

from controllers.DefaultValues import DefaultValues

from django.db import transaction
from django.apps import apps


class StockController(DefaultValues):
    def __init__(self):
        DefaultValues.__init__(self)

        self.table_name = 'registros'
        self.table_id = 'registro_id'

    def add_stock(self, user_perfil, almacen, tipo_montura, numero, cantidad):
        """actualizamos el stock"""
        try:
            with transaction.atomic():
                # productos normales
                stock_filter = Stock.objects.filter(almacen_id=almacen, tipo_montura_id=tipo_montura, numero_montura=numero)
                stock = stock_filter.first()
                if not stock:
                    # creamos el registro
                    stock = Stock.objects.create(almacen_id=almacen, tipo_montura_id=tipo_montura, numero_montura=numero, cantidad=cantidad, vendida=0,
                                                 user_perfil_id=user_perfil, status_id=self.status_activo, created_at='now', updated_at='now')
                stock.save()

            return True

        except Exception as ex:
            print('Error add stock: ' + str(ex))
            self.error_operation = 'Error al aniadir stock, ' + str(ex)
            #raise ValueError('Error al aniadir stock, ' + str(ex))

    def stock_producto(self, tipo_montura_id, almacen_id, numero):
        """devuelve el stock del producto"""
        try:
            almacen = Almacenes.objects.get(pk=almacen_id)
            tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=tipo_montura_id)

            stock_almacen = Stock.objects.get(almacen_id=almacen, tipo_montura_id=tipo_montura, numero_montura=numero)
            if stock_almacen:
                return stock_almacen.vendida

        except Exception as ex:
            self.error_operation = 'no existe stock del producto, ' + str(ex)
            return -1
            #raise ValueError('Error al recuperar stock del producto, ' + str(ex))

    def get_stock_montura(self, tipo_montura_id, almacen_id, vendidas=0):
        try:
            almacen = Almacenes.objects.get(pk=almacen_id)
            tipo_montura = apps.get_model('configuraciones', 'TiposMontura').objects.get(pk=tipo_montura_id)

            lista_stock = apps.get_model('inventarios', 'Stock').objects.filter(almacen_id=almacen, tipo_montura_id=tipo_montura, vendida=vendidas, status_id=self.status_activo).order_by('numero_montura')

            return lista_stock

        except Exception as ex:
            self.error_operation = 'error al recuperar stock de montura, ' + str(ex)
            return []
