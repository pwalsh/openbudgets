define([
    'uijet_dir/uijet',
    'explorer',
    'ui/filters',
    'ui/nodes',
    'ui/nodes-list',
    'ui/chart'
], function (uijet, Explorer, filters, nodes, nodes_list, chart) {

    uijet.declare(filters)
        .declare(nodes)
        .declare(nodes_list)
        .declare(chart);

    return Explorer;
});
