
//control especifico del modulo
function sendSearchProducto() {
	sendFormObject('search', div_modulo);
}

function sendFormProducto(operation, message) {
	switch (operation) {
		case ('add'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'productoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Productos!', 'Esta seguro de querer adicionar este producto?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Productos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'productoWarning();';
				modalF.modal();
			}
			break;

		case ('modify'):
			resValidation = verifyForm();
			if (resValidation === true) {
				modalFunction.value = 'productoSaveForm();';
				//set data modal
				modalSetParameters('success', 'center', 'Productos!', 'Esta seguro de querer guardar estos datos?', 'Cancelar', 'Guardar');
				modalF.modal();
			}
			else {
				//set data modal
				modalSetParameters('warning', 'center', 'Productos!', resValidation, 'Cancelar', 'Volver');

				//function cancel
				modalFunction.value = 'productoWarning();';
				modalF.modal();
			}
			break;

		case ('delete'):
			modalFunction.value = 'productoDelete();';
			//set data modal
			modalSetParameters('danger', 'center', 'Productos!', 'Esta seguro de querer eliminar ' + message + '?', 'Cancelar', 'Eliminar');
			modalF.modal();

			break;

		default:
			break;
	}
}

function productoSaveForm() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

function productoWarning() {
	modalF.modal('toggle');
}

function productoDelete() {
	modalF.modal('toggle');
	document.forms['formulario'].elements['add_button'].disabled = true;
	document.forms['formulario'].elements['button_cancel'].disabled = true;

	sendFormObject('formulario', div_modulo);
}

//busqueda de productos relacionados
function buscarProductosRelacionados() {

	linea = Trim(document.getElementById('br_linea').value);
	producto = Trim(document.getElementById('br_producto').value);
	codigo = Trim(document.getElementById('br_codigo').value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

	operation_mandar = document.forms['form_operation'].elements['operation_x'].value;
	pid = document.forms['form_operation'].elements['id'].value;

	datos_busqueda = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'buscar_producto_relacionado',
		'linea': linea,
		'producto': producto,
		'codigo': codigo,
		'operation_mandar': operation_mandar,
		'pid': pid,
		'csrfmiddlewaretoken': token,
	}

	$("#div_busqueda_relacionados").html(imgLoading);
	$("#div_busqueda_relacionados").load(hostURL, datos_busqueda, function () {
		//termina de cargar ajax
	});
}

//minimizar busqueda productos relacionados
function minimizarBusquedaRelacionado() {
	$("#div_busqueda_relacionados").html('<i>resultado busqueda</i>');
}

//selecionamos el producto relacionado
function seleccionarProductoRelacionado(producto_id) {
	producto_nombre = Trim(document.getElementById('productor_nombre_' + producto_id).value);

	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

	datos_producto = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'producto_relacionado',
		'producto_id': producto_id,
		'producto': producto_nombre,
		'csrfmiddlewaretoken': token,
	}

	$("#lista_productos_relacionados").html(imgLoading);
	$("#lista_productos_relacionados").load(hostURL, datos_producto, function () {
		//termina de cargar ajax
	});
}

//quitamos el producto del combo
function quitarProductoRelacionado(producto_relacionado_id) {
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;

	datos_quitar = {
		'module_x': document.forms['form_operation'].elements['module_x'].value,
		'operation_x': 'quitar_producto_relacionado',
		'producto_relacionado_id': producto_relacionado_id,
		'csrfmiddlewaretoken': token,
	}

	$("#lista_productos_relacionados").html(imgLoading);
	$("#lista_productos_relacionados").load(hostURL, datos_quitar, function () {
		//termina de cargar ajax
	});
}

