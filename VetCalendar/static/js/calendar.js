function build_cal(cal_date) {
     
    // schedule.forEach((item)=>{                
    //     console.log(item)
    //     Object.entries(item).forEach((i1)=>{
    //         console.log(i1)
    //     })
    //     // {
    //     //     title: `${item[title]}`,
    //     //     start: `${item[start]}`
    //     // },
    // })
    console.log("date: ", cal_date)
    $('#calendar').fullCalendar({        
        timeZone: 'local',
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,basicWeek,basicDay'
        },
        defaultDate: cal_date, // 2023-02-24 
        navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        height: 1200,
        events:[ 
            
        ]
    });
};        

function format_date(date) {
    // console.log("Date: " + date);
    var dd = String(date.getDate()).padStart(2, '0');
    var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = date.getFullYear(); 
    // console.log(mm, dd);
    return yyyy + '-' + mm  + '-' + dd
    // return yyyy + mm + dd
}

function add_events(schedule){
    // console.log(schedule);  
    var myCalendar = $('#calendar'); 
    myCalendar.fullCalendar('removeEvents');
    // myCalendar.fullCalendar();
    schedule.forEach((item)=>{
        // console.log(item.start.toString())
        var new_start = item.start.toString() + "T" + item.time.toString()
        var myEvent = {
            title: "" + item.title.toString() + "",
            start: new_start,
            color: "" + item.color.toString() + "",            
        };
        // console.log(item.color.toString())
        // console.log(new_start)
        myCalendar.fullCalendar( 'renderEvent', myEvent );
    });
}

function get_shifts(date) {                      
    var data
    $.ajax({                                        
        url: "/get_shifts/" + date + "",
        success: function (response){            
            //console.log(response.schedule);
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

function update_shift_list(date) {
    // console.log("update_shift_list: ", date)
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

var pageDate = new Date()
var initDate = format_date(pageDate);
// var initDate = moment(new Date(pageDate)).format('YYYY/MM/DD');

$(document).ready(function () {     
    // console.log(initDate);
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
        // $("#date-select").val(format_date_datepicker(new Date(getDate)));
        // $("#month_clear").val(format_date_datepicker(new Date(getDate)));
        // var view = $('#calendar').fullCalendar('getView');
        // console.log("1st: " + calDate);
        get_shifts(getDate);
        update_shift_list(getDate);
        // pageDate.setMonth(pageDate.getMonth()+1);
        // calDate = format_date(pageDate);
    });
});  
