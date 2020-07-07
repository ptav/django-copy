/*
    django-copy JS
    ==============

    Visible on Hover
    ----------------

    To create a block that becomes visible (the toggle)
    on mouse hover over a second block (the trigger):
    
    1. add class "visible-on-hover" to the trigger block
    2. identify the toggle block with an id
    3. add the attribute "data-toggle" in the trigger block equal to the toggle id
*/

$(".visible-on-hover").on("mouseenter", __dc_show__);
$(".visible-on-hover").on("mouseleave", __dc_hide__);
$(".visible-on-hover").each(__dc_initial_hide__);


function __dc_initial_hide__()
{
    var toggle = $(this).attr("data-toggle");
    $("#" + toggle).hide();
}


function __dc_hide__()
{
    event.stopPropagation();
    var toggle = $(this).attr("data-toggle");
    $("#" + toggle).hide("slow");
}


function __dc_show__(event)
{
    event.stopPropagation();
    var toggle = $(this).attr("data-toggle");
    $("#" + toggle).show("slow");
};