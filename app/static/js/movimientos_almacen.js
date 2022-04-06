
function sendSearchMA() {
    sendFormObject('search', div_modulo);
}

function sendFormMA(operation, message) {
    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'MASaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Movimientos Almacen!', 'Esta seguro de querer adicionar este movimiento de Almacen?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Movimientos Almacen!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'MAWarning();';
                modalF.modal();
            }
            break;

        case ('anular'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'MAAnular();';
                //set data modal
                modalSetParameters('danger', 'center', 'Movimientos Almacen!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Movimientos Almacen!', resValidation, 'Cancelar', 'Volver');
                //function cancel
                modalFunction.value = 'MAWarning();';
                modalF.modal();
            }

            break;

        default:
            break;
    }
}

function MASaveForm() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function MAWarning() {
    modalF.modal('toggle');
}

function MAAnular() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function seleccionPMA(tipo_montura, nombre_montura, montura_id) {
    const tp = document.getElementById(tipo_montura);
    tp.value = montura_id;
    maSeleccionAlmacenMontura();
}

function maSeleccionAlmacenMontura() {
    const almacen = document.getElementById('almacen').value;
    const almacen2 = document.getElementById('almacen2').value;
    const tipo_montura = document.getElementById('tipo_montura').value;

    const listado = $('#div_listap');
    const listado_stock = $('#div_listado_stock');

    token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

    datos = {
        'module_x': document.forms['form_operation'].elements['module_x'].value,
        'operation_x': 'stock_monturas',
        'tipo_montura_id': tipo_montura,
        'almacen_id': almacen,
        'csrfmiddlewaretoken': token
    }

    listado_stock.html(imgLoading);
    listado_stock.load(hostURL, datos, function () {
        //termina de cargar la ventana
    });

    if (almacen != '0' && almacen2 != '0' && tipo_montura != '0') {
        listado.fadeIn('slow');
    }
    else {
        listado.fadeOut('slow');
    }
}

function maSeleccionStock(numero_registro, producto, id) {
    //verificamos que no repita monturas
    for (i = 1; i <= 50; i++) {
        aux_p = document.getElementById('stock_' + i);
        if (parseInt(numero_registro) != i && aux_p.value == id) {
            //alert('ya selecciono este producto');
            tb2 = document.getElementById('tb2_' + numero_registro);
            tb2.focus();
            tb2.value = '';
            modalSetParameters('warning', 'center', 'Salidas Almacen!', 'ya selecciono esta montura', 'Cancelar', 'Volver');
            modalFunction.value = 'SAWarning();';
            modalF.modal();
            return false;
        }
    }

    //asignamos el id del stock
    obj_aux = document.getElementById("stock_" + numero_registro);
    obj_aux.value = id;

    //alert(numero);alert(id);
    numero = parseInt(numero_registro);
    numero_int = numero + 1;
    if (numero_int <= 50) {
        numero_str = numero_int.toString();
        nombre_actual = "fila_" + numero_str;
        //alert(nombre_actual);
        objeto_actual = document.getElementById(nombre_actual);
        //objeto_actual.style.display = "block";
        objeto_actual.style.display = "";
    }
}
