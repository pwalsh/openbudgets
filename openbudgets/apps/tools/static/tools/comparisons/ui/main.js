define([
    'uijet_dir/uijet',
    'comparisons',
    'ui/legend',
    'ui/legend-list',
    'ui/normalization-select',
    'ui/site-menu',
    'ui/entities',
    'ui/entities-list',
    'ui/nodes',
    'ui/breadcrumbs',
    'ui/search-crumb',
    'ui/nodes-list',
    'ui/nodes-search',
    'ui/search-filter',
    'ui/nodes-footer',
    'ui/chart-container',
    'ui/chart-header-buttons',
    'ui/chart-heading',
    'ui/chart',
    'ui/chart-period-selects'
], function (uijet, comparisons, legend, legend_list, normalization_select, site_menu,
    entities, entities_list, nodes, breadcrumbs, search_crumb, nodes_list, nodes_search,
    search_filter, nodes_footer, chart_container, chart_header_buttons, chart_heading,
    chart, chart_period_selects) {

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
        .declare(legend_list)
        .declare(site_menu)
        .declare(entities)
        .declare(entities_list)
        .declare(normalization_select)
        .declare(nodes)
        .declare(breadcrumbs)
        .declare(search_crumb)
        .declare(nodes_list)
        .declare(nodes_search)
        .declare(search_filter)
        .declare(nodes_footer)
        .declare(chart_container)
        .declare(chart_header_buttons)
        .declare(chart_heading)
        .declare(chart)
        .declare(chart_period_selects);

    return comparisons;
});
