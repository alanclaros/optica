/*
* home page java script
*/

//cupon
var tiempo_ini = 0;
var tiempo_fin = 0;
var primera_vez = 0;
var timeDiff = 0;
var seBusco = 0;

//ci
var tiempo_ini_2 = 0;
var tiempo_fin_2 = 0;
var primera_vez_2 = 0;
var timeDiff_2 = 0;
var seBusco_2 = 0;

setInterval('buscarCupon()', 1000);
setInterval('buscarCI()', 1000);

//cupon
function empiezaEscribir() {
    if (primera_vez == 0) {
        primera_vez = 1;
        tiempo_ini = new Date();
        tiempo_fin = new Date();
    }
    else {
        //variable que indicar si mandar el ajax para buscar
        seBusco = 0;

        tiempo = new Date();
        // time difference in ms
        timeDiff = tiempo - tiempo_fin;

        tiempo_fin = tiempo;

        // strip the ms
        timeDiff /= 1000;
    }
}

//cupon
function buscarCupon() {
    try {
        cupon_txt = Trim(document.getElementById('cupon').value);
        if (cupon_txt.length > 4) {
            tiempo = new Date();
            timeDiff = tiempo - tiempo_fin;
            tiempo_fin = tiempo;
            timeDiff /= 1000;

            imagen = '<img src="' + url_empresa + '/static/img/pass/loading2.gif">';
            url_main = document.forms['formulario'].elements['url_main'].value;
            token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
            datos = {
                'cupon': cupon_txt,
                'operation_x': 'buscar_cupon',
                'csrfmiddlewaretoken': token,
            }
            //alert(timeDiff>1.5);
            if (timeDiff > 0.7 && seBusco == 0) {
                seBusco = 1;
                //alert('termino escribir');

                //$('#tabla_cliente').fadeIn('slow');

                $("#span_cupon").html(imagen);
                $("#span_cupon").load(url_main, datos, function () {
                    //termina de cargar la ventana
                    resultadoBusqedaCupon();
                });
            }
        }
    }
    catch (e) {
        $("#span_cupon").html('&nbsp;');
    }
}

//cupon resultado
function resultadoBusqedaCupon() {
    try {
        //r_cupon = document.getElementById('r_cupon').value;
        r_cupon_id = document.getElementById('r_cupon_id').value;
        r_porcentaje_descuento = document.getElementById('r_porcentaje_descuento').value;

        // alert(r_cupon_id);
        // alert(r_porcentaje_descuento);

        //cupon = document.getElementById('cupon');
        cupon_id = document.getElementById('cupon_id');
        p_porcentaje_desc = document.getElementById('porcentaje_descuento');

        //cupon.value = r_cupon;
        cupon_id.value = r_cupon_id;
        p_porcentaje_desc.value = r_porcentaje_descuento;

        //txt porcentaje
        txt_porcen = document.getElementById('txt_porcentaje');
        txt_porcen.innerHTML = '(' + r_porcentaje_descuento + ' &#37;)';

        //calcularPorcentajeDescuento();
        //totalPedido();
        totalCompra();
    }
    catch (e) {
        alert('no existe datos para este Cupon');
        $("#span_cupon").html('&nbsp;');
    }
}


//ci
function empiezaEscribir2() {
    if (primera_vez_2 == 0) {
        primera_vez_2 = 1;
        tiempo_ini_2 = new Date();
        tiempo_fin_2 = new Date();
    }
    else {
        //variable que indicar si mandar el ajax para buscar
        seBusco_2 = 0;

        tiempo_2 = new Date();
        // time difference in ms
        timeDiff_2 = tiempo_2 - tiempo_fin_2;

        tiempo_fin_2 = tiempo_2;

        // strip the ms
        timeDiff_2 /= 1000;
    }
}

//ci
function buscarCI() {
    try {
        ci_txt = Trim(document.getElementById('ci').value);
        if (ci_txt.length > 4) {
            tiempo_2 = new Date();
            timeDiff_2 = tiempo_2 - tiempo_fin_2;
            tiempo_fin_2 = tiempo_2;
            timeDiff_2 /= 1000;

            imagen = '<img src="' + url_empresa + '/static/img/pass/loading2.gif">';
            url_main = document.forms['formulario'].elements['url_main'].value;
            token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
            datos = {
                'ci': ci_txt,
                'operation_x': 'buscar_ci',
                'csrfmiddlewaretoken': token,
            }
            //alert(timeDiff>1.5);
            if (timeDiff_2 > 0.7 && seBusco_2 == 0) {
                seBusco_2 = 1;
                //alert('termino escribir');

                //$('#tabla_cliente').fadeIn('slow');

                $("#span_ci").html(imagen);
                $("#span_ci").load(url_main, datos, function () {
                    //termina de cargar la ventana
                    resultadoBusqedaCI();
                });
            }
        }
    }
    catch (e) {
        $("#span_ci").html('&nbsp;');
    }
}

