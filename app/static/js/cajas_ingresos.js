
function sendSearchCajaIngreso() {
	sendFormObject('search', div_modulo);
}

function sendFormCajaIngreso(operation, message) {
	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'cajaIngresoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Cajas Ingresos!', 'Esta seguro de querer adicionar este ingreso?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas Ingresos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaIngresoWarning();';
				modalF.modal();
			}
			break;

		case ('anular'):
			resValidation = controlModuloIngresoCaja();
			console.log('resvalidation: ', resValidation);

			if (resValidation === true) {
				modalFunction.value = 'cajaIngresoAnular();';
				//set data modal
				modalSetParameters('danger', 'center', 'Cajas Ingresos!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Cajas Ingresos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'cajaIngresoWarning();';
				modalF.modal();
			}
			break;

		default:
			break;
	}
}

function cajaIngresoSaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaIngresoWarning() {
	modalF.modal('toggle');
}

function cajaIngresoAnular() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//control especifico del modulo
function controlModuloIngresoCaja() {
	operation = document.getElementById('operation_x').value;
	if (operation == 'anular') {
		motivo = document.getElementById('motivo_anula');
		motivo_txt = Trim(motivo.value);
		if (motivo_txt == '') {
			return 'Debe llenar el motivo de anulacion';
		}
	}

	return true;
}
