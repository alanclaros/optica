
function sendSearchIA() {
	sendFormObject('search', div_modulo);
}

function sendFormIA(operation, message) {
	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'IASaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Ingresos Almacen!', 'Esta seguro de querer adicionar este ingreso a Almacen?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Ingresos Almacen!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'IAWarning();';
				modalF.modal();
			}
			break;

		case ('anular'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'IAAnular();';
				//set data modal
				modalSetParameters('danger', 'center', 'Ingresos Almacen!', 'Esta seguro de querer anular ' + message + '?', 'Cancelar', 'Anular');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Ingresos Almacen!', resValidation, 'Cancelar', 'Volver');
				//function cancel
				modalFunction.value = 'IAWarning();';
				modalF.modal();
			}

			break;

		default:
			break;
	}
}

function IASaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function IAWarning() {
	modalF.modal('toggle');
}

function IAAnular() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function seleccionPIA(tipo_montura, nombre_montura, montura_id) {
	//console.log('nombre montura: ', nombre_montura);
	//console.log('montura id: ', montura_id);
	const tp = document.getElementById(tipo_montura);
	tp.value = montura_id;
	iaSeleccionAlmacenMontura();
}

function iaGetNombreMontura(nombre) {
	if (Trim(nombre) != '') {
		const pos = nombre.lastIndexOf('(');
		if (pos < 0) {
			return '';
		}
		const retorno = nombre.substring(0, pos);
		return retorno;
	}
	else {
		return '';
	}
}

function iaGetNumeroMontura(nombre) {
	if (Trim(nombre) != '') {
		const pos = nombre.lastIndexOf('(');
		if (pos < 0) {
			return 0;
		}
		const retorno = parseInt(nombre.substring(pos + 1, nombre.length - 1));
		return retorno;
	}
	else {
		return 0;
	}
}

function iaSeleccionAlmacenMontura() {
	const almacen = document.getElementById('almacen').value;
	const tipo_montura = document.getElementById('tipo_montura').value;

	const listado = $('#div_listap');

	if (almacen != '0' && tipo_montura != '0') {
		listado.fadeIn('slow');
	}
	else {
		listado.fadeOut('slow');
	}

	for (let i = 1; i <= 50; i++) {
		const obj_aux = document.getElementById("fila_" + i);
		const objMontura = document.getElementById("tipo_montura_nombre_" + i);
		const objCantidad = document.getElementById("cantidad_" + i);
		const objCosto = document.getElementById("costo_" + i);
		const objTotal = document.getElementById("total_" + i);
		if (i == 1) {
			obj_aux.style.display = '';
			objMontura.value = "";
		}
		else {
			obj_aux.style.display = 'none';
		}
		objMontura.value = '';
		objCantidad.value = '';
		objCosto.value = '';
		objTotal.value = '';
	}
}

function iaGenerar() {
	const almacen = document.getElementById('almacen');
	const tipo_montura = document.getElementById('tipo_montura');
	const cantidad = Trim(document.getElementById('cantidad_montura').value);
	const tipo_montura_nombre = document.getElementById('tb2_tipo_montura').value;

	const nombre = iaGetNombreMontura(tipo_montura_nombre);
	const actual = iaGetNumeroMontura(tipo_montura_nombre);

	let cantidad_int = 0;
	if (cantidad.length > 0) {
		cantidad_int = parseInt(cantidad);
	}

	if (almacen.value == '0') {
		modalSetParameters('warning', 'center', 'Ingresos Almacen!', 'Debe seleccionar un almacen', 'Cancelar', 'Volver');
		modalFunction.value = 'IAWarning();';
		modalF.modal();
		return false;
	}

	if (tipo_montura.value == '0') {
		modalSetParameters('warning', 'center', 'Ingresos Almacen!', 'Debe seleccionar un tipo de montura', 'Cancelar', 'Volver');
		modalFunction.value = 'IAWarning();';
		modalF.modal();
		return false;
	}

	if (cantidad_int <= 0 || cantidad_int > 50) {
		modalSetParameters('warning', 'center', 'Ingresos Almacen!', 'Debe ingresar una cantidad entre 1 y 50', 'Cancelar', 'Volver');
		modalFunction.value = 'IAWarning();';
		modalF.modal();
		return false;
	}

	const listado = $('#div_listap');
	listado.fadeIn('slow');
	let cont = 1;

	for (let i = 1; i <= 50; i++) {
		const obj_aux = document.getElementById("fila_" + i);
		const objMontura = document.getElementById("tipo_montura_nombre_" + i);
		const objCantidad = document.getElementById("cantidad_" + i);
		const objCosto = document.getElementById("costo_" + i);
		const objTotal = document.getElementById("total_" + i);

		if (i <= cantidad_int) {
			obj_aux.style.display = '';
			objMontura.value = nombre + ' (' + (actual + cont).toString() + ')';
			objCantidad.value = '1';
			objCosto.value = '1';
			objTotal.value = '1';
			cont = cont + 1;
		}
		else {
			obj_aux.style.display = 'none';
			objMontura.value = '';
			objCantidad.value = '';
			objCosto.value = '';
			objTotal.value = '';
		}
	}
	calcularTotalesIA();
}

//calculamos el total
function calcularTotalesIA() {
	limite = 50;

	total_todo = 0;

	for (i = 1; i <= limite; i++) {
		cantidad = document.getElementById("cantidad_" + i.toString());
		costo = document.getElementById("costo_" + i.toString());
		total = document.getElementById("total_" + i.toString());

		//valores
		cantidad_s = Trim(cantidad.value);
		costo_s = Trim(costo.value);

		if (cantidad_s != "" && costo_s != "") {
			total_v = parseFloat(cantidad_s) * parseFloat(costo_s);
			total_v2 = redondeo(total_v, 2);
			total_todo = total_todo + parseFloat(total_v2);
			total.value = total_v2;
		}
	}

	obj_total = document.getElementById('total');
	obj_total.value = redondeo(total_todo, 2);
}

