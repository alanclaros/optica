
function sendSearchVenta() {
    sendFormObject('search', div_modulo);
}

function ventaWarning() {
    modalF.modal('toggle');
}

function sendFormVenta(operation, message) {
    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer adicionar esta Preventa?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('anular'):
            modalFunction.value = 'ventaSaveForm();';
            //set data modal
            modalSetParameters('danger', 'center', 'PreVentas!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
            modalF.modal();

            break;

        case ('pasar_venta'):
            resValidation = verifyPasarVenta();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer confirmar esta venta?', 'Cancelar', 'Confirmar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }

            break;

        case ('pasar_venta_anular'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular esta Venta?', 'Cancelar', 'Anular');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('gastos'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer adicionar este gasto?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('cobros'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer adicionar este cobro?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        case ('pasar_finalizado'):
            modalFunction.value = 'ventaSaveForm();';
            modalSetParameters('success', 'center', 'Ventas!', 'Esta seguro de querer finalizar esta venta?', 'Cancelar', 'Finalizar');
            modalF.modal();

            break;

        case ('pasar_finalizado_anular'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'ventaSaveForm();';
                modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular esta finalizacion?', 'Cancelar', 'Anular');
                modalF.modal();
            }
            else {
                modalSetParameters('warning', 'center', 'Ventas!', resValidation, 'Cancelar', 'Volver');
                modalFunction.value = 'ventaWarning();';
                modalF.modal();
            }
            break;

        default:
            break;
    }
}

function ventaSaveForm() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

//confirmar anular venta
function anularPreventa() {
    modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular esta preventa?', 'Cancelar', 'Anular');
    modalFunction.value = 'anularPreventaSend();';
    modalF.modal();
}

function anularPreventaSend() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function anularVenta() {
    motivo_an = Trim(document.getElementById('motivo_anula').value);
    if (motivo_an == '') {
        modalSetParameters('warning', 'center', 'Ventas!', 'Debe llenar el motivo', 'Cancelar', 'Volver');
        modalFunction.value = 'ventaWarning();';
        modalF.modal();
        return false;
    }

    modalSetParameters('danger', 'center', 'Ventas!', 'Esta seguro de querer anular esta venta?', 'Cancelar', 'Anular');
    modalFunction.value = 'anularVentaSend();';
    modalF.modal();
}

function anularVentaSend() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

//acc, buscar cliente
function buscarClienteVenta() {
    obj_telefonos = Trim(document.getElementById('buscar_telefonos').value);
    obj_apellidos = Trim(document.getElementById('buscar_apellidos').value);
    obj_nombres = Trim(document.getElementById('buscar_nombres').value);

    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

    const imagen = '<td colspan="4" class="left w100">' + imgLoading + '</td>';

    datos = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'buscar_cliente',
        'telefonos': obj_telefonos,
        'apellidos': obj_apellidos,
        'nombres': obj_nombres,
        'csrfmiddlewaretoken': token,
    }

    $("#div_clientes").fadeIn('slow');
    $("#div_clientes").html(imagen);
    $("#div_clientes").load(hostURL, datos, function () {
        //termina de cargar la ventana
    });
}

//acc, selecccionar cliente
function seleccionarClienteVenta(cliente_id) {
    obj_ci_nit = document.getElementById('ci_nit_' + cliente_id).value;
    obj_apellidos = document.getElementById('apellidos_' + cliente_id).value;
    obj_nombres = document.getElementById('nombres_' + cliente_id).value;
    obj_telefonos = document.getElementById('telefonos_' + cliente_id).value;
    obj_direccion = document.getElementById('direccion_' + cliente_id).value;
    obj_factura_a = document.getElementById('factura_a_' + cliente_id).value;

    p_ci_nit = document.getElementById('ci_nit');
    p_apellidos = document.getElementById('apellidos');
    p_nombres = document.getElementById('nombres');
    p_telefonos = document.getElementById('telefonos');
    p_direccion = document.getElementById('direccion');
    p_cliente_id = document.getElementById('cliente_id');
    p_factura_a = document.getElementById('factura_a');

    p_ci_nit.value = obj_ci_nit;
    p_apellidos.value = obj_apellidos;
    p_nombres.value = obj_nombres;
    p_telefonos.value = obj_telefonos;
    p_direccion.value = obj_direccion;
    p_cliente_id.value = cliente_id;
    p_factura_a.value = obj_factura_a;

    //nombre del cliente en el tab de imagenes
    const cliente_img = $('#span_cliente_imagenes');
    cliente_img.html(obj_nombres + ' ' + obj_apellidos);

    //historias
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

    datos = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'get_historias',
        'cliente_id': cliente_id,
        'nombres': obj_nombres,
        'apellidos': obj_apellidos,
        'csrfmiddlewaretoken': token
    }
    $('#div_ventas_historias').html(imgLoading);
    $('#div_ventas_historias').load(hostURL, datos, function () {
        //termina de cargar la ventana
    });

    $("#div_clientes").fadeOut('slow');
}

