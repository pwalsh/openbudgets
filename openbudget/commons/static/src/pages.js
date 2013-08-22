!function (global) {
    var $main = $('#panel-main'),
        main = $main[0],
        $scrolled = $('#main-wrapper').scroller();

    $main.mousewheel(function (e, delta, dx, dy) {
        // prevent the default scrolling and keep it inside the content area
        e.preventDefault();
        $scrolled.scroller('scrollTo', -main.offsetTop - 37*dy);
    });
}(this);
