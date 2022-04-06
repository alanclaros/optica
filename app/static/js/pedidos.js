
function sendSearchPedido() {
    sendFormObject('search', div_modulo);
}

//impresion de pedido
function imprimirPedido(pedido_id) {
    document.forms['form_print'].elements['id'].value = pedido_id;
    document.forms['form_print'].elements['operation_x'].value = 'print';
    document.forms['form_print'].submit();
}

function sendFormPedido(operation, message) {
    switch (operation) {
        case ('marcar_pedido'):

            modalFunction.value = 'pedidoSaveForm();';
            //set data modal
            modalSetParameters('success', 'center', 'Pedidos!', 'Esta seguro de querer marcar este pedido?', 'Cancelar', 'Guardar');
            modalF.modal();

            break;

        case ('anular'):
            modalFunction.value = 'pedidoAnular();';
            //set data modal
            modalSetParameters('danger', 'center', 'Pedidos!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
            modalF.modal();

            break;

        default:
            break;
    }
}

function pedidoSaveForm() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function pedidoAnular() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}