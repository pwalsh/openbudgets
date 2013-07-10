define([
    'uijet_dir/uijet',
    'explorer',
    'ui/legend',
    'ui/site-menu',
    'ui/entities',
    'ui/nodes',
    'ui/nodes-list',
    'ui/chart'
], function (uijet, explorer, legend, site_menu, entities, nodes, nodes_list, chart) {

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element     : '#welcome',
            mixins      : ['Layered'],
            app_events  : {
                welcome : 'wake'
            }
        }
    }])
        .declare(legend)
        .declare(site_menu)
        .declare(entities)
        .declare(nodes)
        .declare(nodes_list)
        .declare(chart);

    return explorer;
});
