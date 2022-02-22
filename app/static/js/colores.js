
function sendSearchColor() {
    div_modulo = $("#div_block_content");
    sendFormObject('search', div_modulo);
}

function sendFormColor(operation, message) {
    //modal function
    modalFunction = document.getElementById('modalFunctionSuccess');
    modalF = $('#modalForm');

    switch (operation) {
        case ('add'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'colorSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Colores!', 'Esta seguro de querer adicionar este color?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Colores!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'colorWarning();';
                modalF.modal();
            }
            break;

        case ('modify'):
            resValidation = verifyForm();
            if (resValidation === true) {
                modalFunction.value = 'colorSaveForm();';
                //set data modal
                modalSetParameters('success', 'center', 'Colores!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
                modalF.modal();
            }
            else {
                //set data modal
                modalSetParameters('warning', 'center', 'Colores!', resValidation, 'Cancelar', 'Volver');

                //function cancel
                modalFunction.value = 'colorWarning();';
                modalF.modal();
            }
            break;

        case ('delete'):
            modalFunction.value = 'colorDelete();';
            //set data modal
            modalSetParameters('danger', 'center', 'Colores!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
            modalF.modal();

            break;

        default:
            break;
    }
}

function colorSaveForm() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function colorWarning() {
    modalF = $('#modalForm');
    modalF.modal('toggle');
}

function colorDelete() {
    modalF = $('#modalForm');
    div_modulo = $("#div_block_content");

    modalF.modal('toggle');
    document.forms['formulario'].elements['add_button'].disabled = true;
    document.forms['formulario'].elements['button_cancel'].disabled = true;

    sendFormObject('formulario', div_modulo);
}

function coloresChangeColor() {
    try {
        txt_color = Trim(document.getElementById('color_hex').value);
        console.log('color: ', txt_color);
        txt_muestra = document.getElementById('color_muestra');
        if (txt_color.length == 7) {
            txt_muestra.style.backgroundColor = txt_color;
        }
    }
    catch (e) {

    }
}