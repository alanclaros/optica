

function module_pagination(page) {
	const token_pagination = document.forms['form_page'].elements['csrfmiddlewaretoken'].value;
	const module_x = document.forms['form_operation'].elements['module_x'].value;

	let datos_pagination = {
		'module_x': module_x,
		'csrfmiddlewaretoken': token_pagination,
	}
	const name_var_page = document.forms['form_page'].elements['name_var_page'].value;

	datos_pagination[name_var_page] = page;

	div_modulo.html(imagen_modulo);
	div_modulo.load(hostURL, datos_pagination, function () {
		//termina de cargar la ventana
		const setLink = hostURL + '/' + module_x;
		window.history.pushState({ href: setLink }, '', setLink);
	});
}

let cont_hide = 0;
function hideNotifications() {
	for (let im = 0; im <= 20; im++) {
		try {
			let existe_message;
			if (im == 0) {
				existe_message = document.getElementById('message');
				//alert(existe_message);
			}
			else {
				existe_message = document.getElementById('message' + im);
				//alert(existe_message);
			}

			if (existe_message != null) {
				if (cont_hide == 0) {
					cont_hide = 1;
				}
				else {
					cont_hide = 0;
					if (im == 0) {
						$('#message').stop(true);
						$('#message').fadeOut(5000);
					}
					else {
						$('#message' + im).stop(true);
						$('#message' + im).fadeOut(5000);
					}
				}
			}
		}
		catch (e) {

		}
	}
}

//de las notificaciones para abrir los menus
function notificacionAbrir(tipo) {
	if (document.getElementById('li_header_ventas')) {
		const li_header = document.getElementById('li_header_ventas');
		const href_header = $('#href_header_ventas');

		const clase_header = li_header.className;
		//console.log(clase_header);

		if (clase_header.toLowerCase() == 'nav-item has-treeview') {
			href_header.click();
		}

		if (tipo === 'pedido') {
			openModule('30');
		}
		if (tipo == 'reserva') {
			openModule('29');
		}
	}
}

function checkNotifications() {
	try {
		autenticado = document.forms['form_notificaciones'].elements['autenticado'].value;
	}
	catch (e) {
		autenticado = 'no';
	}

	if (autenticado == 'si') {
		try {
			const send_url = urlEmpresa + '/notificacionespagina/';
			const token = document.forms['form_notificaciones'].elements['csrfmiddlewaretoken'].value;
			const datos = {
				'check': 'ok',
				'csrfmiddlewaretoken': token,
			}

			//verificamos
			$('#div_notifications').fadeIn('slow');
			//$("#div_notifications").html(imagen);
			$("#div_notifications").load(send_url, datos, function () {
				//termina de cargar la ventana
				resultadoNotificacion();
			});
		}
		catch (e) {
			//error
		}
	}
}

//resultado de la notificacion
function resultadoNotificacion() {
	return true;
}

