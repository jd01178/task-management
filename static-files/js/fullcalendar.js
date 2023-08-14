let getCalendarData = async () => {
    let taskData = await sendGetRequest('/api/v1/calendar-tasks/')
    let googleEventData = await sendGetRequest('/api/v1/calendar-events/')
    return taskData.concat(googleEventData)
}



//Full Calendar
document.addEventListener('DOMContentLoaded', async function () {
    var containerEl = document.getElementById('external-events');
    new FullCalendar.Draggable(containerEl, {
        itemSelector: '.fc-event',
        eventData: function (eventEl) {
            return {
                title: eventEl.innerText.trim(),
                title: eventEl.innerText,
                className: eventEl.className + ' overflow-hidden '
            }
        }
    });
    var calendarEl = document.getElementById('calendar2');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },

        defaultView: 'month',
        navLinks: true, // can click day/week names to navigate views
        businessHours: true, // display business hours
        editable: true,
        selectable: true,
        selectMirror: true,
        droppable: true, // this allows things to be dropped onto the calendar
        select: function (arg) {
            var title = prompt('Task Title:');
            if (title) {
                calendar.addEvent({
                    title: title,
                    start: arg.start,
                    end: arg.end,
                    allDay: arg.allDay
                })
            }
            calendar.unselect()
        },
        eventClick: function (arg) {
            if (confirm('Are you sure you want to delete this task?')) {
                arg.event.remove()
            }
        },
        editable: true,
        dayMaxEvents: true, // allow "more" link when too many events
        events: await getCalendarData(),
    });

    calendar.render();
});


//List FullCalendar
document.addEventListener('DOMContentLoaded', async function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        height: 'auto',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'listDay,listWeek'
        },

        // customize the button names,
        // otherwise they'd all just say "list"
        views: {
            listDay: {buttonText: 'list day'},
            listWeek: {buttonText: 'list week'}
        },
        initialView: 'listWeek',
        initialDate: new Date(),
        navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        dayMaxEvents: true, // allow "more" link when too many events
        events: await getCalendarData(),
    });

    calendar.render();
});