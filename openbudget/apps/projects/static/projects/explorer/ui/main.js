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
            mixins      : ['Layered']
        }
    }, {
        type    : 'Pane',
        config  : {
            element         : '#loading',
            mixins          : ['Transitioned'],
            adapters        : ['Spin'],
            animation_type  : 'slide',
            signals         : {
                post_wake   : 'spin',
                pre_sleep   : 'spinOff'
            },
            app_events      : {
                'api_routes_set': 'sleep'
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