function openModule(module_id) {
	//alert(module_id);
	//console.log('open module, module_id: ', module_id);
	let checkModule = module_id;
	let moduleOperations = [];
	moduleOperations = checkModule.split('/');
	//console.log('module operations: ', moduleOperations);

	let module_aux = document.getElementById('module_ref_1000');
	module_aux.className = 'nav-link back_menu';

	//desmarcamos todos los posibles
	for (let mi = 1; mi <= 50; mi++) {
		try {
			module_aux = document.getElementById('module_ref_' + mi);
			module_aux.className = 'nav-link back_menu';
		}
		catch (e) {

		}
	}

	const module_ref = document.getElementById('module_ref_' + moduleOperations[0]);
	const token_module = document.forms['form_notificaciones'].elements['csrfmiddlewaretoken'].value;

	//select module
	module_ref.className = 'nav-link back_menu_item_select active';

	//un modulo con una operacion
	let datos_modulo = {};
	if (moduleOperations.length === 1) {
		datos_modulo = {
			'module_x': moduleOperations[0],
			'csrfmiddlewaretoken': token_module,
		}

		div_modulo.html(imagen_modulo);
		div_modulo.load(hostURL, datos_modulo, function (response) {
			const setURL = hostURL + '/' + moduleOperations[0];
			window.history.pushState({ href: setURL }, '', setURL);
		});
	}

	//un modulo con operaciones
	if (moduleOperations.length === 2) {
		//check id
		const posID = moduleOperations[1].indexOf('?');
		let forOperationX = moduleOperations[1];
		let varName = 'x';
		let varValue = 'x';
		if (posID > -1) {
			forOperationX = moduleOperations[1].substring(0, posID);
			//console.log('for operation x: ', forOperationX);
			const parametros = moduleOperations[1].substring(posID + 1, moduleOperations[1].length);
			//console.log('parametros...: ', parametros);
			const dataParametros = parametros.split('=');
			varName = dataParametros[0];
			varValue = dataParametros[1];
		}

		//console.log('varname: ', varName, ' varvalue: ', varValue);
		datos_modulo = {
			'module_x': moduleOperations[0],
			'operation_x': forOperationX,
			'csrfmiddlewaretoken': token_module,
		}
		datos_modulo[varName] = varValue;
		//console.log('datos modulo..: ', datos_modulo);

		div_modulo.html(imagen_modulo);
		div_modulo.load(hostURL, datos_modulo, function (response) {
			const setURL = hostURL + '/' + moduleOperations[0] + '/' + moduleOperations[1];
			window.history.pushState({ href: setURL }, '', setURL);
		});
	}

	//un modulo con submodulo y operaciones
	if (moduleOperations.length === 4) {
		//console.log('entra... length 4....');
		//check id
		const posID = moduleOperations[3].indexOf('?');
		let forOperationX = moduleOperations[2];
		let varName = 'x';
		let varValue = 'x';
		if (posID > -1) {
			forOperationX = moduleOperations[3].substring(0, posID);
			//console.log('for operation x: ', forOperationX);
			const parametros = moduleOperations[3].substring(posID + 1, moduleOperations[3].length);
			//console.log('parametros...: ', parametros);
			const dataParametros = parametros.split('=');
			varName = dataParametros[0];
			varValue = dataParametros[1];
		}

		datos_modulo = {
			'module_x': moduleOperations[0],
			'operation_x': moduleOperations[2],
			'operation_x2': forOperationX,
			'id': moduleOperations[1],
			'csrfmiddlewaretoken': token_module,
		}
		datos_modulo[varName] = varValue;
		//console.log('datos modulo..: ', datos_modulo);

		div_modulo.html(imagen_modulo);
		div_modulo.load(hostURL, datos_modulo, function (response) {
			const setURL = hostURL + '/' + moduleOperations[0] + '/' + moduleOperations[1] + '/' + moduleOperations[2] + '/' + moduleOperations[3];
			window.history.pushState({ href: setURL }, '', setURL);
		});
	}

	//close sidebar when select module (mobile devices)
	const div_body_class = document.getElementById('div_body').className;
	const pos = div_body_class.indexOf('open');
	if (pos > -1) {
		const btn_show_menu = document.getElementById('btn_show_menu');
		btn_show_menu.click();
	}




	// div_modulo.html(imagen_modulo);
	// // let para_cargar = url_empresa;
	// // if (para_cargar != '') {
	// // 	para_cargar = url_empresa + '/';
	// // }
	// //para_cargar = 'http://127.0.0.1:8000/';
	// const para_cargar = hostURL;
	// // const hostName = location.hostname;
	// // const host = location.host;
	// // const origin = location.origin;
	// // console.log('host: ', host, ' hostname: ', hostName, ' origin: ', origin);
	// //console.log('para cargar: ', para_cargar);

	// div_modulo.load(para_cargar, datos_modulo, function (response) {
	// 	//console.log('reponse...', response);
	// 	//termina de cargar la ventana

	// 	//console.log('response: ', response);
	// 	//document.title = 'modulo ' + module_id;
	// 	//window.history.pushState({ "html": response, "pageTitle": 'modulo ' + module_id }, "", module_id);
	// 	//window.history.pushState({ "html": response, "pageTitle": 'modulo ' + module_id }, response, module_id);
	// 	//window.history.pushState(response, 'modulo ' + module_id, module_id);
	// 	const setURL = hostURL + '/' + module_id;

	// 	window.history.pushState({ href: setURL }, '', setURL);
	// });

	// const div_body_class = document.getElementById('div_body').className;
	// const pos = div_body_class.indexOf('open');
	// if (pos > -1) {
	// 	const btn_show_menu = document.getElementById('btn_show_menu');
	// 	btn_show_menu.click();
	// }

}

