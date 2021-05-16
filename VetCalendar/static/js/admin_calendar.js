function build_cal(cal_date) {
    $('#calendar').fullCalendar({
        timeZone: 'local',
        header: {
            left: 'prev,next, today, datepicker',
            center: 'title',
            right: 'month,listWeek,listDay'
        },
        views: {
            listDay: { buttonText: 'list day' },
            listWeek: { buttonText: 'list week' }
        },
        defaultView: 'month',
        defaultDate: '"' + cal_date + '"',
        events:[             
        ],
        navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        selectable: true,
        selectHelper: true,
        
    });    
    // console.log("cal_date: " + cal_date)
};        

function verify_clear(form) {
    date = $('#calendar').fullCalendar('getDate').format("MMM-YYYY");
    // console.log(form);    
    if(form == 0){
        $('#clear_entries').attr('formaction', 'clear_month')   
        $('#clear_entries').attr('form', 'clear_month_form')      
    } else if (form == 1){
        $('#clear_entries').attr('formaction', 'clear_user')
        $('#clear_entries').attr('form', 'clear_user_form')
        $('#modal_user').html($('#clear_user_form').find('#id_user').children(':selected').text())
        // console.log($('#clear_user_form').find('#id_user').children(':selected').text());
        $('#warning').html('Are you sure you want to clear all shifts for the selected user for the month shown above?')
    }
    $('#clear_month').modal('show');    
    $('#clear_month').find('#modal_date').text(date);
    
}

function format_date(date) {
    // console.log("Date: " + date);
    var dd = String(date.getDate()).padStart(2, '0');
    var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = date.getFullYear(); 
    // console.log(mm, dd);
    return yyyy + '-' + mm  + '-' + dd
}
function format_date_datepicker(date) {
    // console.log("Date: " + date);
    var dd = String(date.getDate()).padStart(2, '0');
    var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = date.getFullYear(); 
    // console.log(mm, dd);
    return mm  + '-' + dd + '-' + yyyy
}

function add_events(schedule){
    // console.log(schedule);  
    var myCalendar = $('#calendar'); 
    myCalendar.fullCalendar('removeEvents');
    // myCalendar.fullCalendar();
    schedule.forEach((item)=>{
        // console.log(item)
        var new_start = item.start.toString() + "T" + item.time.toString()
        var myEvent = {
            title: "" + item.title.toString() + "",
            start: new_start,
            startStr: item.shift_h.toString(),
            endStr: item.shift_type.toString(),
            id: item.id.toString(),
            color: "" + item.color.toString() + "", 
        };
        // console.log(new_start)       
            
        myCalendar.fullCalendar( 'renderEvent', myEvent );
    });
}

function get_shifts(date) {                      
    var data
    $.ajax({                                        
        url: "/get_shifts/" + date + "",
        success: function (response){            
            // console.log(response.schedule);
            add_events(response.schedule)
            data = response
            return response            
            
        },
        error: function (response) {
            // alert the error if any error occured
            console.log(response.responseJSON.errors)
        }
    });    
    return data;
}

function fix_date(date) {
    now = new Date();
    var hh = now.getHours();
    var mm = now.getMinutes();
    date.setHours(hh);
    date.setMinutes(mm);
    return date;
}

// function form_submit() {
//     $("#modal_form").submit();
// }

var pageDate = new Date()
var initDate = format_date(pageDate);

$(document).ready(function() {    
            
    build_cal(initDate);
    // var getDate = $('#calendar').fullCalendar('getDate').format();
    // calDate = format_date(new Date(getDate));
    get_shifts(initDate);
    //var schedule = {{ schedule }};
    // console.log(initDate)
    // fillCal(data.calDate, data.schedule);
    $('.fc-next-button, .fc-prev-button, .fc-today-button, .fc-month-button').click(function() {
        // console.log("clicked!");
        var getDate = $('#calendar').fullCalendar('getDate').format("MM-DD-YYYY HH:mm");
        // console.log("getDate: " + getDate);
        // console.log("fixed: " + new Date(getDate));
        calDate = format_date(new Date(getDate));
        $("#date-select").val(format_date_datepicker(new Date(getDate)));
        $("#month_clear").val(format_date_datepicker(new Date(getDate)));
        // var view = $('#calendar').fullCalendar('getView');
        // console.log("1st: " + calDate);
        get_shifts(calDate);
        // pageDate.setMonth(pageDate.getMonth()+1);
        // calDate = format_date(pageDate);
    });

    $("#starts-at, #ends-at, #date-select").datetimepicker({
        format: 'MM-DD-YYYY',
    });

    $('#multi-date').datepicker({
        format: 'mm-dd-yyyy',
        multidate: true,
        clearBtn: true,
    });
    $('#month_clear').datepicker({
        format: 'mm-dd-yyyy',
    });
    $('#multi-date').val("").datepicker("update");
    
    $("#date-select").val(format_date_datepicker(pageDate));
    $("#month_clear").val(format_date_datepicker(pageDate));
    $("#date-select").on('dp.change', function(e) {
        // console.log(new Date($(this).val()))
        cDate = format_date(new Date($(this).val()));        
        $('#calendar').fullCalendar('gotoDate', cDate);
        // console.log(cDate)
        get_shifts(cDate);
        $('#month_clear').datepicker("update", $(this).val());
    });

    
    $('.close, .exit, .cancel').on('click', function() {
        // Clear modal inputs
        $('.modal').find('input').val('');
        $('.modal').find('#modal_date').text('');
        $('.modal').find('#id').val('')
        $('.modal').find('#id_user').val('')
        $('.modal').find('#id_shift').val('')
        $('.modal').find('#id_shift_type').val('')

        // hide modal
        $('.modal').modal('hide');
        $('#clear_month').modal('hide');
    });

});  
