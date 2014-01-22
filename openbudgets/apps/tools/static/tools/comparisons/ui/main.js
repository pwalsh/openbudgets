define([
    'uijet_dir/uijet',
    'comparisons',
    'ui/legend',
    'ui/site-menu',
    'ui/entities',
    'ui/nodes',
    'ui/nodes-list',
    'ui/nodes-footer',
    'ui/chart-container',
    'ui/chart-header-buttons',
    'ui/chart-heading',
    'ui/chart',
    'ui/chart-period-selects'
], function (uijet, comparisons, legend, site_menu, entities, nodes, nodes_list, nodes_footer, chart_container, chart_header_buttons, chart_heading, chart, chart_period_selects) {

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
        .declare(nodes_footer)
        .declare(nodes_list)
        .declare(chart_container)
        .declare(chart_header_buttons)
        .declare(chart_heading)
        .declare(chart)
        .declare(chart_period_selects);

    return comparisons;
});
