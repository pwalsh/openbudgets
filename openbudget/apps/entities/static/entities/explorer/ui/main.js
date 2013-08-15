define([
    'uijet_dir/uijet',
    'explorer',
    'ui/site-menu',
    'ui/sheet',
    'ui/items-list',
    'ui/comments'
], function (uijet, explorer, site_menu, sheet, items_list, comments) {

    uijet.declare(site_menu)
        .declare(sheet)
        .declare(items_list)
        .declare(comments);
    
    return explorer;
});