//ci resultado
function resultadoBusqedaCI() {
    try {
        r_apellidos = document.getElementById('r_apellidos').value;
        r_nombres = document.getElementById('r_nombres').value;
        r_telefonos = document.getElementById('r_telefonos').value;
        r_direccion = document.getElementById('r_direccion').value;
        r_email = document.getElementById('r_email').value;

        apellidos = document.getElementById('apellidos');
        nombres = document.getElementById('nombres');
        telefonos = document.getElementById('telefonos');
        direccion = document.getElementById('direccion');
        email = document.getElementById('email');

        apellidos.value = r_apellidos;
        nombres.value = r_nombres;
        telefonos.value = r_telefonos;
        direccion.value = r_direccion;
        email.value = r_email;
        //alert('busqueda terminada');
    }
    catch (e) {
        //alert('no existe datos para este CI');
        console.log('no existe resultados');
        $("#span_ci").html('&nbsp;');
    }
}


url_empresa = document.getElementById('url_empresa').value;

function cambiarLinea() {
    linea_select = document.getElementById('linea_select').value;
    document.form_linea.linea.value = linea_select;
    document.form_linea.submit();
}

function mostrarD(nombre_div, p_id) {
    //token
    token = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
    url_main = document.forms['form_operation'].elements['url_main'].value;

    document.form_operation.operation_x.value = 'img_producto';
    document.form_operation.id.value = p_id;

    datos_img = {
        'operation_x': 'img_producto',
        'id': p_id,
        'csrfmiddlewaretoken': token,
    }

    //loading
    div_load = document.getElementById(nombre_div);
    div_load.className = 'overlay';
    div_load.innerHTML = '<i class="fas fa-2x fa-sync-alt fa-spin"></i>';

    imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
    $("#div_img_carousel").html(imagen);
    $("#div_img_carousel").load(url_main, datos_img, function () {
        //termina de cargar ajax
        mostrarModal(nombre_div);
    });
}

//mostrando imagenes del producto en modal
function mostrarModal(nombre_div) {
    div_load2 = document.getElementById(nombre_div);
    div_load2.className = '';
    div_load2.innerHTML = '';
    $("#myModal").modal();
}

//formulario de contacdto
function formularioContacto() {
    apellidos = document.getElementById('apellidos');
    apellidos_value = Trim(apellidos.value);

    nombres = document.getElementById('nombres');
    nombres_value = Trim(nombres.value);

    telefonos = document.getElementById('telefonos');
    telefonos_value = Trim(telefonos.value);

    mensaje = document.getElementById('mensaje');
    mensaje_value = Trim(mensaje.value);

    email = document.getElementById('email');
    email_value = Trim(email.value);

    if (apellidos_value == '') {
        alert('Debe llenar sus apellidos');
        apellidos.focus();
        return false;
    }

    if (nombres_value == '') {
        alert('Debe llenar sus nombres');
        nombres.focus();
        return false;
    }

    if (telefonos_value == '') {
        alert('Debe llenar sus telefonos');
        telefonos.focus();
        return false;
    }

    if (mensaje_value == '') {
        alert('Debe llenar su mensaje');
        mensaje.focus();
        return false;
    }

    //token
    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    url_main = document.forms['formulario'].elements['url_main'].value;

    datos_contacto = {
        'operation_x': 'contacto',
        'nombres': nombres_value,
        'apellidos': apellidos_value,
        'telefonos': telefonos_value,
        'email': email_value,
        'mensaje': mensaje_value,
        'csrfmiddlewaretoken': token,
    }

    //div fila
    div_fila = $("#fila_resultado");
    div_fila.fadeIn('slow');

    imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
    $("#div_resultado").html(imagen);
    $("#div_resultado").load(url_main, datos_contacto, function () {
        //termina de cargar ajax
        limpiar_form_contacto();
    });
}

