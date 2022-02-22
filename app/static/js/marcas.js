
function mostrarImagenMarca(id) {
    document.form_img.id.value = id;
    document.form_img.submit();
}

function sendSearchMarca() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormMarca(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'marcaSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Marcas!', 'Esta seguro de querer adicionar esta marca?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Marcas!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'marcaWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'marcaSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Marcas!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Marcas!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'marcaWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'marcaDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Marcas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function marcaSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function marcaWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function marcaDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}