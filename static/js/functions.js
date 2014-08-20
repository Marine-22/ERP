function getInternetExplorerVersion()
// Returns the version of Internet Explorer or a -1
// (indicating the use of another browser).
{
    var rv = -1; // Return value assumes failure.
    if (navigator.appName == 'Microsoft Internet Explorer')
    {
        var ua = navigator.userAgent;
        var re  = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
        if (re.exec(ua) != null)
            rv = parseFloat( RegExp.$1 );
    }
    return rv;
}

function writeOutput() {
    //$('#timesheet_calendar').fullCalendar('refetchEvents');
    //jQuery('#cboxClose').click();
    if (killer_variable) {
        $('#timesheet_calendar').fullCalendar('refetchEvents');
        jQuery('#cboxClose').click();
    }
}