function ventaSeleccionMontura(tipo_montura, nombre_montura, montura_id) {
    const tp = document.getElementById(tipo_montura);
    tp.value = montura_id;

    const precio = lista_monturas_precios[montura_id];
    const objPrecio = document.getElementById('tipo_montura_precio');
    objPrecio.value = precio;

    //acc, calculo de precio al seleccionar montura
    // ventaCalcularPrecio();
    ventaSeleccionAlmacenMontura();
}

function ventaSeleccionAlmacenMontura() {
    const almacen = document.getElementById('almacen_id').value;
    const tipo_montura = document.getElementById('tipo_montura').value;

    const montura_stock = $('#div_montura_stock');

    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

    datos = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'stock_monturas',
        'tipo_montura_id': tipo_montura,
        'almacen_id': almacen,
        'csrfmiddlewaretoken': token
    }

    montura_stock.html(imgLoading);
    montura_stock.load(hostURL, datos, function () {
        //termina de cargar la ventana
    });
}

function ventaSeleccionStock(numero_registro, montura, id) {
    //asignamos el id del stock
    obj_aux = document.getElementById("stock_" + numero_registro);
    obj_aux.value = id;
}

function ventaCheckMaterialPrecio() {
    const valores = $('#materiales_select').val();
    let precio = 0;

    if (valores.length > 0) {
        for (let i = 0; i < valores.length; i++) {
            precio = precio + parseFloat(lista_materiales_precios[valores[i]]);
        }

    }
    const objPrecio = document.getElementById('material_precio');
    objPrecio.value = redondeo(precio, 2);

    //acc, calculo del precio
    //ventaCalcularPrecio();
}

function ventaCalcularPrecio() {
    const monturaPrecio = Trim(document.getElementById('tipo_montura_precio').value);
    const montPrecio = monturaPrecio === '' ? 0 : parseFloat(monturaPrecio);

    const materialPrecio = Trim(document.getElementById('material_precio').value);
    const matPrecio = materialPrecio === '' ? 0 : parseFloat(materialPrecio);

    const totalPedido = document.getElementById('total_pedido');
    totalPedido.value = redondeo(montPrecio + matPrecio, 2);

    totalPedidoPreVenta('');
}

//acc, descuento en venta
function calcularPorcentajeDescuentoVenta() {
    porcentaje_descuento = Trim(document.getElementById('porcentaje_descuento').value);
    total_pedido2 = Trim(document.getElementById('total_pedido').value);

    descuento_obj = document.getElementById('descuento');

    if (total_pedido2 != '' && porcentaje_descuento != '') {
        resta_descuento = (parseFloat(porcentaje_descuento) / 100) * parseFloat(total_pedido2);
        descuento_obj.value = redondeo(resta_descuento, 2);
    }
    else {
        if (total_pedido2 === '') {
            descuento_obj.value = '';
        }
    }
}

//acc, total por producto
function totalPedidoPreVenta(origen) {

    obj_total_pedido = document.getElementById('total_pedido');
    total_pedido = 0;
    if (Trim(obj_total_pedido.value) != '') {
        total_pedido = parseFloat(Trim(obj_total_pedido.value));
    }

    if (origen !== 'descuento') {
        calcularPorcentajeDescuentoVenta();
    }

    //descuento
    t_final = total_pedido;
    descuento = Trim(document.getElementById('descuento').value);
    total_venta = document.getElementById('total_venta');
    if (descuento != '') {
        val_descuento = parseFloat(descuento);
        t_final = t_final - val_descuento;
        total_venta.value = redondeo((total_pedido - val_descuento), 2);
    }
    else {
        total_venta.value = redondeo(total_pedido, 2);
    }

    //a cuenta
    a_cuenta = Trim(document.getElementById('a_cuenta').value);
    if (a_cuenta == '') {
        a_cuenta = '0';
    }
    saldo = document.getElementById('saldo');
    saldo.value = redondeo((t_final - parseFloat(a_cuenta)), 2);
}

