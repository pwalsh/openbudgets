define([
    'uijet_dir/uijet',
    'explorer',
    'ui/site-menu',
    'ui/sheet',
    'ui/items-list'
], function (uijet, explorer, site_menu, sheet, items_list) {

    uijet.declare(site_menu)
        .declare(sheet)
        .declare(items_list);
    
    return explorer;
});
