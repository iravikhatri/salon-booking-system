$( document ).ready(function() {

    $('#instalments_block').hide();

    $('input[name=pm_id]').click(function() {
        if($('input[name="pm_id"]:checked').val() == 'form_9'){
            $('#instalments_block').show();
        }
        else {
            $('#instalments_block').hide();
            $('#month3').prop('checked', false);
            $('#month6').prop('checked', false);
            $('#month12').prop('checked', false);
            $('#month3_card').css('background-color', '#fff');
            $('#month6_card').css('background-color', '#fff');
            $('#month12_card').css('background-color', '#fff');
        }
    });

    $(".month_card").click(function() {
        var click_id = $(this).attr('id');

        if('month3_card' == click_id){
            $('input:checkbox[name=month3]').each(function(){
                if($(this).is(':checked')){
                    $('#month3').prop('checked', false);
                    $('#month3_card').css('background-color', '#fff');
                }
                else {
                    $('#month3').prop('checked', true);
                    $('#month3_card').css('background-color', '#cef3f5');
                }
            });

            $('#month6').prop('checked', false);
            $('#month12').prop('checked', false);
            $('#month6_card').css('background-color', '#fff');
            $('#month12_card').css('background-color', '#fff');
        }
        else if('month6_card' == click_id){
            $('input:checkbox[name=month6]').each(function(){
                if($(this).is(':checked')){
                    $('#month6').prop('checked', false);
                    $('#month6_card').css('background-color', '#fff');
                }
                else {
                    $('#month6').prop('checked', true);
                    $('#month6_card').css('background-color', '#cef3f5');
                }
            });

            $('#month3').prop('checked', false);
            $('#month12').prop('checked', false);
            $('#month3_card').css('background-color', '#fff');
            $('#month12_card').css('background-color', '#fff');
        }
        else if('month12_card' == click_id){
            $('input:checkbox[name=month12]').each(function(){
                if($(this).is(':checked')){
                    $('#month12').prop('checked', false);
                    $('#month12_card').css('background-color', '#fff');
                }
                else {
                    $('#month12').prop('checked', true);
                    $('#month12_card').css('background-color', '#cef3f5');
                }
            });

            $('#month3').prop('checked', false);
            $('#month6').prop('checked', false);
            $('#month3_card').css('background-color', '#fff');
            $('#month6_card').css('background-color', '#fff');
        }
    });

    function emi_calculation(payment_time_period) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: '/emi/calculation',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {'data': {
                'payment_time_period':payment_time_period
            }}}),
            success: function (data) {
                result_data = data.result
                console.log(result_data);
                $(`#month${payment_time_period}_per_month_amount`).html(result_data.monthly_EMI);
                $(`#month${payment_time_period}_total_interest_rate`).html(result_data.total_interest_rate);
                $(`#month${payment_time_period}_total_interest_amount`).html(result_data.total_interest_amount);
            },
            error: function(data){
                console.log("ERROR ", data);
            }
        });
    }

    if(String(window.location.pathname).endsWith("/shop/payment")) {
         emi_calculation(3)
         emi_calculation(6)
         emi_calculation(12)
    }

    if(String(window.location.pathname).endsWith("/shop/payment")) {
        $("#o_payment_form_pay").click(function() {
            $.ajax({
                type: "POST",
                dataType: 'json',
                url: '/emidata',
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {'data': {
                    'payment_time_period': Number($('.emi_value:checked').val())
                }}}),
                success: function (data) {
                    result_data = data.result
                    console.log(result_data);
                },
                error: function(data){
                    console.log("ERROR ", data);
                }
            });
        });
    }

});
