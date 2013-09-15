define([
    'uijet_dir/uijet',
    'modules/data/backbone',
    'underscore',
    'api',
    'modules/promises/q',
    'backbone-fetch-cache'
], function (uijet, Backbone, _, api) {

    uijet.use({
        prop: function (property) {
            return function (obj) {
                return obj[property];
            };
        }
    }, uijet.utils);

    var 
        /*
         * Muni (Entity) Model
         */
        Muni = uijet.Model({
            idAttribute : 'id'
        }),
        /*
         * Munis (Entities) Collection
         */
        Munis = uijet.Collection({
            model   : Muni,
            url     : function () {
                return api.getRoute('entities');
            },
            parse   : function (response) {
                //! Array.prototype.filter
                return response.results;
            }
        }),
        /*
         * User (Account) Model
         */
        User = uijet.Model({
            idAttribute : 'uuid',
            name        : function () {
                var first = this.get('first_name'),
                    last = this.get('last_name');
                if ( first || last ) {
                    return first + ' ' + last;
                }
                else {
                    return gettext('Guest:');
                }
            },
            avatar      : function () {
                var avatar = this.get('avatar');
                return avatar ? avatar.replace(/s=\d+[^&]/i, 's=90') : window.DEFAULT_AVATAR;
            }
        }),
        /*
         * State Model
         */
        State = uijet.Model({
            idAttribute : 'uuid',
            urlRoot     : function () {
                return api.getRoute('projectStates');
            },
            url         : function () {
                return this.urlRoot() + (this.id ? this.id + '/' : '');
            },
            parse       : function (response) {
                var user = new User(response.author);
                response.author_model = user;
                response.author = user.id;
                return response;
            }
        });

    return {
        api     : api,
        '_'     : _,
        Backbone: Backbone,
        Muni    : Muni,
        Munis   : Munis,
        User    : User,
        State   : State
    };
});
