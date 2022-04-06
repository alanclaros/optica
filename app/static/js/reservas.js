
function reservasSearchPeriodo(periodo) {
    const periodo_form = document.forms['search'].elements['search_periodo'];
    periodo_form.value = periodo;
    sendSearchReserva();
}

function sendSearchReserva() {
    sendFormObject('search', div_modulo);
}

function reservasShowDia(dia) {
    //registramos el dia en los otros forms
    const form_dia = document.forms['form_registrar_reserva'].elements['dia'];
    form_dia.value = dia;

    //titulo
    const label_actual = document.getElementById('span_periodo_actual').innerHTML;
    const span_titulo = document.getElementById('span_nueva_actividad_periodo');
    span_titulo.innerHTML = dia + '-' + label_actual;

    //quitando mensajes
    const res_act = $('#div_resultado_solicitar_reserva');
    res_act.html('&nbsp;');

    //llenamos las horas para el dia
    const hora_nuevo = $('#hora_nuevo');
    const horas_ids = document.getElementById('horas_ids_' + dia).value;
    const horas = document.getElementById('horas_' + dia).value;
    const div_horas_ids = horas_ids.split(',');
    const div_horas = horas.split(',');

    hora_nuevo.find('option').remove();
    let i = 0;
    for (i = 0; i < div_horas_ids.length; i++) {
        if (div_horas_ids[i] !== '') {
            hora_nuevo.find('option').end().append('<option value="' + div_horas_ids[i] + '">' + div_horas[i] + '</option>');
        }
    }

    const modalA = $('#modalActividad');
    modalA.modal();
}

function setClassInvalid(objeto) {
    let claseObj = objeto.className.toLowerCase();
    const pos = claseObj.indexOf('is-invalid');
    if (pos === -1) {
        claseObj += " is-invalid";
    }
    objeto.className = claseObj;
}

function reservasRegistrarReserva() {
    dia = document.forms['form_registrar_reserva'].elements['dia'].value;
    const nombres = document.getElementById('nombres_nuevo');
    const apellidos = document.getElementById('apellidos_nuevo');
    const telefonos = document.getElementById('telefonos_nuevo');
    const hora = document.getElementById('hora_nuevo');
    const dia_semana = document.getElementById('dia_semana_' + dia);
    const resultado = $('#div_resultado_solicitar_reserva');
    const btn_reserva = document.getElementById('btn_solicitar_reserva');

    if (nombres.value.trim() === '') {
        setClassInvalid(nombres);
        resultado.html('Debe llenar su Nombre');
        return false;
    }
    if (apellidos.value.trim() === '') {
        setClassInvalid(apellidos);
        resultado.html('Debe llenar su Apellido');
        return false;
    }
    if (telefonos.value.trim() === '') {
        setClassInvalid(telefonos);
        resultado.html('Debe llenar su Telefono');
        return false;
    }

    const token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    const datos = {
        'nombres': nombres.value.trim(),
        'apellidos': apellidos.value.trim(),
        'telefonos': telefonos.value.trim(),
        'dia': dia,
        'dia_semana': dia_semana.value,
        'hora': hora.value,
        'periodo': document.getElementById('periodo_actual').value,
        'csrfmiddlewaretoken': token,
        'module_x': document.forms['search'].elements['module_x'].value,
        'operation_x': 'add_reserva'
    }
    //console.log('datos: ', datos, ' dia: ', dia);
    // $('#div_resultado_listado_' + dia).html(imgLoading);
    // $('#div_resultado_listado_' + dia).load('', datos, function () {
    //     //termina de cargar ajax
    //     //boton_imagen.disabled = false;
    // });
    btn_reserva.disabled = true;
    resultado.load(hostURL, datos, function (response) {
        if (response == 0) {
            resultado.html('Error al registrar, intentelo nuevamente');
            btn_reserva.disabled = false;
        }
        else {
            const error_resp = document.getElementById('error_' + dia).value;
            if (error_resp !== '1') {
                //reset
                nombres.value = "";
                apellidos.value = "";
                telefonos.value = "";
            }
            btn_reserva.disabled = false;
        }
    });

}


