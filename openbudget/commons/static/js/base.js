
//******************/
//****  FORMS   ****/
//******************/
(function () {

    var form = $('form'),
        notices = $('form .notices'),
        $inputs = $('form :input'),
        values = {},
        request;

    $('form').h5Validate({
        errorClass: 'invalid',
        validClass: 'valid',
        focusout: true,
        focusin: false,
        change: false,
        keyup: false
    });

    $('input').focus(function (event) {
        $(this).removeClass('invalid valid');
        $(this).siblings('.help').show();
    });

    $('input').blur(function (event) {
        $(this).siblings('.help').hide();
    });

    form.submit(function(event) {
        event.preventDefault();

        request = $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            dataType: "json"
        });

        //form_submit.val('Wait please').attr('disabled', 'disabled');

        request.done(function(response) {
            notices.html(response.data);
        });

        request.fail(function(jqXHR, textStatus) {
            notices.html('FAIL: ' + textStatus);
        });
    });

}());


//******************/
//**** OVERLAYS ****/
//******************/
(function () {

    $('#overlay .close, .disabled-event-catcher').click(function (event) {
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