//mostramos la lista de productos
function mostrarProductosVenta() {
    //verificamos las fechas
    const fecha_entrega = document.getElementById('fecha_entrega').value;
    const hora_entrega = document.getElementById('hora_entrega').value;
    const minuto_entrega = document.getElementById('minuto_entrega').value;
    const fecha_ini = parseInt(getFechaFormatoDB(fecha_entrega) + hora_entrega + minuto_entrega);

    const fecha_devolucion = document.getElementById('fecha_devolucion').value;
    const hora_devolucion = document.getElementById('hora_devolucion').value;
    const minuto_devolucion = document.getElementById('minuto_devolucion').value;
    const fecha_fin = parseInt(getFechaFormatoDB(fecha_devolucion) + hora_devolucion + minuto_devolucion);

    if (fecha_ini >= fecha_fin) {
        modalSetParameters('warning', 'center', 'Ventas!', 'La fecha de entrega no debe ser mayor a la fecha de devolucion', 'Cancelar', 'Volver');
        modalFunction.value = 'ventaWarning();';
        modalF.modal();
        return false;
    }
    else {
        $("#div_listap").fadeIn('slow');
        token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

        datos = {
            'module_x': document.forms['form_operation'].elements['module_x'].value,
            'operation_x': 'stock_productos',
            'fecha_entrega': fecha_entrega,
            'hora_entrega': hora_entrega,
            'minuto_entrega': minuto_entrega,
            'fecha_devolucion': fecha_devolucion,
            'hora_devolucion': hora_devolucion,
            'minuto_devolucion': minuto_devolucion,
            'csrfmiddlewaretoken': token,
        }

        const btn_s = document.getElementById('btn_stock');
        btn_s.disabled = true;

        listado = $("#div_cargar_stock");
        listado.fadeIn('slow');
        listado.html(imgLoading);
        listado.load(hostURL, datos, function () {
            //termina de cargar la ventana
            terminaStockVenta();
        });
    }
}

function terminaStockVenta() {
    const btn_s = document.getElementById('btn_stock');
    btn_s.disabled = false;
    $("#div_cargar_stock").fadeOut('slow');
    $("#div_listap").fadeIn('slow');
    reiniciarProductosVenta();
}

function ocultarProductosVenta() {
    reiniciarProductosVenta();
    $("#div_listap").fadeOut('slow');
}

function reiniciarProductosVenta() {
    //reiniciamos la seleccion
    for (i = 1; i <= 50; i++) {
        producto = document.getElementById('producto_' + i);
        tb2 = document.getElementById('tb2_' + i);

        try {
            cantidad = document.getElementById('cantidad_' + i);
            cantidad.value = '';

            //costo
            costo = document.getElementById('costo_' + i);
            costo.value = '';

            //total
            total = document.getElementById('total_' + i);
            total.value = '';
        }
        catch (e) { }


        producto.value = "0";
        tb2.value = "";

        //ocultamos las filas
        if (i > 1) {
            fila = document.getElementById('fila_' + i);
            fila.style.display = 'none';
        }
    }//end for
    obj_total = document.getElementById('total_pedido');
    obj_total.value = '';

    obj_desc = document.getElementById('porcentaje_descuento');
    obj_porcentaje_desc = document.getElementById('descuento');
    obj_t_venta = document.getElementById('total_venta');
    obj_desc.value = '';
    obj_porcentaje_desc.value = '';
    obj_t_venta.value = '';
}

//acc, seleccion del producto
function seleccionPPreVenta(numero_registro, producto, id) {
    //verificamos que no repita productos
    for (i = 1; i <= 50; i++) {
        aux_p = document.getElementById('producto_' + i);
        if (parseInt(numero_registro) != i && aux_p.value == id) {
            //alert('ya selecciono este producto');
            tb2 = document.getElementById('tb2_' + numero_registro);
            //tb2.focus();
            tb2.value = '';
            modalSetParameters('warning', 'center', 'Ventas!', 'Ya selecciono este producto', 'Cancelar', 'Volver');
            modalFunction.value = 'ventaWarning();';
            modalF.modal();
            return false;
        }
    }

    //asignamos el id del producto
    obj_aux = document.getElementById("producto_" + numero_registro);
    obj_aux.value = id;

    //recuperamos el precio y el stock del producto
    const precio_producto = lista_productos_precios[id];
    const costo_pro = document.getElementById('costo_' + numero_registro);
    costo_pro.value = precio_producto;

    //stock
    const stock_pro = document.getElementById('pro_stock_' + id);
    const span_stock = document.getElementById('span_stock_producto_' + numero_registro);
    span_stock.innerHTML = stock_pro.value;
    if (parseInt(stock_pro.value) <= 0) {
        span_stock.className = "input_stock_red";
    }
    else {
        span_stock.className = "input_stock";
    }


    numero = parseInt(numero_registro);
    numero_int = numero + 1;
    if (numero_int <= 50) {
        numero_str = numero_int.toString();
        nombre_actual = "fila_" + numero_str;
        objeto_actual = document.getElementById(nombre_actual);
        objeto_actual.style.display = "block";
        objeto_actual.style.display = "";
    }
}

