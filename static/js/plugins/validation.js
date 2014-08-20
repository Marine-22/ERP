var killer_variable;

(function($) {
    function inputs(form)   {
        return form.find(":input:visible:not(:button)");
    }

    $.fn.validate = function(url, settings) {
        settings = $.extend({
            type: 'table',
            callback: false,
            fields: false,
            dom: this,
            event: 'submit',
            submitHandler: null
        }, settings);

        return this.each(function() {
            var form = $(this);
            settings.dom.bind(settings.event, function()  {
                var status = false;
                var data = form.serialize();
                if (settings.fields) {
                    data += '&' + $.param({fields: settings.fields});
                }
                $.ajax({
                    async: false,
                    data: data,
                    dataType: 'json',
                    traditional: true,
                    error: function(XHR, textStatus, errorThrown)   {
                        status = true;
                    },
                    success: function(data, textStatus) {
                        status = data.valid;
                        killer_variable = status;
                        if (!status)    {
                            if (settings.callback)  {
                                settings.callback(data, form);
                            }
                            else    {
                                var get_form_error_position = function(key) {
                                    key = key || '__all__';
                                    if (key == '__all__') {
                                        var filter = ':first';
                                    } else {
                                        var filter = ':first[id^=id_' + key.replace('__all__', '') + ']';
                                    }
                                    return inputs(form).filter(filter).parent();
                                };

                                if (settings.type == 'growl')  {
                                    $.each(data.errors, function(key, val)  {
                                        if (key.indexOf('__all__') >= 0)   {
                                            get_form_error_position(key).before('<li><ul class="errorlist"><li>' + val + '</li></ul></li>');
                                        }
                                        else    {
                                            $.achtung({message: ''+val+'', timeout:5, className:'achtung-error'});
                                        }
                                    });
                                }
                            }
                        }
                    },
                    type: 'POST',
                    url: url
                });
                if (status && settings.submitHandler) {
                    return settings.submitHandler.apply(this);
                }
                return status;
            });
        });
    };
})(jQuery);