//limipamos
function limpiar_form_contacto() {
    apellidos = document.getElementById('apellidos');
    apellidos.value = "";

    nombres = document.getElementById('nombres');
    nombres.value = "";

    telefonos = document.getElementById('telefonos');
    telefonos.value = "";

    mensaje = document.getElementById('mensaje');
    mensaje.value = "";

    email = document.getElementById('email');
    email.value = "";
}

//mostrando confirmacion de compra
function mostrarModalCompra(producto_id, precio) {
    cantidad = document.getElementById('producto_' + producto_id);
    cantidad_valor = Trim(cantidad.value);
    if (cantidad_valor == '') {
        alert('Debe llenar una cantidad');
        cantidad.focus();
        return false;
    }

    //producto id
    pedido_prod_id = document.getElementById('pedido_producto_id');
    pedido_prod_id.value = producto_id;

    //producto
    pedido_pr = document.getElementById('pedido_producto');
    nombre_pr = document.getElementById('producto_nombre_' + producto_id).value;
    pedido_pr.innerHTML = nombre_pr;

    //cantidad
    pedido_cant = document.getElementById('pedido_cantidad');
    pedido_cant.value = cantidad_valor;

    //precio
    pedido_prec = document.getElementById('pedido_precio');
    pedido_prec.value = precio;

    //total
    total = redondeo(parseFloat(precio) * parseFloat(cantidad_valor), 2) + ' Bs.';
    pedido_total = document.getElementById('pedido_total');
    pedido_total.innerHTML = total;

    //modal
    $("#modalCompra").modal();
}

//total del pedido
function totalPedido() {
    //cantidad
    pedido_cant = document.getElementById('pedido_cantidad');
    pedido_cant_valor = Trim(pedido_cant.value);

    //total
    pedido_total = document.getElementById('pedido_total');

    if (pedido_cant_valor == '') {
        //alert('Debe llenar una cantidad');
        pedido_total.innerHTML = '0';
        pedido_cant.focus();
        return false;
    }

    //precio
    precio = document.getElementById('pedido_precio').value;

    //total
    total = redondeo(parseFloat(precio) * parseFloat(pedido_cant_valor), 2) + ' Bs.';
    pedido_total.innerHTML = total;
}

//comprar y seguir
function agregarSeguir() {
    //verificamos cantidad
    cantidad = document.getElementById('pedido_cantidad');
    cantidad_valor = Trim(cantidad.value);
    if (cantidad == '') {
        alert('Debe llenar la cantidad');
        cantidad.focus();
        return false;
    }

    //mandamos los datos
    //token
    token = document.forms['form_cart'].elements['csrfmiddlewaretoken'].value;
    url_main = document.forms['form_cart'].elements['url_main'].value;
    producto_id = document.getElementById('pedido_producto_id').value;

    datos_cart = {
        'operation_x': 'add_cart',
        'producto': producto_id,
        'cantidad': cantidad_valor,
        'csrfmiddlewaretoken': token,
    }

    //div notificaciones
    imagen = '<img src="' + url_empresa + '/static/img/pass/loading2.gif">';

    $("#div_notifications").html(imagen);
    $("#div_notifications").load(url_main, datos_cart, function () {
        //termina de cargar ajax
        $("#modalCompra").modal('hide');
    });

    return true;
}

//comprar ahora
function comprarAhora() {
    if (agregarSeguir()) {
        sleep(2000);
        window.open(url_empresa + '/carrito/', '_self');
    }
}

function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds) {
            break;
        }
    }
}

//total del carrito
function totalCarrito(p_id) {
    //cantidad
    pedido_cant = document.getElementById('pedido_' + p_id);
    pedido_cant_valor = Trim(pedido_cant.value);

    //total
    pedido_total = document.getElementById('pedido_total_' + p_id);

    if (pedido_cant_valor == '') {
        //alert('Debe llenar una cantidad');
        pedido_total.innerHTML = '0';
        totalCompra();
        return false;
    }

    //precio
    precio = document.getElementById('precio_' + p_id).value;

    //total
    total = redondeo(parseFloat(precio) * parseFloat(pedido_cant_valor), 2) + ' Bs.';
    pedido_total.innerHTML = total;

    totalCompra();
}

function totalCompra() {
    lista_ids = document.getElementById('lista_ids').value;
    total_c = 0;

    if (lista_ids != '') {
        division = lista_ids.split(';');
        for (i = 0; i < division.length; i++) {
            cantidad = Trim(document.getElementById('pedido_' + division[i]).value);
            precio = Trim(document.getElementById('precio_' + division[i]).value);

            if (cantidad != '' && precio != '') {
                total_c = total_c + (parseFloat(cantidad) * parseFloat(precio));
            }
        }
        total_car = document.getElementById('total_carrito');
        total_car.innerHTML = redondeo(total_c, 2) + ' Bs.';
    }
}