//cobros
function anularCobroVenta(ci_id) {
    const div_a = $('#div_motivo_anula_' + ci_id);
    div_a.fadeIn('slow');
}

function anularCobroVentaCancelar(ci_id) {
    const div_a = $('#div_motivo_anula_' + ci_id);
    div_a.fadeOut('slow');
}

function anularCobroVentaConfirmar(ci_id) {
    const motivo_anula = Trim(document.getElementById('motivo_anula_' + ci_id).value);
    if (motivo_anula == '') {
        modalSetParameters('warning', 'center', 'Ventas!', 'debe llenar el motivo', 'Cancelar', 'Volver');
        modalFunction.value = 'ventaWarning();';
        modalF.modal();
    }
    else {
        document.forms['form_operation'].elements['motivo_anula'].value = motivo_anula;
        document.forms['form_operation'].elements['ci_id'].value = ci_id;
        document.forms['form_operation'].elements['operation_x2'].value = 'cobros_anular_x';
        modalSetParameters('danger', 'center', 'Cobros!', 'esta seguro de anular este cobro?', 'Cancelar', 'Anular');
        modalFunction.value = 'anularCobroVentaSend();';
        modalF.modal();
    }
}

function anularCobroVentaSend() {
    modalF.modal('toggle');

    sendFormObject('form_operation', div_modulo);
}

//impresion de venta
function imprimirVenta(venta_id) {
    modalPrintFunctionB1.value = "imprimirVentaPreImpreso('" + venta_id + "');";
    modalPrintFunctionB2.value = "imprimirVentaDisenio('" + venta_id + "');";
    modalPrintSetParameters('success', 'center', 'Ventas!', 'Imprimir PreImpreso?', 'SI', 'NO');
    modalFPrint.modal();
}

function imprimirVentaPreImpreso(venta_id) {
    modalFPrint.modal('toggle');
    document.forms['form_print'].elements['id'].value = venta_id;
    document.forms['form_print'].elements['operation_x'].value = 'imprimir_preimpreso';
    document.forms['form_print'].submit();
}

function imprimirVentaDisenio(venta_id) {
    modalFPrint.modal('toggle');
    document.forms['form_print'].elements['id'].value = venta_id;
    document.forms['form_print'].elements['operation_x'].value = 'imprimir_disenio';
    document.forms['form_print'].submit();
}

//impresion de venta gasto
function imprimirVentaGasto(gasto_id) {
    document.forms['form_print'].elements['id'].value = gasto_id;
    document.forms['form_print'].submit();
}

//impresion de venta cobro
function imprimirVentaCobro(cobro_id) {
    document.forms['form_print'].elements['id'].value = cobro_id;
    document.forms['form_print'].submit();
}

//impresion de venta resumen
function imprimirVentaResumen(venta_id) {
    document.forms['form_print'].elements['id'].value = venta_id;
    document.forms['form_print'].elements['operation_x'].value = 'print_resumen';
    document.forms['form_print'].submit();
}

//impresion de venta resumen desde ventana principal de ventas
function imprimirResumenFinalizar(venta_id) {
    document.forms['form_print'].elements['id'].value = venta_id;
    document.forms['form_print'].elements['operation_x'].value = 'print_resumen';
    document.forms['form_print'].submit();
}

function ventaSelectTipoVenta() {
    //segun el tipo de venta
    const tipo_venta = document.getElementById('tipo_venta').value;
    const div_pp_1 = $('#div_planpagos_1');
    const div_pp_2 = $('#div_planpagos_2');
    if (tipo_venta === 'contado') {
        div_pp_1.fadeOut('slow');
        div_pp_2.fadeOut('slow');
    }
    else {
        div_pp_1.fadeIn('slow');
        div_pp_2.fadeIn('slow');
    }
}

