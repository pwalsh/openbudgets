
//******************/
//**** OVERLAYS ****/
//******************/
(function () {

    $('#overlay .close').click(function (event) {
        $('[id^="overlay"]').hide();
    });

    $('.login-link').click(function (event) {
        event.preventDefault();
        $('#overlay, #overlay .close').show();
        $('#overlay-login').show();
        $('#overlay-register').hide();
        $('#overlay-password-reset').hide();
        $('#overlay-password-change').hide();
    });

    $('.register-link').click(function (event) {
        event.preventDefault();
        $('#overlay, #overlay .close').show();
        $('#overlay-register').show();
        $('#overlay-login').hide();
        $('#overlay-password-reset').hide();
        $('#overlay-password-change').hide();
    });

    $('.password-reset-link').click(function (event) {
        event.preventDefault();
        $('#overlay, #overlay .close').show();
        $('#overlay-password-reset').show();
        $('#overlay-register').hide();
        $('#overlay-login').hide();
        $('#overlay-password-change').hide();
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


