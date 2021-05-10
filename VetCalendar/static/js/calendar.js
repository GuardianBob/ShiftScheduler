$(document).ready(function() {
    var today = new Date();
    $('#calendar').fullCalendar({        
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,basicWeek,basicDay'
        },
        defaultDate: today,
        navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: [
            {
                title: 'All Day Event',
                start: '2021-05-01'
            },
            {
                title: 'Long Event',
                start: '2021-05-07',
                end: '2021-05-10'
            },
            {
                id: 999,
                title: 'Repeating Event',
                start: '2021-05-09T16:00:00'
            },
            {
                id: 999,
                title: 'Repeating Event',
                start: '2021-05-16T16:00:00'
            },
            {
                title: 'Conference',
                start: '2021-05-11',
                end: '2021-05-13'
            },
            {
                title: 'Meeting',
                start: '2021-05-12T10:30:00',
                end: '2021-05-12T12:30:00'
            },
            {
                title: 'Lunch',
                start: '2021-05-12T12:00'
            },
            {
                title: 'Meeting',
                start: '2021-05-12T14:30:00'
            },
            {
                title: 'Happy Hour',
                start: '2021-05-12T17:30:00'
            },
            {
                title: 'Dinner',
                start: '2021-05-12T20:00:00'
            },
            {
                title: 'Birthday Party',
                start: '2021-05-13T07:00:00'
            },
            {
                title: 'Click for Google',
                url: 'https://google.com/',
                start: '2021-05-28'
            }
        ]
    });
    
});