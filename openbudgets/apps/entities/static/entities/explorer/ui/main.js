define([
    'uijet_dir/uijet',
    'explorer',
    'ui/site-menu',
    'ui/sheet-selector',
    'ui/sheet',
    'ui/breadcrumbs',
    'ui/items-list',
    'ui/comments',
    'ui/footer',
    // deps automatically loaded via uijet and undetectable by r.js
    'uijet_dir/widgets/Pane',
    'uijet_dir/mixins/Layered',
    'uijet_dir/mixins/Toggled',
    'uijet_dir/mixins/Templated',
    'uijet_dir/mixins/Scrolled',
    'uijet_dir/adapters/Spin',
    'uijet_dir/adapters/jqWheelScroll'
], function (uijet, explorer, site_menu, sheet_selector, sheet, breadcrumbs, items_list, comments, footer) {

    uijet.declare(site_menu)
        .declare(sheet_selector)
        .declare(sheet)
        .declare(breadcrumbs)
        .declare(items_list)
        .declare(comments)
        .declare(footer);
    
    return explorer;
});
