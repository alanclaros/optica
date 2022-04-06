
//guardamos
function mandarFormularioConfiguracion() {
	resValidation = verifyForm();

	if (resValidation === true) {
		modalFunction.value = 'configuracionesSaveForm();';
		//set data modal
		modalSetParameters('success', 'center', 'Configuraciones!', 'Esta seguro de querer guardar los datos?', 'Cancelar', 'Guardar');
		modalF.modal();
	}
	else {
		//set data modal
		modalSetParameters('warning', 'center', 'Configuraciones!', resValidation, 'Cancelar', 'Volver');

		//function cancel
		modalFunction.value = 'configuracionesWarning(modalF);';
		modalF.modal();
	}
}

function configuracionesSaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function configuracionesWarning(modalF) {
	modalF.modal('toggle');
}