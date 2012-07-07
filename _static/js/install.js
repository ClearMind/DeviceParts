$(document).ready(function () {
    // DATEPICKER
    $('#id_install_date').datepicker({
        dateFormat:"dd.mm.yy",
        dayNamesMin:["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
        firstDay:1
    });

    // AUTOCOMPLETER
    var getDevices = function () {
        var result = [];
        $.ajax('/parts/devices/', {
            async:false,
            success:function (data, textStatus, jqXHR) {
                result = data;
                console.log(textStatus);
            }
        });
        return result;
    }
    var devices = getDevices();
    var inv_numbers = [];
    for (var i = 0; i < devices.length; ++i) {
        inv_numbers.push(devices[i][0]);
    }
    $('#id_inventory_number').autocomplete({
        minLength:2,
        source:inv_numbers,
        select:function (event, ui) {
            $('#id_inventory_number').val(ui.item.value);
            for (var i = 0; i < devices.length; ++i) {
                if (devices[i][0] == ui.item.value) {
                    $('#id_device_type').val(devices[i][1]);
                    var new_location = "http://" + window.location.host + "/parts/installed/" + ui.item.value +
                        "/?only_content=1";
                    $('#installed_parts').attr('src', new_location);
                }
            }
        }
    });

    $('#id_parts_in_stores').chosen({no_results_text: "None"});

});

