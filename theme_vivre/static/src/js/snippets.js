$( document ).ready(function() {

    function getYesterdaysDate() {
        var date = new Date();
        date.setDate(date.getDate());
        return `${(date.getMonth()+1)}/${date.getDate()}/${date.getFullYear()}`
    }

    var date1 = String(window.location.pathname).endsWith('/choose/date')

    if(date1){
        var script = document.createElement('script');
        script.src = 'https://unpkg.com/gijgo@1.9.13/js/gijgo.min.js';
        document.head.appendChild(script);

        $('#appoint_date').datepicker({
            minDate: getYesterdaysDate(),
            uiLibrary: 'bootstrap4',
        });
    }

    function number_format(temp_number) {
        var return_number;
        if((temp_number/2) < 10){
            if(temp_number % 2 == 0){
                return_number = `0${String(temp_number/2)}:00`;
            }
            else {
                return_number = `0${String(temp_number/2).replace(".5", ":3")}0`;
            }
        }
        else {
            if(temp_number % 2 == 0){
                return_number = `${String(temp_number/2)}:00`;
            }
            else {
                return_number = `${String(temp_number/2).replace(".5", ":3")}0`;
            }
        }
        return return_number
    }

    $('#appoint_date').change(function(){
        appoint_date = $('input[name="appoint_date"]').val();
        sale_order_number = $('input[name="sale_order_number"]').val();

        vals = {
            'appoint_date':appoint_date,
            'sale_order_number':sale_order_number
        }

        $.ajax({
            type: "POST",
            dataType: 'json',
            url: '/quotationtimeslots',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {'data': vals}}),
            success: function (data) {

                var jsondata, key, temp;
                jsondata = data.result;

                $("#select_time_slots").empty();
                for (key in jsondata) {
                    temp = jsondata[key]
                    if(jsondata[key].length){
                        var temp2 = jsondata[key].length;
                        for(var i = 0; i < temp2; i++){
                            var x = document.getElementById("select_time_slots");
                            var option = document.createElement("option");
                            option.text = `${number_format(temp[i][0])} - ${number_format(temp[i][1])}`;
                            option.value = key + '-' + String(temp[i][0]) + '-' + String(temp[i][1]);
                            x.add(option);
                        }
                    }
                }

            },error: function(data){
                console.log("ERROR ", data);
            }
        });
    });


    $('.product_details_modal').hide();
    $("#product_details_close").click(function() {
        $('.product_details_modal').hide();
    });

    $("button").click(function() {

        var click_id = $(this).attr('id');

        if(String(click_id).includes('vivre_product_id')){
            product_id = $('#' + click_id).val();
            vals = {
                'product_id':product_id
            }
            $.ajax({
                type: "POST",
                dataType: 'json',
                url: '/shop/cart/updates',
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {'data': vals}}),
                success: function (data) {
                    jsondata = data.result;
                    console.log(jsondata.total_quantity);
                    $('.my_cart_quantity').html(jsondata.total_quantity);
                },
                error: function(data){
                    console.log("ERROR ", data);
                }
            });
        }

        if(String(click_id).includes('product_details_view')){

            var click_id = $(this).attr('id');
            var product_name = click_id.split('-')

            vals = {
                'product_name':product_name[1]
            }

            $.ajax({
                type: "POST",
                dataType: 'json',
                url: '/getdetails',
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {'data': vals}}),
                success: function (data) {

                    jsondata = data.result

                    $('.vivre_product_name').html(jsondata.name);
                    $('.vivre_product_time').html(jsondata.appointment_time);
                    $('.vivre_product_price').html(jsondata.price);
                    $('.vivre_product_description').html(jsondata.description);

                    $('.product_details_modal').show();
                },
                error: function(data){
                    console.log("ERROR ", data);
                }
            });
        }

    });

});
