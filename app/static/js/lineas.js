
function mostrarImagenLinea(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchLinea() {
    sendFormObject('search', div_modulo);
}

function sendFormLinea(operation, message) {
    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'lineaSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Lineas!', 'Esta seguro de querer adicionar esta linea?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Lineas!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'lineaWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'lineaSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Lineas!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Lineas!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'lineaWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'lineaDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Lineas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function lineaSaveForm() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function lineaWarning() {
    modalF.modal('toggle');
}

function lineaDelete() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}