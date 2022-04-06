
function mostrarImagenTecnico(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchTecnico() {
    sendFormObject('search', div_modulo);
}

function sendFormTecnico(operation, message) {
    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'tecnicoSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Tecnicos!', 'Esta seguro de querer adicionar este tecnico?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Tecnicos!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'tecnicoWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'tecnicoSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Tecnicos!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Tecnicos!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'tecnicoWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'tecnicoDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Tecnicos!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function tecnicoSaveForm() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function tecnicoWarning() {
    modalF.modal('toggle');
}

function tecnicoDelete() {
    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}