function verifyPasarVenta() {
    //verificamos tipo de montura y montura
    const tipo_montura = Trim(document.getElementById('tipo_montura').value);
    if (tipo_montura === '0' || tipo_montura === '') {
        return 'Debe Seleccionar el tipo de montura';
    }

    //stock
    const stock1 = Trim(document.getElementById('stock_1').value);
    if (stock1 === '0' || stock1 === '') {
        return 'Debe Seleccionar la montura de stock';
    }

    //materiales
    const valores = $('#materiales_select').val();
    if (valores.length === 0) {
        return 'Debe seleccionar al menos 1 material'
    }

    //laboratorio
    const laboratorio = Trim(document.getElementById('laboratorio_id').value);
    if (laboratorio === '0') {
        return 'Debe Seleccionar un laboratorio';
    }

    //tecnico
    const tecnico = Trim(document.getElementById('tecnico_id').value);
    if (tecnico === '0') {
        return 'Debe Seleccionar un tecnico';
    }

    //oftalmologo
    const oftalmologo = Trim(document.getElementById('oftalmologo_id').value);
    if (oftalmologo === '0') {
        return 'Debe Seleccionar un oftalmologo';
    }

    //total
    const total_venta = Trim(document.getElementById('total_venta').value);
    if (total_venta === '') {
        return 'El total de la venta debe ser mayor a cero';
    }
    if (parseFloat(total_venta) <= 0) {
        return 'El total de la venta debe ser mayor a cero';
    }

    //tipo de venta
    const tipo_venta = Trim(document.getElementById('tipo_venta').value);
    if (tipo_venta === 'planpagos') {
        const cuotas = Trim(document.getElementById('cuotas_planpagos').value);
        if (cuotas === '') {
            return 'Debe llenar la cantidad de cuotas';
        }
        const dias = Trim(document.getElementById('dias_planpagos').value);
        if (dias === '') {
            return 'Debe llenar la cantidad de dias';
        }
        const a_cuenta = Trim(document.getElementById('a_cuenta').value);
        if (a_cuenta !== '') {
            if (parseFloat(a_cuenta) > 0) {
                return 'En ventas con plan de pagos, no debe existir un monto a cuenta';
            }
        }
    }

    return true;
}

function ventaValidarStock() {
    const stock = document.getElementById('stock_1');
    const tb2 = document.getElementById('tb2_1');
    if (tb2) {
        if (Trim(tb2.value) === '') {
            stock.value = '0';
        }
    }
}

function ventasCambiaPrecio() {
    totalPedidoPreVenta('');
}

async function ventasCargarImagen() {
    const nuevaImagen = Trim(document.getElementById('imagen1').value);
    if (nuevaImagen === '') {
        modalSetParameters('warning', 'center', 'Ventas!', 'Debe seleccionar la imagen', 'Cancelar', 'Volver');
        modalFunction.value = 'ventaWarning();';
        modalF.modal();
        return false;
    }

    const btn_imagen = document.getElementById('btn_imagen');
    btn_imagen.disabled = true;
    const fd = new FormData(document.forms['form_imagenes']);

    $('#div_lista_imagenes').html(imgLoading);

    let result;

    try {
        result = await $.ajax({
            url: hostURL,
            method: 'POST',
            type: 'POST',
            cache: false,
            data: fd,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response != 0) {
                    $('#div_lista_imagenes').html(response);
                } else {
                    alert('error al realizar la operacion, intentelo de nuevo');
                }
                btn_imagen.disabled = false;
            },
            error: function (qXHR, textStatus, errorThrown) {
                console.log(errorThrown);
                console.log(qXHR);
                console.log(textStatus);
            },
        });
        //alert(result);
        btn_imagen.disabled = false;
    }
    catch (e) {
        console.error(e);
        btn_imagen.disabled = false;
    }
}

//mostramos la imagen
function ventasMostrarImagen(pid) {
    document.form_img.id.value = pid;
    document.form_img.submit();
}

//eliminar imagen
function ventasEliminarImagen(pid) {

    //token
    token = document.forms['form_imagenes'].elements['csrfmiddlewaretoken'].value;
    module_x = document.forms['form_operation'].elements['module_x'].value;

    datos_imagen = {
        'module_x': module_x,
        'operation_x': 'eliminar_imagen',
        'id': pid,
        'csrfmiddlewaretoken': token,
    }

    $("#div_lista_imagenes").html(imgLoading);
    $("#div_lista_imagenes").load(hostURL, datos_imagen, function () {
        //termina de ejecutar
    });
}

//imagen de venta
function ventasMostrarVentaImagen(ventaImagenId) {
    document.form_img.operation_x.value = 'mostrar_imagen_venta';
    document.form_img.id.value = ventaImagenId;
    document.form_img.submit();
}