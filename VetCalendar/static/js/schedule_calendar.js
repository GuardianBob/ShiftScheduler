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
        defaultDate: cal_date,
        events:[             
        ],
        navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        selectable: true,
        selectHelper: true,
        height:900,
        select: function(start, end) {
            // Display the modal.
            // You could fill in the start and end fields based on the parameters
            $('.modal').modal('show');
            $('.modal').find('#modal_date, #id_date').text(start.format("MMM-DD-YYYY"));
            $('.modal').find('#date').val(start.format("MM-DD-YYYY"));

        },
        eventClick: function(event, element) {
            // Display the modal and set the values to the event values.
            $('.modal').modal('show');
            $('.modal').find('#modal_date, #id_date').text(event.start.format("MMM-DD-YYYY"));
            $('.modal').find('#date').val(event.start.format("MM-DD-YYYY"));
            $('.modal').find('#id').val(event.id)
            $('.modal').find('#delete_shift').attr('href', "/delete_sched_shift/" + event.id)
            // console.log(event.start.format("MM-DD-YYYY"))
            $('.modal').find('[name=user] option').filter(function(){
                return ($(this).text() == event.title);
            }).prop('selected', true);
            $('.modal').find('[name=shift] option').filter(function(){
                // console.log(event.id);
                return ($(this).text() == event.startStr);                
            }).prop('selected', true);
            // $('.modal').find('#starts-at').val(event.start);
            // $('.modal').find('#ends-at').val(event.end);
            $('.modal').find('[name=shift_type] option').filter(function(){
                return ($(this).text() == event.endStr);                
            }).prop('selected', true);
        },
        
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
            // update_shift_list(response.schedule)
            data = response.schedule
            return data         
        },
        error: function (response) {
            // alert the error if any error occured
            console.log(response.responseJSON.errors)
        }
    });    
    // return data;
}

function update_shift_list(date) {
    $.ajax({                                        
        url: "/get_shift_count/" + date + "",
        success: function (response){            
            // console.log(response.shift_count);
            $("#shift_counts tr").remove();
            $.each( response.shift_count, function(id, user) {                
                // console.log(user.name.toString());
                html = `<tr><td><a href="/users/info/${id}">${user.name.toString()}</a></td><td>${user.month.toString()}</td><td>${user.year.toString()}</td></tr>`;
                $("#shift_counts").append(html);
            });
            shifts = response
            return shifts         
        },
        error: function (response) {
            // alert the error if any error occured
            console.log(response.responseJSON.errors)
        }
    });
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
        var getDate = $('#calendar').fullCalendar('getDate').format("YYYY-MM-DD");
        // console.log("getDate: " + getDate);
        // console.log("fixed: " + new Date(getDate));
        calDate = format_date(new Date(getDate));
        $("#date-select").val(format_date_datepicker(new Date(getDate)));
        $("#month_clear").val(format_date_datepicker(new Date(getDate)));
        // var view = $('#calendar').fullCalendar('getView');
        // console.log("1st: " + calDate);
        get_shifts(getDate);
        update_shift_list(getDate);
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
        console.log(e.date)
        console.log(new Date(e.date))
        cDate = format_date(new Date(e.date));   
        $('#calendar').fullCalendar('gotoDate', cDate);
        console.log(cDate)
        get_shifts(cDate);
        $('#month_clear').datepicker("update", $(this).val());
    });

    
        // Whenever the user clicks on the "save" button om the dialog
    // $('#save-event').on('click', function() {
    //     $("#modal_form").submit();
    //     // var title = $('#title').val();
    //     // if (title) {
    //     //     var eventData = {
    //     //         title: title,
    //     //         start: $('#starts-at').val({
    //     //             format: 'DD/MM/YYYY'
    //     //         }),
    //     //         end: $('#ends-at').val()
    //     //     };
    //     //     $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
    //     // }
    //     // $('#calendar').fullCalendar('unselect');

    //     // Clear modal inputs
    //     $('.modal').find('input').val('');

    //     // hide modal
    //     $('.modal').modal('hide');        
    // });
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
