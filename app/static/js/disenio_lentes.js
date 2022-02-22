
function mostrarImagenDisenioLente(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchDisenioLente() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormDisenioLente(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'disenioLenteSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Disenio Lentes!', 'Esta seguro de querer adicionar este disenio de lentes?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Disenio Lentes!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'disenioLenteWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'disenioLenteSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Disenio Lentes!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Disenio Lentes!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'disenioLenteWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'disenioLenteDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Disenio Lentes!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function disenioLenteSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function disenioLenteWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function disenioLenteDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}