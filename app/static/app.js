$(document).ready(function() {

    $(".update-button").change(function(event) {
        var checkbox = $(event.target);
        var is_checked = $(checkbox).is(":checked");
        var order_id = checkbox.prop("id")
        
        req = $.ajax({
            url : "/update",
            type : "POST",
            data : { order_id : order_id, checkbox : checkbox.prop("name"), is_checked : is_checked}
        });

        req.done(function() {
            checkbox.prop("checked") = is_checked;
        });
  
    });

});