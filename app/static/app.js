$(document).ready(function() {
    $(".update-button").change(function(event) {
        var checkbox = $(event.target);
        var is_checked = $(checkbox).is(":checked");
        var order_id = $(checkbox).parents("tr").attr("id");
        var countCheckedCheckboxes = $(checkbox).parents("tr").find("input[type='checkbox']").filter(':checked').length;

        if(countCheckedCheckboxes == 0){
            $(checkbox).parents("tr").removeClass("finished-order");
            $(checkbox).parents("tr").removeClass("almost-finished-order");
            $(checkbox).parents("tr").removeClass("started-order");
            $(checkbox).parents("tr").addClass("not-started-order");
        }
        else if(countCheckedCheckboxes == 1){
            $(checkbox).parents("tr").removeClass("finished-order");
            $(checkbox).parents("tr").removeClass("almost-finished-order");
            $(checkbox).parents("tr").removeClass("not-started-order");
            $(checkbox).parents("tr").addClass("started-order");
        }
        else if(countCheckedCheckboxes == 2){
            $(checkbox).parents("tr").removeClass("finished-order");
            $(checkbox).parents("tr").removeClass("started-order");
            $(checkbox).parents("tr").removeClass("not-started-order");
            $(checkbox).parents("tr").addClass("almost-finished-order");
        }
        else if(countCheckedCheckboxes == 3){
            $(checkbox).parents("tr").removeClass("almost-finished-order");
            $(checkbox).parents("tr").removeClass("started-order");
            $(checkbox).parents("tr").removeClass("not-started-order");
            $(checkbox).parents("tr").addClass("finished-order");
        }
        req = $.ajax({
            url : "/update",
            type : "POST",
            data : { order_id : order_id, checkbox : checkbox.prop("name"), is_checked : is_checked}
        });

        req.done(function() {
            checkbox.attr("checked", true);
        });
  
    });

    $(".number-input").children("button").click(function(event) {
        var number = $(event.target).siblings("input").val();
        if($(event.target).siblings("input").prop("validity").valid &&
            $(event.target).siblings("input").val() > 0){
            var type = $(event.target).attr("id");
            var order_id = $(event.target).parents("tr").attr("id");

            req = $.ajax({
                url : "/finance",
                type : "POST",
                data : { order_id : order_id, type : type, number : number}
            });
            req.done(function(data) {
                $(event.target).hide();
                $(event.target).siblings("input").hide();
                var newNumber;
                if($(event.target).siblings("span").length){
                    newNumber = $(event.target).siblings("span");
                    newNumber.show();
                }
                else{
                    newNumber = document.createElement("span");
                    $(event.target).parents(".number-input").prepend(newNumber);
                    if(type == "expenses-number"){
                        newNumber.classList.add("expense");
                    }
                    else{
                        newNumber.classList.add("income");
                    }
                }

                if(type == "expenses-number"){
                    newNumber.innerText = ("-" + data.value);
                }
                else{
                    newNumber.innerText = ("+" + data.value);
                }

                $(event.target).parents("tr").find(".total-earnings").text(data.total);
                
                var sum = 0
                $(".total-earnings").each(function(){
                    sum += parseInt($(this).text());
                })
                $(".all-earnings").text(sum);
                $("#earnings-sum").text(function(){
                    var totalEarnings = 0
                    $(".total-earnings").each(function(){           
                        totalEarnings += parseInt(this.innerText);
                    })
                    return totalEarnings;
                })
                $(event.target).parents("tr").find(".total-earnings").each(function(){
                    if(parseInt($(this).text()) < 0){
                        $(this).removeClass('income');
                        $(this).addClass('expense');
                    }
                    else if(parseInt($(this).text()) > 0){
                        $(this).removeClass('expense');
                        $(this).addClass('income');
                    }
                })
                $("#earnings-sum").each(function(){
                    if(parseInt($(this).text()) < 0){
                        $(this).removeClass('income');
                        $(this).addClass('expense');
                    }
                    else if(parseInt($(this).text()) > 0){
                        $(this).removeClass('expense');
                        $(this).addClass('income');
                    }
                })
            });
        }
    })
    $("tbody").on("click", ".income,.expense", function(){
        if($(event.target).is(":visible")){
            $(event.target).hide();
            $(event.target).siblings("input").show();
            $(event.target).siblings("input").focus();
            $(event.target).siblings("button").show();
        }
    })
    $(".update-button").each(function() {
        var countCheckedCheckboxes = $(this).parents("tr").find("input[type='checkbox']").filter(':checked').length;

        if(countCheckedCheckboxes == 0){
            $(this).parents("tr").removeClass("finished-order");
            $(this).parents("tr").removeClass("almost-finished-order");
            $(this).parents("tr").removeClass("started-order");
            $(this).parents("tr").addClass("not-started-order");
        }
        else if(countCheckedCheckboxes == 1){
            $(this).parents("tr").removeClass("finished-order");
            $(this).parents("tr").removeClass("almost-finished-order");
            $(this).parents("tr").removeClass("not-started-order");
            $(this).parents("tr").addClass("started-order");
        }
        else if(countCheckedCheckboxes == 2){
            $(this).parents("tr").removeClass("finished-order");
            $(this).parents("tr").removeClass("started-order");
            $(this).parents("tr").removeClass("not-started-order");
            $(this).parents("tr").addClass("almost-finished-order");
        }
        else if(countCheckedCheckboxes == 3){
            $(this).parents("tr").removeClass("almost-finished-order");
            $(this).parents("tr").removeClass("started-order");
            $(this).parents("tr").removeClass("not-started-order");
            $(this).parents("tr").addClass("finished-order");
    }})
    $("#earnings-sum").text(function(){
        var totalEarnings = 0
        $(".total-earnings").each(function(){           
            totalEarnings += parseInt(this.innerText);
        })
        return totalEarnings;
    })
    $(".total-earnings").each(function(){
        if(parseInt($(this).text()) < 0){
            $(this).removeClass('income');
            $(this).addClass('expense');
        }
        else if(parseInt($(this).text()) > 0){
            $(this).removeClass('expense');
            $(this).addClass('income');
        }
    })
    $("#earnings-sum").each(function(){
        if(parseInt($(this).text()) < 0){
            $(this).removeClass('income');
            $(this).addClass('expense');
        }
        else if(parseInt($(this).text()) > 0){
            $(this).removeClass('expense');
            $(this).addClass('income');
        }
    })

});
$(document).change(function() {
    
})