//mostrando dialogo
empezando_pedido = 'no';
function realizarPedido() {
    ci = document.getElementById('ci');
    ci_value = Trim(ci.value);

    apellidos = document.getElementById('apellidos');
    apellidos_value = Trim(apellidos.value);

    nombres = document.getElementById('nombres');
    nombres_value = Trim(nombres.value);

    telefonos = document.getElementById('telefonos');
    telefonos_value = Trim(telefonos.value);

    direccion = document.getElementById('direccion');
    direccion_value = Trim(direccion.value);

    email = document.getElementById('email');
    email_value = Trim(email.value);

    mensaje = document.getElementById('mensaje');
    mensaje_value = Trim(mensaje.value);

    if (ci_value == '') {
        alert('Debe llenar su CI');
        ci.focus();
        return false;
    }

    if (apellidos_value == '') {
        alert('Debe llenar sus apellidos');
        apellidos.focus();
        return false;
    }

    if (nombres_value == '') {
        alert('Debe llenar sus nombres');
        nombres.focus();
        return false;
    }

    if (telefonos_value == '') {
        alert('Debe llenar sus telefonos');
        telefonos.focus();
        return false;
    }

    if (direccion_value == '') {
        alert('Debe llenar su direccion');
        direccion.focus();
        return false;
    }

    //lista de productos para el pedido
    lista_ids = document.getElementById('lista_ids').value;
    if (lista_ids == '') {
        alert('debe tener al menos un producto');
        return false;
    }

    division = lista_ids.split(';');
    lista_productos_ids = '';
    lista_cantidad = '';

    for (i = 0; i < division.length; i++) {
        cantidad = Trim(document.getElementById('pedido_' + division[i]).value);

        if (cantidad != '') {
            lista_productos_ids += division[i] + '|';
            lista_cantidad += cantidad + '|';
        }
    }

    if (lista_productos_ids == '') {
        alert('Debe Comprar al menos un producto');
        return false;
    }

    //modal
    empezando_pedido = 'si';
    $("#modalCarrito").modal();
}

function confirmarPedido() {

    //lista de productos para el pedido
    lista_ids = document.getElementById('lista_ids').value;

    division = lista_ids.split(';');
    lista_productos_ids = '';
    lista_cantidad = '';

    for (i = 0; i < division.length; i++) {
        cantidad = Trim(document.getElementById('pedido_' + division[i]).value);

        if (cantidad != '') {
            lista_productos_ids += division[i] + '|';
            lista_cantidad += cantidad + '|';
        }
    }

    if (lista_productos_ids == '') {
        alert('Debe Comprar al menos un producto');
        return false;
    }

    if (empezando_pedido == 'si') {
        empezando_pedido = 'no';
        btn_cart = document.getElementById('btn_cart');
        btn_cart2 = document.getElementById('btn_cart2');
        btn_cart.disabled = true;
        btn_cart2.disabled = true;

        lista_productos_ids = lista_productos_ids.substring(0, lista_productos_ids.length - 1);
        lista_cantidad = lista_cantidad.substring(0, lista_cantidad.length - 1);

        //token
        token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
        url_main = document.forms['formulario'].elements['url_main'].value;

        tipo_pedido = document.getElementById('tipo_pedido').value;

        //cupon, descuento
        s_cupon = Trim(document.getElementById('cupon').value);
        s_cupon_id = Trim(document.getElementById('cupon_id').value);
        s_porcentaje_descuento = Trim(document.getElementById('porcentaje_descuento').value);

        datos_pedido = {
            'operation_x': 'realizar_pedido',
            'ci': ci_value,
            'nombres': nombres_value,
            'apellidos': apellidos_value,
            'telefonos': telefonos_value,
            'direccion': direccion_value,
            'email': email_value,
            'mensaje': mensaje_value,
            'tipo_pedido': tipo_pedido,
            'lista_productos_ids': lista_productos_ids,
            'lista_cantidad': lista_cantidad,
            'csrfmiddlewaretoken': token,

            'cupon': s_cupon,
            'cupon_id': s_cupon_id,
            'porcentaje_descuento': s_porcentaje_descuento,
        }

        //div fila
        div_fila = $("#fila_resultado");
        div_fila.fadeIn('slow');

        imagen = '<img src="' + url_empresa + '/static/img/pass/loading.gif">';
        $("#div_resultado").html(imagen);
        $("#div_resultado").load(url_main, datos_pedido, function () {
            //termina de cargar ajax
            finalizarCarrito();

            error_de_carrito = document.getElementById('error_carrito').value;
            if (error_de_carrito != '1') {
                const total_compra = document.getElementById('total_carrito').innerHTML;
                const head = 'pedido de venta';
                const body = 'Cliente: ' + apellidos_value + ' ' + nombres_value + '\nFonos: ' + telefonos_value + '\nTotal: ' + total_compra + "\nMensaje: " + mensaje_value;
                const id = document.getElementById('lista_notificacion').value;

                //btn_push= document.getElementById('btn_webpush');
                url_push = document.forms['formulario'].elements['url_webpush'].value;

                datos_push = {
                    'head': head,
                    'body': body,
                    'id': id,
                    'csrfmiddlewaretoken': token,
                }
                console.log('datos push: ', datos_push);

                $("#div_push_result").html(imagen);
                $("#div_push_result").load(url_push, datos_push, function () {
                    //termina de cargar ajax
                    //finalizarCarrito();
                    //alert('push enviado');
                });
            }
        });
    }
}

