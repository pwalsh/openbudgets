
//******************/
//****  FORMS   ****/
//******************/
(function () {

    var $forms = $('form.modal'),
        valid_class = 'valid',
        invalid_class = 'invalid',
        help_class = 'help',
        changeHandler = function () {
            var valid = true,
                $this = $(this);
            $this.next().hide();
            if ( this.type in validation_map ) {
                valid = validation_map[this.type].test(this.value);
            }
            if ( valid ) {
                $this.addClass(valid_class);
                $this.removeClass(invalid_class);
                $this.closest('form').trigger('validate');
            }
            else {
                $this.addClass(invalid_class);
                $this.removeClass(valid_class);
            }
        },
        editHandler = function (e) {
            var $this = $(this);
            $this.removeClass('valid invalid')
                .next()
                    .show();
        },
        validateHandler = function () {
            var valid = false,
                $form = $(this).find('input').each(function () {
                            if ( this.type in validation_map ) {
                                if ( ! validation_map[this.type].test($(this).val()) ) {
                                    valid = false;
                                    // break
                                    return false;
                                }
                            }
                            valid = true;
                        });
            $form.trigger(valid ? 'valid' : 'invalid');
        },
        validHandler = function () {
            $(this).find('.mock-button').addClass('hide')
                .end().find('input[type=submit]').removeClass('hide');
        },
        invalidHandler = function () {
            $(this).find('input[type=submit]').addClass('hide')
                .end().find('.mock-button').removeClass('hide');
        },
        validation_map = {};

    $forms.on({
            validate: validateHandler,
            valid   : validHandler,
            invalid : invalidHandler
        })
        .each(function (i, form) {
            $(form).find('input')
                .on('change', changeHandler)
                .on('focus', editHandler)
                .each(function (i, input) {
                    var $input = $(input),
                        pattern = $input.attr('pattern'),
                        type = input.type;
                    if ( pattern && ! (type in validation_map) ) {
                        validation_map[type] = RegExp(pattern);
                    }
                });
        });

    $forms.submit(function(event) {
        var $form = $(this),
            notices = $form.find('.notices');
        event.preventDefault();

        $.ajax({
            type: $form.attr("method"),
            url: $form.attr("action"),
            data: $form.serialize(),
            dataType: "json"
        })

        //form_submit.val('Wait please').attr('disabled', 'disabled');

        .done(function(response) {
            notices.html(response.data);
        })

        .fail(function(jqXHR, textStatus) {
            notices.html('FAIL: ' + textStatus);
        });
    });

}());


//******************/
//**** OVERLAYS ****/
//******************/
(function () {

    $('#overlay .close, .mock-button').click(function (event) {
        $('[id^="overlay"]').hide();
    });

    $('.login-link').click(function (event) {
        event.preventDefault();
        $('form').removeAttr('id');
        $('#overlay-login form').attr('id', 'active-form');
        $('#overlay, #overlay .close').show();
        $('#overlay-login').show();
        $('#overlay-register').hide();
        $('#overlay-password-reset').hide();
        $('#overlay-password-change').hide();
    });

    $('.register-link').click(function (event) {
        event.preventDefault();
        $('form').removeAttr('id');
        $('#overlay-register form').attr('id', 'active-form');
        $('#overlay, #overlay .close').show();
        $('#overlay-register').show();
        $('#overlay-login').hide();
        $('#overlay-password-reset').hide();
        $('#overlay-password-change').hide();
    });

    $('.password-reset-link').click(function (event) {
        event.preventDefault();
        $('form').removeAttr('id');
        $('#overlay-password-reset form').attr('id', 'active-form');
        $('#overlay, #overlay .close').show();
        $('#overlay-password-reset').show();
        $('#overlay-register').hide();
        $('#overlay-login').hide();
        $('#overlay-password-change').hide();
    });

    $('.password-change-link').click(function (event) {
        event.preventDefault();
        $('form').removeAttr('id');
        $('#overlay-password-change form').attr('id', 'active-form');
        $('#overlay, #overlay .close').show();
        $('#overlay-password-change').show();
        $('#overlay-register').hide();
        $('#overlay-login').hide();
        $('#overlay-password-show').hide();
    });

}());



// NAV PANEL UX
(function () {

    $('#nav-anchor').mouseenter(function (event) {
        event.preventDefault();
        $('#nav-panel').show();
    });

    $('#nav-panel').mouseleave(function () {
        $('#nav-panel').hide();
    });

    $('#nav-panel-close').click(function () {
        $('#nav-panel').hide();
    });

}());

// USER PANEL UX
(function () {

    $('.account').hover(function (event) {
        event.preventDefault();
        $('.actions').toggle();
    });

}());


