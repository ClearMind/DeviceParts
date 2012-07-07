$(document).ready(function(){
    var url = '';
    $('#print_act').click(function(e){
        var id = $(this).data('deviceid');
        e.preventDefault();
        $.ajax('/parts/print/?device=' + id, {
            dataType: "text",
            method: 'GET',
            success: function (data) {
                url = data;
                console.log('URL: ' + url);
                $('#down_link').attr('src', url);
            }
        });
    });
});