//cancelamos
function cancelarPedido() {
    $("#modalCarrito").modal('hide');
}

//finalizar carrito
function finalizarCarrito() {
    $("#modalCarrito").modal('hide');
    $("#tabla_cliente").fadeOut('slow');
    $("#tabla_detalle").fadeOut('slow');
    $("#tabla_boton").fadeOut('slow');

    //notificaciones
    div_noti = $("#div_notifications");
    div_noti.html('<i class="fas fa-cart-arrow-down notification_icon"></i>');

    //webpush
}

//para ir al carrito desde el icono
function irCarrito(direccion) {
    window.open(direccion, '_self');
}

//eliminar producto
function eliminarProducto(p_id) {
    if (confirm('Esta seguro de eliminar este producto?')) {
        document.form_delete.operation_x.value = 'delete';
        document.form_delete.producto.value = p_id;
        document.form_delete.submit();
    }
}

//forma de pago
function formaDePago(tipo) {
    tabla_qr = $("#tabla_qr");
    tabla_transferencia = $("#tabla_transferencia");

    if (tipo == "qr") {
        document.formulario.tipo_pedido.value = 'qr';
        tabla_qr.fadeIn('slow');
        tabla_transferencia.fadeOut('slow');
    }
    else {
        document.formulario.tipo_pedido.value = 'transferencia';
        tabla_qr.fadeOut('slow');
        tabla_transferencia.fadeIn('slow');
    }
}

//ropa, detalle del producto
function detalleProducto(producto_id, producto) {
    document.form_detalle.id.value = producto_id;
    document.form_detalle.producto.value = producto;
    document.form_detalle.submit();
}

function paginaInicio() {
    document.form_inicio.submit();
}

//acc, total por producto
function totalPedidoVenta(numero_registro) {
    total_pedido = 0;

    cantidad = Trim(document.getElementById('cantidad_' + numero_registro).value);
    costo = Trim(document.getElementById('costo_' + numero_registro).value);
    if (cantidad != '' && costo != '') {
        cantidad_valor = parseFloat(cantidad);
        costo_valor = parseFloat(costo);
        total = cantidad_valor * costo_valor;
        total_pedido += total;
        obj_total = document.getElementById('total_' + numero_registro);
        obj_total.value = redondeo(total, 2);
    }
}

function nextPedido() {
    tab_forma_pago = $('#custom-tabs-one-profile-tab');
    tab_forma_pago.click();
}

function anteriorPedido() {
    tab_datos = $('#custom-tabs-one-home-tab');
    tab_datos.click();
}