//cargamos imagen con ajax
function cargarImagen() {
	posicion = document.getElementById('posn_1');
	posicion_valor = Trim(posicion.value);

	valor_imagen = Trim(document.getElementById('imagen1').value);
	if (valor_imagen == '') {
		//alert('debe seleccionar una imagen');
		modalSetParameters('warning', 'center', 'Productos!', 'Debe seleccionar una imagen', 'Cancelar', 'Volver');
		modalFunction.value = 'productoWarning();';
		modalF.modal();
		return false;
	}

	if (posicion_valor == '') {
		//alert('Debe llenar la posicion');
		//posicion.focus();
		modalSetParameters('warning', 'center', 'Productos!', 'Debe llenar la posicion', 'Cancelar', 'Volver');
		modalFunction.value = 'productoWarning();';
		modalF.modal();
		return false;
	}

	//boton de la imagen
	boton_imagen = document.getElementById('btn_imagen');
	boton_imagen.disabled = true;

	pid = document.getElementById('pid').value;
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	module_x = document.forms['form_operation'].elements['module_x'].value;

	var fd = new FormData();
	//alert(fd);
	var files = $('#imagen1')[0].files[0];
	//alert(files);
	fd.append('imagen1', files);
	fd.append('module_x', module_x);
	//alert(fd);
	fd.append('operation_x', 'add_imagen');
	fd.append('csrfmiddlewaretoken', token);
	fd.append('pid', pid);
	fd.append('posicion', posicion_valor);

	$.ajax({
		url: hostURL,
		type: 'post',
		data: fd,
		contentType: false,
		processData: false,
		success: function (response) {
			if (response != 0) {

				datos_imagen = {
					'module_x': module_x,
					'operation_x': 'lista_imagenes',
					'pid': pid,
					'csrfmiddlewaretoken': token,
				}

				$("#div_lista_imagenes").html(imgLoading);
				$("#div_lista_imagenes").load(hostURL, datos_imagen, function () {
					//termina de cargar ajax
					boton_imagen.disabled = false;
				});
				//alert('cargado');
			} else {
				alert('no se pudo cargar la imagen, intentelo de nuevo');
				boton_imagen.disabled = false;
			}
		},
	});

}

//mostramos la imagen
function mostrarImagen(pid) {
	document.form_img.id.value = pid;
	document.form_img.submit();
}

//eliminar imagen
function eliminarImagen(pid) {
	//token
	token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
	module_x = document.forms['form_operation'].elements['module_x'].value;

	datos_imagen = {
		'module_x': module_x,
		'operation_x': 'eliminar_imagen',
		'id': pid,
		'csrfmiddlewaretoken': token,
	}

	$("#div_lista_imagenes").html(imgLoading);
	$("#div_lista_imagenes").load(hostURL, datos_imagen, function () {
		//termina de cargar ajax
		//boton_imagen.disabled = false;
	});

}

async function formularioImagenProducto(operation, operation2, formulario, add_button, button_cancel) {

	document.forms[formulario].elements[add_button].disabled = true;
	document.forms[formulario].elements[button_cancel].disabled = true;

	var fd = new FormData(document.forms['formulario']);

	//mostramos valores
	// for (var pair of fd.entries()) {
	// 	console.log(pair[0] + ', ' + pair[1]);
	// }

	div_modulo.html(imagen_modulo);

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
					div_modulo.html(response);
				} else {
					alert('error al realizar la operacion, intentelo de nuevo');
				}
			},
			error: function (qXHR, textStatus, errorThrown) {
				console.log(errorThrown);
				console.log(qXHR);
				console.log(textStatus);
			},
		});
		//alert(result);
	}
	catch (e) {
		console.error(e);
	}
}

//crea descripcion del producto
function crearDescripcion() {
	descr1 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion1').value));
	descr2 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion2').value));
	descr3 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion3').value));
	descr4 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion4').value));
	descr5 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion5').value));
	descr6 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion6').value));
	descr7 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion7').value));
	descr8 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion8').value));
	descr9 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion9').value));
	descr10 = TrimDerecha(TrimIzquierda(document.getElementById('descripcion10').value));

	texto1 = verificarTexto(descr1);
	texto2 = verificarTexto(descr2);
	texto3 = verificarTexto(descr3);
	texto4 = verificarTexto(descr4);
	texto5 = verificarTexto(descr5);
	texto6 = verificarTexto(descr6);
	texto7 = verificarTexto(descr7);
	texto8 = verificarTexto(descr8);
	texto9 = verificarTexto(descr9);
	texto10 = verificarTexto(descr10);

	texto_mostrar = texto1 + texto2 + texto3 + texto4 + texto5 + texto6 + texto7 + texto8 + texto9 + texto10;
	descripcion = $("#datos_descripcion");
	descripcion.html(texto_mostrar);
}

//arma texto de la descripcion del producto con negrita y cursiva
function verificarTexto(descripcion) {
	if (descripcion == '') {
		return '';
	}
	else {
		return descripcion + '<br>';
	}
}