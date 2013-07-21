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