//seleccion tipo de montura
function seleccionaTipoMontura(tipo_montura_id) {
    color_borde_resaltado = document.getElementById('color_borde_resaltado').value;

    e_color = document.getElementById('tipo_montura_' + tipo_montura_id);
    aux_color = getRGB(e_color.style.borderColor);

    if (aux_color['red'] == '255' && aux_color['green'] == '255' && aux_color['blue'] == '255') {
        e_color.style.borderColor = color_borde_resaltado;
    }
    else {
        e_color.style.borderColor = '#FFFFFF';
    }

    //asignamos los filtros
    lista_objeto = Trim(document.getElementById('lista_tipos_montura').value);
    div_objeto = lista_objeto.split(',');
    //console.log('lista objeto: ', lista_objeto);
    //console.log('div objeto: ', div_objeto);
    objeto_select = '';
    for (ico = 0; ico < div_objeto.length; ico++) {
        ax_element = document.getElementById('tipo_montura_' + div_objeto[ico]);
        ax_color = getRGB(ax_element.style.borderColor);
        if (ax_color['red'] == '255' && ax_color['green'] == '255' && ax_color['blue'] == '255') {
            //no seleccionado
        }
        else {
            objeto_select += div_objeto[ico] + ',';
        }
    }
    if (objeto_select.length > 0) {
        objeto_select = objeto_select.substring(0, objeto_select.length - 1);
    }
    //console.log('tipos montura: ', objeto_select);
    //asigamos a los formularios de busqueda
    document.forms['form_producto'].elements['tipos_montura_select'].value = objeto_select;
    document.forms['form_linea'].elements['tipos_montura_select'].value = objeto_select;
}

//seleccion disenio lente
function seleccionaDisenioLente(disenio_lente_id) {
    color_borde_resaltado = document.getElementById('color_borde_resaltado').value;

    e_color = document.getElementById('disenio_lente_' + disenio_lente_id);
    aux_color = getRGB(e_color.style.borderColor);

    if (aux_color['red'] == '255' && aux_color['green'] == '255' && aux_color['blue'] == '255') {
        e_color.style.borderColor = color_borde_resaltado;
    }
    else {
        e_color.style.borderColor = '#FFFFFF';
    }

    //asignamos los filtros
    lista_objeto = Trim(document.getElementById('lista_disenio_lentes').value);
    div_objeto = lista_objeto.split(',');
    objeto_select = '';
    for (ico = 0; ico < div_objeto.length; ico++) {
        ax_element = document.getElementById('disenio_lente_' + div_objeto[ico]);
        ax_color = getRGB(ax_element.style.borderColor);
        if (ax_color['red'] == '255' && ax_color['green'] == '255' && ax_color['blue'] == '255') {
            //no seleccionado
        }
        else {
            objeto_select += div_objeto[ico] + ',';
        }
    }
    if (objeto_select.length > 0) {
        objeto_select = objeto_select.substring(0, objeto_select.length - 1);
    }

    //asigamos a los formularios de busqueda
    document.forms['form_producto'].elements['disenio_lentes_select'].value = objeto_select;
    document.forms['form_linea'].elements['disenio_lentes_select'].value = objeto_select;
}

//seleccion material
function seleccionaMaterial(material_id) {
    color_borde_resaltado = document.getElementById('color_borde_resaltado').value;

    e_color = document.getElementById('material_' + material_id);
    aux_color = getRGB(e_color.style.borderColor);

    if (aux_color['red'] == '255' && aux_color['green'] == '255' && aux_color['blue'] == '255') {
        e_color.style.borderColor = color_borde_resaltado;
    }
    else {
        e_color.style.borderColor = '#FFFFFF';
    }

    //asignamos los filtros
    lista_objeto = Trim(document.getElementById('lista_materiales').value);
    div_objeto = lista_objeto.split(',');
    objeto_select = '';
    for (ico = 0; ico < div_objeto.length; ico++) {
        ax_element = document.getElementById('material_' + div_objeto[ico]);
        ax_color = getRGB(ax_element.style.borderColor);
        if (ax_color['red'] == '255' && ax_color['green'] == '255' && ax_color['blue'] == '255') {
            //no seleccionado
        }
        else {
            objeto_select += div_objeto[ico] + ',';
        }
    }
    if (objeto_select.length > 0) {
        objeto_select = objeto_select.substring(0, objeto_select.length - 1);
    }

    //asigamos a los formularios de busqueda
    document.forms['form_producto'].elements['materiales_select'].value = objeto_select;
    document.forms['form_linea'].elements['materiales_select'].value = objeto_select;
}

