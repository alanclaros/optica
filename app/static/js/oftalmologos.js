
function mostrarImagenOftalmologo(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchOftalmologo() {
    sendFormObject('search', div_modulo);
}

function sendFormOftalmologo(operation, message) {
    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'oftalmologoSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Oftalmologos!', 'Esta seguro de querer adicionar esta oftalmologo?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Oftalmologos!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'oftalmologoWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'oftalmologoSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Oftalmologos!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Oftalmologos!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'oftalmologoWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'oftalmologoDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Oftalmologos!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function oftalmologoSaveForm() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function oftalmologoWarning() {
    modalF.modal('toggle');
}

function oftalmologoDelete() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}