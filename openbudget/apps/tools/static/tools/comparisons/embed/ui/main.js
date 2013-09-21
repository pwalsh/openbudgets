define([
    'uijet_dir/uijet',
    'app',
    'ui/header',
    'ui/chart',
    'ui/footer'
], function (uijet, app, header, chart, footer) {

    uijet.declare(header)
        .declare(chart)
        .declare(footer);

    app();

});
