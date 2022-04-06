
function sendSearchCliente() {
	sendFormObject('search', div_modulo);
}

function sendFormCliente(operation, message) {
	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'clienteSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Clientes!', 'Esta seguro de querer adicionar este cliente?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Clientes!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'clienteWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'clienteSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Clientes!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Clientes!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'clienteWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'clienteDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Clientes!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function clienteSaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function clienteWarning() {
	modalF.modal('toggle');
}

function clienteDelete() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}