function reservasConfirmarReserva(reserva_id, dia) {
    const nombres = document.getElementById('nombres_r_' + reserva_id);
    const apellidos = document.getElementById('apellidos_r_' + reserva_id);
    const telefonos = document.getElementById('telefonos_r_' + reserva_id);
    const mensaje = document.getElementById('mensaje_r_' + reserva_id);
    const hora_ini = document.getElementById('hora_ini_r_' + reserva_id);

    const resultado = $('#div_resultado_confirmar');
    const btn_confirmar = document.getElementById('btn_confirmar_confirmar');
    const btn_eliminar = document.getElementById('btn_confirmar_eliminar');

    resultado.html('&nbsp;');

    const span_nombres = document.getElementById('span_confirmar_nombres');
    const span_apellidos = document.getElementById('span_confirmar_apellidos');
    const span_telefonos = document.getElementById('span_confirmar_telefonos');
    const span_hora = document.getElementById('span_confirmar_hora');
    const span_mensaje = document.getElementById('span_confirmar_mensaje');

    span_nombres.innerHTML = nombres.value;
    span_apellidos.innerHTML = apellidos.value;
    span_telefonos.innerHTML = telefonos.value;
    span_mensaje.innerHTML = mensaje.value;
    span_hora.innerHTML = hora_ini.value;

    const label_actual = document.getElementById('span_periodo_actual').innerHTML;
    const span_titulo = document.getElementById('span_confirmar_periodo');
    span_titulo.innerHTML = dia + '-' + label_actual;

    //id
    const reserva_id_conf_del = document.getElementById('reserva_id_conf_del');
    reserva_id_conf_del.value = reserva_id;

    btn_confirmar.disabled = false;
    btn_eliminar.disabled = false;

    reservasCancelarMostrar();

    const modalConf = $('#modalConfirmar');
    modalConf.modal();
}

//mostrar botones de confirmacion
function reservasMostrarConfirmar(tipo) {
    const tr_conf = $('#tr_confirmar');
    const tr_elim = $('#tr_eliminar');
    if (tipo === 'confirmar') {
        tr_conf.fadeIn('slow');
        tr_elim.fadeOut('slow');
    }
    else {
        tr_elim.fadeIn('slow');
        tr_conf.fadeOut('slow');

    }
}

//cancelando confirmacion
function reservasCancelarMostrar() {
    const tr_conf = $('#tr_confirmar');
    const tr_elim = $('#tr_eliminar');

    tr_conf.fadeOut('slow');
    tr_elim.fadeOut('slow');
}

//confirmamos o eliminamos la actividad
function reservasConfirmarActividad(tipo) {
    const resultado = $('#div_resultado_confirmar');
    const btn_confirmar = document.getElementById('btn_confirmar_confirmar');
    const btn_eliminar = document.getElementById('btn_confirmar_eliminar');
    const reserva_id = document.getElementById('reserva_id_conf_del').value;

    const token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    const datos = {
        'reserva_id': reserva_id,
        'csrfmiddlewaretoken': token,
        'module_x': document.forms['search'].elements['module_x'].value,
        'operation_x': tipo
    }

    reservasCancelarMostrar();

    btn_confirmar.disabled = true;
    btn_eliminar.disabled = true;
    resultado.load(hostURL, datos, function (response) {
        if (response == 0) {
            resultado.html('Error al registrar, intentelo nuevamente');
            btn_confirmar.disabled = false;
            btn_eliminar.disabled = false;
        }
        else {
            btn_confirmar.disabled = false;
            btn_eliminar.disabled = false;
        }
    });
}

function reservasShowReservas(dia) {
    //quitando mensajes
    const res_act = $('#div_resultado_listado_' + dia);
    res_act.html('&nbsp;');

    reservasListadoCancelar(dia);

    const modalLi = $('#modalListado_' + dia);
    modalLi.modal();
}

//confirmacion para eliminar de listado
function reservasListadoEliminar(dia, reserva_id) {
    const tr_elim = $('#tr_listado_eliminar_' + dia);
    tr_elim.fadeIn('slow');

    const reserva_id_elim = document.getElementById('reserva_id_eliminar');
    reserva_id_elim.value = reserva_id;
}
//cancelar
function reservasListadoCancelar(dia) {
    const tr_elim = $('#tr_listado_eliminar_' + dia);
    tr_elim.fadeOut('slow');
}

function reservasEliminarReserva(dia) {
    const resultado = $('#div_resultado_listado_' + dia);
    const token = document.forms['formulario'].elements['csrfmiddlewaretoken'].value;
    const reserva_id = document.getElementById('reserva_id_eliminar').value;
    const datos = {
        'reserva_id': reserva_id,
        'csrfmiddlewaretoken': token,
        'module_x': document.forms['search'].elements['module_x'].value,
        'operation_x': 'eliminar_reserva'
    }

    reservasListadoCancelar(dia);

    resultado.load(hostURL, datos, function (response) {
        if (response == 0) {
            resultado.html('Error al eliminar, intentelo nuevamente');
        }
        else {
            //ok
        }
    });
}