$(document).ready(
    function()
    {

        $('.submit').click(function(){
            var actionType = jQuery("<input type='hidden' name='action_type'/>");
            actionType.val(jQuery(this).attr("type"));
            $('#form').append(actionType).submit();
        });

        $('.wUserInfo').click(function(){
            var url = $(this).attr('link');
            $.get(url, {}, function(e) {
                $(".approve").show();
                $(".inner").html(e);
                paging_init("table[data-actual]", url);
            });
        });

        $('.allocation').click(function(){
            var element_id = $(this).attr('id');
            $('.'+element_id).each(function(){
                $(this).toggle();
            })
        });

        $('#ts,#int,#ws').livequery(function(){
            $(this).ajaxForm({
                //beforeSubmit: alert('Get rdy!'),
                success: writeOutput
            })
        });

        $('.delete_button').livequery(function(){
            $(this).click(function(){
                var url = $(this).attr('href');
                $.post(url, function(data) {
                    killer_variable = true;
                    writeOutput();
                });
                return false;
            })
        });

        $('.popup-link').click(function(){
            $(this).colorbox({
                width:'600px',
                href:$(this).attr('data-loader')
            })
        });

        $('.cbox-close').livequery(function() {
            $(this).click(function(){
                jQuery('#cboxClose').click();
            });
        });

        $('.titleNextIcon').click(function(){
            // make some whichcraft
        });

        $('.titlePrevIcon').click(function(){
            // make some whichcraft
        });

        $('#timesheet_calendar').fullCalendar({
            firstDay:1,
            editable: true,
            disableDragging: true,
            contentHeight: 600,
            eventResize: function(event,dayDelta,minuteDelta,revertFunc) {

                $.post($('#timesheet_calendar').attr('clone'), {id:event.id,delta:dayDelta,type:event.className},
                    function(data) {
                        $('#timesheet_calendar').fullCalendar('refetchEvents');
                    });
            },

            /*eventDrop: function(event,dayDelta,minuteDelta,allDay,revertFunc) {
             alert(event.start   );
             },*/

            events: $('#timesheet_calendar').attr('events'),

            loading: function(bool) {
                if (bool) $('#loading').show();
                else $('#loading').hide();
            },

            dayClick: function(date, calEvent, jsEvent, view) {
                var href = $('#timesheet_calendar').attr('add');

                $(this).colorbox({
                    width:'600px',
                    href:$('#timesheet_calendar').attr('add'),
                    onComplete: function() {
                        var ver = getInternetExplorerVersion();

                        day = date.getDate();
                        month = date.getMonth() + 1;

                        if (ver == 7 || ver == 8) {
                            //dear god, please make IE dissappear
                            year = date.getYear();
                        } else {
                            year = date.getYear() + 1900;
                        }

                        $(".datepicker").val(day+'.'+month+'.'+year);
                    }
                });
            },

            eventClick: function(calEvent, jsEvent, view) {
                $(this).colorbox({
                    width:'700px',
                    //href:'/timesheet/edit_'+calEvent.className+'/'+calEvent.id+'/'
                    href:'/timesheet/form/edit/'+calEvent.className+'/'+calEvent.id+'/'
                });
            }

        });
    });