//seleccion de color
function seleccionaColor(color_id) {
    color_borde_resaltado = document.getElementById('color_borde_resaltado').value;
    e_color = document.getElementById('color_' + color_id);

    aux_color = getRGB(e_color.style.borderColor);

    if (aux_color['red'] == '255' && aux_color['green'] == '255' && aux_color['blue'] == '255') {
        e_color.style.borderColor = color_borde_resaltado;
    }
    else {
        e_color.style.borderColor = '#FFFFFF';
    }

    //asignamos los filtros
    lista_colores = Trim(document.getElementById('lista_colores').value);
    div_co = lista_colores.split(',');
    colores_select = '';
    for (ico = 0; ico < div_co.length; ico++) {
        ax_element = document.getElementById('color_' + div_co[ico]);
        ax_color = getRGB(ax_element.style.borderColor);
        if (ax_color['red'] == '255' && ax_color['green'] == '255' && ax_color['blue'] == '255') {
            //no seleccionado
        }
        else {
            colores_select += div_co[ico] + ',';
        }
    }
    if (colores_select.length > 0) {
        colores_select = colores_select.substring(0, colores_select.length - 1);
    }

    //asigamos a los formularios de busqueda
    document.forms['form_producto'].elements['colores_select'].value = colores_select;
    document.forms['form_linea'].elements['colores_select'].value = colores_select;
}

//seleccion marca
function seleccionaMarca(marca_id) {
    color_borde_resaltado = document.getElementById('color_borde_resaltado').value;

    e_color = document.getElementById('marca_' + marca_id);
    aux_color = getRGB(e_color.style.borderColor);

    if (aux_color['red'] == '255' && aux_color['green'] == '255' && aux_color['blue'] == '255') {
        e_color.style.borderColor = color_borde_resaltado;
    }
    else {
        e_color.style.borderColor = '#FFFFFF';
    }

    //asignamos los filtros
    lista_objeto = Trim(document.getElementById('lista_marcas').value);
    div_objeto = lista_objeto.split(',');
    objeto_select = '';
    for (ico = 0; ico < div_objeto.length; ico++) {
        ax_element = document.getElementById('marca_' + div_objeto[ico]);
        ax_color = getRGB(ax_element.style.borderColor);
        if (ax_color['red'] == '255' && ax_color['green'] == '255' && ax_color['blue'] == '255') {
            //no seleccionado
        }
        else {
            objeto_select += div_objeto[ico] + ',';
        }
    }
    if (objeto_select.length > 0) {
        objeto_select = objeto_select.substring(0, objeto_select.length - 1);
    }

    //asigamos a los formularios de busqueda
    document.forms['form_producto'].elements['marcas_select'].value = objeto_select;
    document.forms['form_linea'].elements['marcas_select'].value = objeto_select;
}

function getRGB(str) {
    var match = str.match(/rgba?\((\d{1,3}), ?(\d{1,3}), ?(\d{1,3})\)?(?:, ?(\d(?:\.\d?))\))?/);
    return match ? {
        red: match[1],
        green: match[2],
        blue: match[3]
    } : {};
}

//marcar oferta
function marcarOferta() {
    aux_oferta = document.getElementById('aux_oferta');
    p_oferta = document.getElementById('oferta');
    if (aux_oferta.checked) {
        p_oferta.value = '1';
        document.forms['form_producto'].elements['oferta'].value = '1';
        document.forms['form_linea'].elements['oferta'].value = '1';
    }
    else {
        p_oferta.value = '0';
        document.forms['form_producto'].elements['oferta'].value = '0';
        document.forms['form_linea'].elements['oferta'].value = '0';
    }
}

//marcar mas vendido
function marcarMasVendido() {
    aux_mas_vendido = document.getElementById('aux_mas_vendido');
    p_mas_vendido = document.getElementById('mas_vendido');
    if (aux_mas_vendido.checked) {
        p_mas_vendido.value = '1';
        document.forms['form_producto'].elements['mas_vendido'].value = '1';
        document.forms['form_linea'].elements['mas_vendido'].value = '1';
    }
    else {
        p_mas_vendido.value = '0';
        document.forms['form_producto'].elements['mas_vendido'].value = '0';
        document.forms['form_linea'].elements['mas_vendido'].value = '0';
    }
}

//marcar novedad
function marcarNovedad() {
    aux_novedad = document.getElementById('aux_novedad');
    p_novedad = document.getElementById('novedad');
    if (aux_novedad.checked) {
        p_novedad.value = '1';
        document.forms['form_producto'].elements['novedad'].value = '1';
        document.forms['form_linea'].elements['novedad'].value = '1';
    }
    else {
        p_novedad.value = '0';
        document.forms['form_producto'].elements['novedad'].value = '0';
        document.forms['form_linea'].elements['novedad'].value = '0';
    }
}

