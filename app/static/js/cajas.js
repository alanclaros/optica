
function sendSearchCaja() {
	sendFormObject('search', div_modulo);
}

function sendFormCaja(operation, message) {
	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'cajaSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Cajas!', 'Esta seguro de querer adicionar esta Caja?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'cajaSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Cajas!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'cajaDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Cajas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function cajaSaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaWarning() {
	modalF.modal('toggle');
}

function cajaDelete() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}