//send order forms
function sendOrder(order, type, field_order, field_type) {
	const token_search = document.forms['form_order'].elements['csrfmiddlewaretoken'].value;
	const module_x = document.forms['form_operation'].elements['module_x'].value;

	let datos_search = {
		'csrfmiddlewaretoken': token_search,

		'module_x': module_x,
		'module_x2': document.forms['form_operation'].elements['module_x2'].value,
		'module_x3': document.forms['form_operation'].elements['module_x3'].value,

		'operation_x': document.forms['form_operation'].elements['operation_x'].value,
		'operation_x2': document.forms['form_operation'].elements['operation_x2'].value,
		'operation_x3': document.forms['form_operation'].elements['operation_x3'].value,

		'id': document.forms['form_operation'].elements['id'].value,
		'id2': document.forms['form_operation'].elements['id2'].value,
		'id3': document.forms['form_operation'].elements['id3'].value,
	}
	datos_search[field_order] = order;
	datos_search[field_type] = type;

	div_modulo.html(imagen_modulo);
	div_modulo.load(hostURL, datos_search, function () {
		//termina de cargar la ventana
		const setLink = hostURL + '/' + module_x;
		window.history.pushState({ href: setLink }, '', setLink);
	});
}

//boton de adicion
function sendOperation(operation = '', operation2 = '', operation3 = '', id = '', id2 = '', id3 = '') {
	const token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
	const module_x = document.forms['form_operation'].elements['module_x'].value;

	const datos_operation = {
		'csrfmiddlewaretoken': token_operation,

		'module_x': module_x,
		'module_x2': document.forms['form_operation'].elements['module_x2'].value,
		'module_x3': document.forms['form_operation'].elements['module_x3'].value,

		'operation_x': operation,
		'operation_x2': operation2,
		'operation_x3': operation3,

		'id': id,
		'id2': id2,
		'id3': id3,
	}
	//console.log('entra sendoperation: ', datos_operation);
	div_modulo.html(imagen_modulo);

	div_modulo.load(hostURL, datos_operation, function () {
		//termina de cargar la ventana
		//console.log('operation send operation: ', operation);
		let setLink = "";
		if (Trim(operation2) === '') {
			if (operation === 'delete' || operation === 'anular') {
				setLink = hostURL + '/' + module_x;
			}
			else {
				setLink = hostURL + '/' + module_x + '/' + operation + '?id=' + id;
			}
		}
		else {
			//submodulo
			if (operation2 === 'delete' || operation2 === 'anular') {
				setLink = hostURL + '/' + module_x + '/' + id + '/' + operation;
			}
			else {
				setLink = hostURL + '/' + module_x + '/' + id + '/' + operation + '/' + operation2 + '?id2=' + id2;
			}
		}

		//console.log('setlink...: ', setLink);
		//const setLink = hostURL + '/' + module_x + '/' + operation + '?id=' + id;
		window.history.pushState({ href: setLink }, '', setLink);
		//console.log('window history: ', window.history);
	});
}

function backWindow() {
	const token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
	const module_x = document.forms['form_operation'].elements['module_x'].value;

	const datos_operation = {
		'csrfmiddlewaretoken': token_operation,

		'module_x': document.forms['form_operation'].elements['module_x'].value,
	}

	div_modulo.html(imagen_modulo);
	div_modulo.load(hostURL, datos_operation, function () {
		//termina de cargar la ventana
		//window.history.pushState({ href: module_x }, '', module_x);
		window.history.pushState({ href: hostURL + '/' + module_x }, '', hostURL + '/' + module_x);
	});
}

