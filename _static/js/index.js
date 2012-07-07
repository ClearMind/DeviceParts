$(document).ready(function(){
    $('#show-hide').change(function(){
        var checked = $(this).attr('checked') == 'checked';
        console.log(checked);
        if(checked)
            $('.zero').hide();
        else
            $('.zero').show();
    })
});
