define([
    'uijet_dir/uijet',
    'explorer',
    'ui/site-menu',
    'ui/sheet-selector',
    'ui/sheet',
    'ui/items-list',
    'ui/comments'
], function (uijet, explorer, site_menu, sheet_selector, sheet, items_list, comments) {

    uijet.declare(site_menu)
        .declare(sheet_selector)
        .declare(sheet)
        .declare(items_list)
        .declare(comments);
    
    return explorer;
});
