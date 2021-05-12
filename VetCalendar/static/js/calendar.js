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
    $('#calendar').fullCalendar({        
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,basicWeek,basicDay'
        },
        defaultDate: '"' + cal_date + '"',
        navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events:[ 
            
        ]
    });
};        

function format_date(date) {
    var dd = String(date.getDate()).padStart(2, '0');
    var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = date.getFullYear(); 
    return yyyy + '-' + mm  + '-' + dd
}

function add_events(schedule){
    console.log(schedule);  
    var myCalendar = $('#calendar'); 
    myCalendar.fullCalendar();
    schedule.forEach((item)=>{
        // console.log(item.title.toString())
        var myEvent = {
            title: "" + item.title.toString() + "",
            start: "'" + item.start.toString() + "'"
        };
        myCalendar.fullCalendar( 'renderEvent', myEvent );
    });
}

function get_shifts(date, change) {                      
    var data
    $.ajax({                                        
        url: "/get_shifts/" + date + "/" + change + "",
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

var pageDate = new Date()
var calDate = format_date(pageDate);

$(document).ready(function() {       
    console.log(calDate); 
    build_cal(calDate);    
    var data = get_shifts(calDate, "none");
    //var schedule = {{ schedule }};
    // console.log(data)
    // fillCal(data.calDate, data.schedule);
    $('.fc-next-button').click(function() {
        console.log("clicked!");  
        get_shifts(calDate, "next");
        pageDate.setMonth(pageDate.getMonth()+1);
        calDate = format_date(pageDate);
    });
    $('.fc-prev-button').click(function() {
        console.log("clicked!");  
        get_shifts(calDate, "prev");
        pageDate.setMonth(pageDate.getMonth()-1);
        calDate = format_date(pageDate);
    });
});  


// $(document).ready(function() {
//     var today = new Date();
//     $('#calendar').fullCalendar({        
//         header: {
//             left: 'prev,next today',
//             center: 'title',
//             right: 'month,basicWeek,basicDay'
//         },
//         defaultDate: today,
//         navLinks: true, // can click day/week names to navigate views
//         editable: true,
//         eventLimit: true, // allow "more" link when too many events
//         events: [     
//             {
//                 title: 'All Day Event',
//                 start: '2021-05-01'
//             },
//             {
//                 title: 'Long Event',
//                 start: '2021-05-07',
//                 end: '2021-05-10'
//             },
//             {
//                 id: 999,
//                 title: 'Repeating Event',
//                 start: '2021-05-09T16:00:00'
//             },
//             {
//                 id: 999,
//                 title: 'Repeating Event',
//                 start: '2021-05-16T16:00:00'
//             },
//             {
//                 title: 'Conference',
//                 start: '2021-05-11',
//                 end: '2021-05-13'
//             }
//         ]
//     });
    
// });

