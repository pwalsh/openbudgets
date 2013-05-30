define([
    'uijet_dir/uijet',
    'modules/data/backbone',
    'underscore'
], function (uijet, Backbone, _) {

    var
        /*
         * Muni (Entity) Model
         */
        Muni = uijet.Model({
            idAttribute : 'uuid'
        }),
        /*
         * Munis (Entities) Collection
         */
        Munis = uijet.Collection({
            model   : Muni,
            url     : API_URL + 'entity/',
            parse   : function (response) {
                //! Array.prototype.filter
                return response.results.filter(function (item) {
                    return item.division.index === 3;
                });
            }
        });

    return {
        Munis   : Munis
    };
});
