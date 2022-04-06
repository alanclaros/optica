
function sendSearchCajaEgreso() {
	sendFormObject('search', div_modulo);
}

function sendFormCajaEgreso(operation, message) {
	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'cajaEgresoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Cajas Egresos!', 'Esta seguro de querer adicionar este egreso?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas Egresos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaEgresoWarning();';
				modalF.modal();
			}
			break;

		case ('anular'):
			resValidation = controlModuloEgresoCaja();

			if (resValidation === true) {
				modalFunction.value = 'cajaEgresoAnular();';
				//set data modal
				modalSetParameters('danger', 'center', 'Cajas Egresos!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas Egresos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaEgresoWarning();';
				modalF.modal();
			}
			break;

		default:
			break;
	}
}

function cajaEgresoSaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaEgresoWarning() {
	modalF.modal('toggle');
}

function cajaEgresoAnular() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//control especifico del modulo
function controlModuloEgresoCaja() {
	operation = document.getElementById('operation_x').value;
	if (operation == 'anular') {
		motivo = document.getElementById('motivo_anula');
		motivo_txt = TrimDerecha(TrimIzquierda(motivo.value));
		if (motivo_txt == '') {
			return 'Debe llenar el motivo de anulacion';
		}
	}

	return true;
}
