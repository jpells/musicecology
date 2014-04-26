$(document).ready(function() {
    //Attach ajax to newsletter subscribe form.
    $("#subscribe-form").submit(function() {
        $.ajax({
            type: $("#subscribe-form").attr("method"),
            url: $("#subscribe-form").attr("action"),
            data: $("#subscribe-form").serialize(),
            success: function(data) {
                //Render successful alert message.
                $("#subscribe-result").html('<div class="messages"><div class="alert alert-dismissable alert-info" data-alert="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">x</button>'.concat(data.message).concat('</div></div>'))
            },
        });
        return false;
    });
});