function backWindow2() {
	const token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;
	const idPrincipal = document.forms['form_operation'].elements['id'].value;
	const operation_x = document.forms['form_operation'].elements['operation_x'].value;
	const module_x = document.forms['form_operation'].elements['module_x'].value;

	const datos_operation = {
		'csrfmiddlewaretoken': token_operation,

		'module_x': module_x,
		'module_x2': document.forms['form_operation'].elements['module_x2'].value,

		'operation_x': operation_x,

		'id': idPrincipal,
	}

	div_modulo.html(imagen_modulo);
	div_modulo.load(hostURL, datos_operation, function () {
		//termina de cargar la ventana
		const setLink = hostURL + '/' + module_x + '/' + idPrincipal + '/' + operation_x;
		//console.log('back window 2.....', setLink);
		window.history.pushState({ href: setLink }, '', setLink);
	});
}

function backWindow3() {
	const token_operation = document.forms['form_operation'].elements['csrfmiddlewaretoken'].value;

	const datos_operation = {
		'csrfmiddlewaretoken': token_operation,

		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'module_x2': document.forms['form_operation'].elements['module_x2'].value,
		'module_x3': document.forms['form_operation'].elements['module_x3'].value,

		'operation_x': document.forms['form_operation'].elements['operation_x'].value,
		'operation_x2': document.forms['form_operation'].elements['operation_x2'].value,

		'id': document.forms['form_operation'].elements['id'].value,
		'id2': document.forms['form_operation'].elements['id2'].value,
	}

	div_modulo.html(imagen_modulo);
	div_modulo.load(hostURL, datos_operation, function () {
		//termina de cargar la ventana
	});
}

function validarNumero(nombre) {
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
		if (letra == "1" || letra == "2" || letra == "3" || letra == "4" || letra == "5" || letra == "6" || letra == "7" || letra == "8" || letra == "9" || letra == "0") {
			nuevo_valor = nuevo_valor + letra;
		}
	}
	campo.value = nuevo_valor;
}

function validarNumeroPunto(nombre) {
	tipo = typeof (nombre);
	if (tipo == 'object') {
		campo = nombre;
	}
	if (tipo == "string") {
		campo = document.getElementById(nombre);
	}

	var tam = campo.value.length;
	var valor = "";
	var letra = "";
	var nuevo_valor = "";
	for (i = 0; i < tam; i++) {
		valor = campo.value.substring(i, (i + 1));
		letra = valor.toUpperCase();
		if (letra == "1" || letra == "2" || letra == "3" || letra == "4" || letra == "5" || letra == "6" || letra == "7" || letra == "8" || letra == "9" || letra == "0" || letra == ".") {
			nuevo_valor = nuevo_valor + letra;
		}
	}
	campo.value = nuevo_valor;
}

function validarNumeroPuntoNegativo(nombre) {
	tipo = typeof (nombre);
	if (tipo == 'object') {
		campo = nombre;
	}
	if (tipo == "string") {
		campo = document.getElementById(nombre);
	}

	var tam = campo.value.length;
	var valor = "";
	var letra = "";
	var nuevo_valor = "";
	for (i = 0; i < tam; i++) {
		valor = campo.value.substring(i, (i + 1));
		letra = valor.toUpperCase();
		if (letra == "1" || letra == "2" || letra == "3" || letra == "4" || letra == "5" || letra == "6" || letra == "7" || letra == "8" || letra == "9" || letra == "0" || letra == "." || letra == '-') {
			nuevo_valor = nuevo_valor + letra;
		}
	}
	campo.value = nuevo_valor;
}

