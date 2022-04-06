
function mostrarImagenLaboratorio(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchLaboratorio() {
    sendFormObject('search', div_modulo);
}

function sendFormLaboratorio(operation, message) {
    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'laboratorioSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Laboratorios!', 'Esta seguro de querer adicionar este laboratorio?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Laboratorios!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'laboratorioWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'laboratorioSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Laboratorios!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Laboratorios!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'laboratorioWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'laboratorioDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Laboratorios!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function laboratorioSaveForm() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function laboratorioWarning() {
    modalF.modal('toggle');
}

function laboratorioDelete() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}
