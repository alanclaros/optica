//url empresa
const urlEmpresa = '';

//host url
const hostURL = location.origin + urlEmpresa;

//img loading
const imgLoading = '<img src="' + urlEmpresa + '/static/img/pass/loading.gif">';
const imgLoading2 = '<img src="' + urlEmpresa + '/static/img/pass/loading2.gif">';

//settings
const imagen_modulo = '<div class="Loader">Loading...</div>';

//block content
const div_modulo = $("#div_block_content");

//modal function
const modalFunction = document.getElementById('modalFunctionSuccess');
const modalF = $('#modalForm');

const modalPrintFunctionB1 = document.getElementById('modalPrintFunctionB1');
const modalPrintFunctionB2 = document.getElementById('modalPrintFunctionB2');
const modalFPrint = $('#modalPrint');

//check for hide notifications
setInterval('hideNotifications()', 5000);

//notificaciones
setInterval('checkNotifications()', 45000); //45 segundos

// Get the modal
var modal = document.getElementById("printModal");

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

$(document).ready(function () {

    // $(document).on('click', 'a', function () {
    //   openURL($(this).attr("href"));
    //   return false; //intercept the link
    // });  

    window.addEventListener('popstate', function (e) {
        //console.log('parametro e: ', e);
        if (e.state) {
            //console.log('state..: ', e.state);
            let moduloCargar = e.state.href;
            moduloCargar = moduloCargar.replace(hostURL + '/', '');
            //console.log('modulo cargar pop state: ', moduloCargar);
            openModule(moduloCargar);
        }
    });

});