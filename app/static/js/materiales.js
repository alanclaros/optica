
function mostrarImagenMaterial(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchMaterial() {
    //div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormMaterial(operation, message) {
    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'materialSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Materiales!', 'Esta seguro de querer adicionar este material?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Materiales!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'materialWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'materialSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Materiales!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Materiales!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'materialWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'materialDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Materiales!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function materialSaveForm() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function materialWarning() {
    modalF.modal('toggle');
}

function materialDelete() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}