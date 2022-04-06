
function sendSearchSA() {
	sendFormObject('search', div_modulo);
}

function sendFormSA(operation, message) {
	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'SASaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Salidas Almacen!', 'Esta seguro de querer adicionar esta salida de Almacen?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Salidas Almacen!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'SAWarning();';
				modalF.modal();
			}
			break;

		case ('anular'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'SAAnular();';
				//set data modal
				modalSetParameters('danger', 'center', 'Salidas Almacen!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Salidas Almacen!', resValidation, 'Cancelar', 'Volver');
				//function cancel
				modalFunction.value = 'SAWarning();';
				modalF.modal();
			}

			break;

		default:
			break;
	}
}

function SASaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function SAWarning() {
	modalF.modal('toggle');
}

function SAAnular() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function seleccionPSA(tipo_montura, nombre_montura, montura_id) {
	const tp = document.getElementById(tipo_montura);
	tp.value = montura_id;
	saSeleccionAlmacenMontura();
}

function saSeleccionAlmacenMontura() {
	const almacen = document.getElementById('almacen').value;
	const tipo_montura = document.getElementById('tipo_montura').value;

	const listado = $('#div_listap');
	const listado_stock = $('#div_listado_stock');

	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

	datos = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'stock_monturas',
		'tipo_montura_id': tipo_montura,
		'almacen_id': almacen,
		'csrfmiddlewaretoken': token
	}

	listado_stock.html(imgLoading);
	listado_stock.load(hostURL, datos, function () {
		//termina de cargar la ventana
	});

	if (almacen != '0' && tipo_montura != '0') {
		listado.fadeIn('slow');
	}
	else {
		listado.fadeOut('slow');
	}
}

function saSeleccionStock(numero_registro, producto, id) {
	//verificamos que no repita monturas
	for (i = 1; i <= 50; i++) {
		aux_p = document.getElementById('stock_' + i);
		if (parseInt(numero_registro) != i && aux_p.value == id) {
			//alert('ya selecciono este producto');
			tb2 = document.getElementById('tb2_' + numero_registro);
			tb2.focus();
			tb2.value = '';
			modalSetParameters('warning', 'center', 'Salidas Almacen!', 'ya selecciono esta montura', 'Cancelar', 'Volver');
			modalFunction.value = 'SAWarning();';
			modalF.modal();
			return false;
		}
	}

	//asignamos el id del stock
	obj_aux = document.getElementById("stock_" + numero_registro);
	obj_aux.value = id;

	//alert(numero);alert(id);
	numero = parseInt(numero_registro);
	numero_int = numero + 1;
	if (numero_int <= 50) {
		numero_str = numero_int.toString();
		nombre_actual = "fila_" + numero_str;
		//alert(nombre_actual);
		objeto_actual = document.getElementById(nombre_actual);
		//objeto_actual.style.display = "block";
		objeto_actual.style.display = "";
	}
}