async function buscarProducto() {
    producto_dato = document.getElementById('producto_search');
    producto_val = Trim(producto_dato.value);
    if (producto_val == '') {
        alert('Debe escribir un criterio de busqueda');
        producto_dato.focus();
        return false;
    }

    url_main = document.forms['form_operation'].elements['url_main'].value;
    document.form_producto.producto.value = producto_val;

    //loading
    div_loading_sup = document.getElementById('loading_search');
    div_loading_sup.className = 'overlay';
    div_loading_sup.innerHTML = '<i class="fas fa-2x fa-sync-alt fa-spin"></i>';

    div_loading_listado = document.getElementById('loading_listado');
    div_loading_listado.className = 'overlay';
    div_loading_listado.innerHTML = '<i class="fas fa-2x fa-sync-alt fa-spin"></i>';

    var fd = new FormData(document.forms['form_producto']);

    let result22;

    try {
        result22 = await $.ajax({
            url: url_main,
            method: 'POST',
            type: 'POST',
            cache: false,
            data: fd,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response != 0) {
                    $("#div_listado").html(response);
                } else {
                    alert('error al realizar la operacion, intentelo de nuevo');
                }
                div_loading_sup.className = '';
                div_loading_sup.innerHTML = '';

                div_loading_listado.className = '';
                div_loading_listado.innerHTML = '';
            },
            error: function (qXHR, textStatus, errorThrown) {
                console.log(errorThrown); console.log(qXHR); console.log(textStatus);
                div_loading_sup.className = '';
                div_loading_sup.innerHTML = '';

                div_loading_listado.className = '';
                div_loading_listado.innerHTML = '';
            },
        });
        //alert(result);
    }
    catch (e) {
        console.error(e);
        div_loading_sup.className = '';
        div_loading_sup.innerHTML = '';

        div_loading_listado.className = '';
        div_loading_listado.innerHTML = '';
    }

    return true;
}

async function escogerLinea(linea) {
    document.form_linea.linea.value = linea;
    url_main = document.forms['form_operation'].elements['url_main'].value;

    div_loading_sup = document.getElementById('loading_search');
    div_loading_sup.className = 'overlay';
    div_loading_sup.innerHTML = '<i class="fas fa-2x fa-sync-alt fa-spin"></i>';

    var fd_superior = new FormData(document.forms['form_linea']);
    fd_superior.append('parte_form', 'superior');
    let result33;
    try {
        result33 = await $.ajax({
            url: url_main,
            method: 'POST',
            type: 'POST',
            cache: false,
            data: fd_superior,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response != 0) {
                    $("#div_superior").html(response);
                } else {
                    alert('error al realizar la operacion, intentelo de nuevo');
                }
                div_loading_sup.className = '';
                div_loading_sup.innerHTML = '';
            },
            error: function (qXHR, textStatus, errorThrown) {
                console.log(errorThrown); console.log(qXHR); console.log(textStatus);
                div_loading_sup.className = '';
                div_loading_sup.innerHTML = '';
            },
        });
    }
    catch (e) {
        console.error(e);
        div_loading_sup.className = '';
        div_loading_sup.innerHTML = '';
    }

    //$("#div_listado").html(imagen);
    div_loading_listado = document.getElementById('loading_listado');
    div_loading_listado.className = 'overlay';
    div_loading_listado.innerHTML = '<i class="fas fa-2x fa-sync-alt fa-spin"></i>';

    var fd = new FormData(document.forms['form_linea']);
    fd.append('parte_form', 'listado');
    let result22;
    try {
        result22 = await $.ajax({
            url: url_main,
            method: 'POST',
            type: 'POST',
            cache: false,
            data: fd,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response != 0) {
                    $("#div_listado").html(response);
                } else {
                    alert('error al realizar la operacion, intentelo de nuevo');
                }
                div_loading_listado.className = '';
                div_loading_listado.innerHTML = '';
            },
            error: function (qXHR, textStatus, errorThrown) {
                console.log(errorThrown); console.log(qXHR); console.log(textStatus);
                div_loading_listado.className = '';
                div_loading_listado.innerHTML = '';
            },
        });
        //alert(result);
    }
    catch (e) {
        console.error(e);
        div_loading_listado.className = '';
        div_loading_listado.innerHTML = '';
    }

    return true;
}

//filtro de busqueda
function filtrarBusqueda() {
    p_search = Trim(document.getElementById('producto_search').value);
    if (p_search == '') {
        //busqueda por linea
        linea_actual = document.forms['form_linea'].elements['linea'].value;
        escogerLinea(linea_actual);
    }
    else {
        buscarProducto();
    }
}