function verifyForm() {
	//variables a controlar
	controlForm = TrimDerecha(TrimIzquierda(document.forms["formulario"].elements["control_form"].value));
	tam = controlForm.length;

	if (tam > 0) {
		var division = controlForm.split(";");
		tamC = division.length;

		for (i = 0; i < tamC; i++) {
			auxS = division[i];
			divisionC = auxS.split("|");
			tipoDato = divisionC[0];

			controlarDato = divisionC[2];
			nombreCampo = divisionC[3];
			nombreMostrar = divisionC[4];
			//console.log('nombre campo: ', nombreCampo);

			campoForm = document.getElementById(nombreCampo);
			valor = TrimDerecha(TrimIzquierda(campoForm.value));
			tamValor = valor.length;

			if (tipoDato == "txt" && controlarDato == "S") {
				tamDato = parseInt(divisionC[1]);

				if (tamValor == 0) {
					txtValid(nombreCampo);
					//alert('Debe llenar este campo');
					campoForm.focus();
					//return false;
					return 'Debe llenar este campo: ' + nombreMostrar;
				}
				if (tamValor < tamDato) {
					//alert('Este campo debe tener al menos ' + tamDato + ' letras');
					campoForm.focus();
					//return false;
					return nombreMostrar + ': debe tener al menos ' + tamDato + ' letras';
				}
			}

			if (tipoDato == "cbo" && controlarDato == "S") {
				noDato = divisionC[1];

				if (valor == noDato) {
					//alert('Debe seleccionar un valor');
					campoForm.focus();
					//return false;
					return 'Debe seleccionar un valor para: ' + nombreMostrar;
				}
			}
		} //fin for
	} // fin if tam>0

	return true;
}

function TrimDerecha(str) {
	var resultStr = "";
	var i = 0;

	// Return immediately if an invalid value was passed in
	if (str + "" == "undefined" || str == null)
		return null;

	// Make sure the argument is a string
	str += "";

	if (str.length == 0)
		resultStr = "";
	else {
		// Loop through string starting at the end as long as there
		// are spaces.
		i = str.length - 1;
		while ((i >= 0) && (str.charAt(i) == " "))
			i--;

		// When the loop is done, we're sitting at the last non-space char,
		// so return that char plus all previous chars of the string.
		resultStr = str.substring(0, i + 1);
	}

	return resultStr;
}

function TrimIzquierda(str) {
	var resultStr = "";
	var i = len = 0;

	// Return immediately if an invalid value was passed in
	if (str + "" == "undefined" || str == null)
		return null;

	// Make sure the argument is a string
	str += "";

	if (str.length == 0)
		resultStr = "";
	else {
		// Loop through string starting at the beginning as long as there
		// are spaces.
		//	  	len = str.length - 1;
		len = str.length;

		while ((i <= len) && (str.charAt(i) == " "))
			i++;

		// When the loop is done, we're sitting at the first non-space char,
		// so return that char plus the remaining chars of the string.
		resultStr = str.substring(i, len);
	}

	return resultStr;
}

function Trim(str) {
	resultado = TrimDerecha(TrimIzquierda(str));

	return resultado;
}

/**impresion, dialogo modal */
function closeModalPrint() {
	modal = document.getElementById("printModal");
	modal.style.display = "none";
}

function openModalPrint() {
	modal = document.getElementById("printModal");
	modal.style.display = "block";
}

function redondeo(numero, decimales) {
	var flotante = parseFloat(numero);
	var resultado = Math.round(flotante * Math.pow(10, decimales)) / Math.pow(10, decimales);
	resultado2 = resultado;
	var aux_c = "" + resultado;
	if (aux_c.indexOf('.') != -1) {
		//si hay decimales
		var division = aux_c.split(".");
		ta = division[1].length;
		if (ta == 1) {
			resultado2 = resultado + "0";
		}
	}
	else {
		//sin decimales
		resultado2 = resultado + ".00";
	}

	return resultado2;
}

/**valida campos de texto
 * mostrando rojo, si no lleno datos
 */
