$(document).ready(function(){

    var rooms = String(window.location.pathname).includes('rooms')
    var salespersons = String(window.location.pathname).includes('salespersons')
    if(salespersons || rooms){

        var script = document.createElement('script');
        script.src = 'https://unpkg.com/gijgo@1.9.13/js/gijgo.min.js';
        document.head.appendChild(script);

        $('#datepicker').datepicker({
            uiLibrary: 'bootstrap4',
        });
    }

    for(var i = 0; i < 60; i++){
        $(".time-margin" + String(i)).css("margin-left", String((i*100) + 58)  + "px");
        $(".time-width" + String(i)).css("width", String((i*100) - 2)  + "px");
        $(".booking_box" + String(i)).css("width", String((i*100))  + "px");
        $(".booking_record_ml" + String(i+1)).css("margin-left", String(i*125)  + "px");
    }

    for(var i = 2; i < 60; i++){
        $(".booking_record_width" + String(i)).css("width", String(i * 125)  + "px");
    }
});
