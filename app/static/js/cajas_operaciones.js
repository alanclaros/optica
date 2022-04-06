

//inicio de caja
function sendFormCajaIniciar(operation, message) {
	switch (operation) {
		case ('add'):
			modalFunction.value = 'cajaIniciarSaveForm();';
			//set data modal
			modalSetParameters('success', 'center', 'Cajas!', 'Esta seguro de iniciar esta Caja?', 'Cancelar', 'Guardar');
			modalF.modal();
			break;

		case ('delete'):
			modalFunction.value = 'cajaIniciarDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Cajas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();
			break;

		default:
			break;
	}
}

function cajaIniciarSaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaIniciarDelete() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//recepcion de caja
function sendFormCajaIniciarRecibir(operation, message) {
	switch (operation) {
		case ('add'):
			modalFunction.value = 'cajaIniciarRecibirSaveForm();';
			//set data modal
			modalSetParameters('success', 'center', 'Cajas!', 'Esta seguro de recibir esta Caja?', 'Cancelar', 'Guardar');
			modalF.modal();
			break;

		case ('delete'):
			modalFunction.value = 'cajaIniciarRecibirDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Cajas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();
			break;

		default:
			break;
	}
}

function cajaIniciarRecibirSaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaIniciarRecibirDelete() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//cierre de caja
function sendFormCajaCerrar(operation, message) {
	switch (operation) {
		case ('add'):
			modalFunction.value = 'cajaCerrarSaveForm();';
			//set data modal
			modalSetParameters('success', 'center', 'Cajas!', 'Esta seguro de cerrar esta Caja?', 'Cancelar', 'Guardar');
			modalF.modal();
			break;

		case ('delete'):
			modalFunction.value = 'cajaCerrarDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Cajas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();
			break;

		default:
			break;
	}
}

function cajaCerrarSaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaCerrarDelete() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//cierre de caja recibir
function sendFormCajaCerrarRecibir(operation, message) {
	switch (operation) {
		case ('add'):
			modalFunction.value = 'cajaCerrarRecibirSaveForm();';
			//set data modal
			modalSetParameters('success', 'center', 'Cajas!', 'Esta seguro de cerrar esta Caja?', 'Cancelar', 'Guardar');
			modalF.modal();
			break;

		case ('delete'):
			modalFunction.value = 'cajaCerrarRecibirDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Cajas!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();
			break;

		default:
			break;
	}
}

function cajaCerrarRecibirSaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function cajaCerrarRecibirDelete() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//validando monedas
function validarNumeroCO(nombre) {
	tipo = typeof (nombre);
	if (tipo == 'object') {
		campo = nombre;
	}
	if (tipo == "string") {
		campo = document.getElementById(nombre);
	}
	//alert(campo);
	var tam = campo.value.length;
	var valor = "";
	var letra = "";
	var nuevo_valor = "";
	for (i = 0; i < tam; i++) {
		valor = campo.value.substring(i, (i + 1));
		letra = valor.toUpperCase();
		if (letra == "1" || letra == "2" || letra == "3" || letra == "4" || letra == "5" || letra == "6" || letra == "7" || letra == "8" || letra == "9" || letra == "0" || letra == "-") {
			nuevo_valor = nuevo_valor + letra;
		}
	}
	campo.value = nuevo_valor;

	lista_monedas = document.getElementById('lista_monedas').value;
	div = lista_monedas.split('||');
	total = 0;
	for (i = 0; i < div.length; i++) {
		div2 = div[i].split('|');
		aux = 'moneda_' + div2[0];
		moneda = TrimDerecha(TrimIzquierda(document.getElementById(aux).value));
		if (moneda.length > 0) {
			total = total + (parseFloat(moneda) * parseFloat(div2[1]));
		}
	}

	//total
	objeto = document.getElementById('total');
	objeto.value = redondeo(total, 2);
}
