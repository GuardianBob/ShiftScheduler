$(document).ready(function(){  
    $('#nav_logo').click(function(){
        $('#nav-bar').animate({width: 'toggle'});
        $('#nav_logo_hidden').animate({width: 'toggle'});
    });
    $('#nav_logo_hidden').click(function(){
        $('#nav-bar').animate({width: 'toggle'});
        $('#nav_logo_hidden').animate({width: 'toggle'});
    });    

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    $(document).mouseup(function(e) 
    {
        var container = $("#mySideNav");

        // if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0) 
        {
            container.width("0%");
        }
    });
    
});

function openNav() {
    $("#mySideNav").width("60%");}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySideNav").style.width = "0";
}

function toggleCode(div) {
    $(div).toggle({height: 'toggle'});
}