function txtValid(nombre) {
	tipo = typeof (nombre);
	if (tipo == 'object') {
		campo = nombre;
	}
	if (tipo == "string") {
		campo = document.getElementById(nombre);
	}
	//console.log('campo: ', campo.name);

	clase = campo.className;
	clase = clase.replace('is-invalid', '');
	campo_valor_actual = Trim(campo.value);

	//control con el formulario
	try {
		control_form_aux = Trim(document.forms['formulario'].elements['control_form'].value);
		if (control_form_aux != '') {
			div_form_aux = control_form_aux.split(';');
			for (iaux = 0; iaux < div_form_aux.length; iaux++) {
				auxValid = div_form_aux[iaux];
				divisionValid = auxValid.split("|");
				tipoDatoValid = divisionValid[0];
				controlarDatoValid = divisionValid[2];
				nombreCampoValid = divisionValid[3];

				if (tipoDatoValid == 'txt' && controlarDatoValid == 'S' && nombreCampoValid == campo.name) {
					tamDatoValid = parseInt(divisionValid[1]);

					if (campo_valor_actual.length < tamDatoValid) {
						clase = clase + ' is-invalid';
					}
				}

				if (tipoDatoValid == "cbo" && controlarDatoValid == "S" && nombreCampoValid == campo.name) {
					noDatoValid = divisionValid[1];
					if (campo_valor_actual == noDatoValid) {
						clase = clase + ' is-invalid';
					}
				}
			}
		}
		clase = clase.replace('  ', ' ');
		campo.className = clase;
	}
	catch (e) {
		//sin control form
		if (campo_valor_actual == '') {
			clase = clase + ' is-invalid';
		}
		clase = clase.replace('  ', ' ');
		campo.className = clase;
	}
}

//press success button 
function modalPressSuccess() {
	functionName = document.getElementById('modalFunctionSuccess').value;
	eval(functionName);
}

function modalSetParameters(type, position, title, body, btn_cancel, btn_success) {
	//header
	modalBackGround = document.getElementById('modalHeader');
	modalBackGround.className = 'modal-header modal_bg_' + type;
	//body
	modalBackGroundBody = document.getElementById('modalBodyBG');
	modalBackGroundBody.className = 'modal-body modal_bg_body_' + type;
	//footer
	modalBackGroundFooter = document.getElementById('modalFooterBG');
	modalBackGroundFooter.className = 'modal-footer justify-content-between modal_bg_footer_' + type;
	//console.log(modalBackGround.className);

	modalPos = document.getElementById('modalPosition');
	defPosition = "modal-dialog";
	if (position == 'center') {
		defPosition = "modal-dialog modal-dialog-centered";
	}
	modalPos.className = defPosition;

	mTitle = document.getElementById('modalTitle');
	mTitle.innerHTML = title;
	mBody = document.getElementById('modalBody');
	mBody.innerHTML = body;
	mBtnCancel = document.getElementById('modalButtonCancel');
	mBtnCancel.innerHTML = btn_cancel;
	mBtnSuccess = document.getElementById('modalButtonSuccess');
	mBtnSuccess.innerHTML = btn_success;
	// if (type === 'danger') {
	// 	mBtnSuccess.className = 'btn btn-danger';
	// }
	// else {
	// 	mBtnSuccess.className = 'btn btn-primary';
	// }
}

function modalPrintSetParameters(type, position, title, body, btn_cancel, btn_success) {
	//header
	modalBackGround = document.getElementById('modalPrintHeader');
	modalBackGround.className = 'modal-header modal_bg_' + type;
	//body
	modalBackGroundBody = document.getElementById('modalPrintBodyBG');
	modalBackGroundBody.className = 'modal-body modal_bg_body_' + type;
	//footer
	modalBackGroundFooter = document.getElementById('modalPrintFooterBG');
	modalBackGroundFooter.className = 'modal-footer justify-content-between modal_bg_footer_' + type;
	//console.log(modalBackGround.className);

	// modalPos = document.getElementById('modalPrintPosition');
	// defPosition = "modal-dialog";
	// if (position == 'center') {
	// 	//defPosition = "modal-dialog modal-dialog-centered";
	// 	defPosition = "modal-dialog-centered modal-sm";
	// }
	// modalPos.className = defPosition;

	mTitle = document.getElementById('modalPrintTitle');
	mTitle.innerHTML = title;
	mBody = document.getElementById('modalPrintBody');
	mBody.innerHTML = body;
	mBtnCancel = document.getElementById('modalPrintB1');
	mBtnCancel.innerHTML = btn_cancel;
	mBtnSuccess = document.getElementById('modalPrintB2');
	mBtnSuccess.innerHTML = btn_success;
}

