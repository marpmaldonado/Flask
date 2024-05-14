$(document).ready(function(){
$("#btnActualizar").click(function()
{
 cargarmodal.load("../templates/Modaltareas.html");
});

function cargarmodal(){
    $('#Mtareas').load(ruta,function(){
        $('#Mtareas').modal("show");
    });
};

});

