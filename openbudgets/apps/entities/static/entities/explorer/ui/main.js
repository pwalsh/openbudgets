define([
    'uijet_dir/uijet',
    'explorer',
    'ui/site-menu',
    'ui/sheet-selector',
    'ui/sheet',
    'ui/breadcrumbs',
    'ui/items-list',
    'ui/comments',
    'ui/footer'
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
