$(document).ready(function(){
    $('a.cancel').click(function(e){
        e.preventDefault();
        var id = $(this).data('id');
        $.ajax('/parts/cancel/' + id, {
            success: function(result) {
                console.log(result);
                $('#row-'+id).hide();
            },
            cache: false,
            timeout: 10000
        });
    });
});