//press success button 
function modalPrintPressB1() {
	const functionName = document.getElementById('modalPrintFunctionB1').value;
	eval(functionName);
}
function modalPrintPressB2() {
	const functionName = document.getElementById('modalPrintFunctionB2').value;
	eval(functionName);
}

async function sendFormObject(formName, divLoad) {
	var fd = new FormData(document.forms[formName]);

	divLoad.html(imagen_modulo);
	let result;
	try {
		result = await $.ajax({
			url: hostURL,
			method: 'POST',
			type: 'POST',
			cache: false,
			data: fd,
			contentType: false,
			processData: false,
			success: function (response) {
				if (response != 0) {
					divLoad.html(response);
					let currentLink = location.href;
					//console.log('current link: ', currentLink, ' host url: ', hostURL);
					currentLink = currentLink.replace(hostURL + '/', '');
					let moduleOperations = [];
					moduleOperations = currentLink.split('/');
					const setLink = hostURL + '/' + moduleOperations[0];
					window.history.pushState({ href: setLink }, '', setLink);
				} else {
					alert('error al realizar la operacion, intentelo de nuevo');
				}
			},
			error: function (qXHR, textStatus, errorThrown) {
				console.log(errorThrown); console.log(qXHR); console.log(textStatus);
			},
		});
		//alert(result);
	}
	catch (e) {
		console.error(e);
	}
}

async function sendFormObjectImg(formName, divLoad, img) {
	var fd = new FormData(document.forms[formName]);

	// Display the key/value pairs
	// for (var pair of formData.entries()) {
	// 	console.log(pair[0]+ ', ' + pair[1]); 
	// }

	divLoad.html(img);

	let result;

	try {
		result = await $.ajax({
			url: hostURL,
			method: 'POST',
			type: 'POST',
			cache: false,
			data: fd,
			contentType: false,
			processData: false,
			success: function (response) {
				if (response != 0) {
					divLoad.html(response);
				} else {
					alert('error al realizar la operacion, intentelo de nuevo');
				}
			},
			error: function (qXHR, textStatus, errorThrown) {
				console.log(errorThrown); console.log(qXHR); console.log(textStatus);
			},
		});
		//alert(result);
	}
	catch (e) {
		console.error(e);
	}
}

function sleep(milliseconds) {
	var start = new Date().getTime();
	for (var i = 0; i < 1e7; i++) {
		if ((new Date().getTime() - start) > milliseconds) {
			break;
		}
	}
}

function getFechaFormatoDB(fecha) {
	const division = fecha.split('-');
	const dia = division[0];
	const aux_mes = division[1];
	const anio = division[2];
	let mes = '';
	switch (aux_mes) {
		case 'Ene':
			mes = '01';
			break;
		case 'Feb':
			mes = '02';
			break;
		case 'Mar':
			mes = '03';
			break;
		case 'Abr':
			mes = '04';
			break;
		case 'May':
			mes = '05';
			break;
		case 'Jun':
			mes = '06';
			break;
		case 'Jul':
			mes = '07';
			break;
		case 'Ago':
			mes = '08';
			break;
		case 'Sep':
			mes = '09';
			break;
		case 'Oct':
			mes = '10';
			break;
		case 'Nov':
			mes = '11';
			break;
		case 'Dic':
			mes = '12';
			break;
	}
	return anio + mes + dia;
}