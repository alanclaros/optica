
function mostrarImagenTipoMontura(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchTipoMontura() {
    sendFormObject('search', div_modulo);
}

function sendFormTipoMontura(operation, message) {
    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'tipoMonturaSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Tipos Montura!', 'Esta seguro de querer adicionar este tipo de montura?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Tipos Montura!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'tipoMonturaWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'tipoMonturaSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Tipos Montura!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Tipos Montura!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'tipoMonturaWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'tipoMonturaDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Tipos Montura!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function tipoMonturaSaveForm() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function tipoMonturaWarning() {
    modalF.modal('toggle');
}

function tipoMonturaDelete() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}