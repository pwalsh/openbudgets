define([
    'uijet_dir/uijet'
], function (uijet) {

    var Store = window.localStorage;

    uijet.use({
        storage : {
            has : function (key) {
                return this.get(key) !== null;
            },
            set : function (key, data) {
                Store.setItem(key, typeof data == 'string' ? data : JSON.stringify(data));
                return this;
            },
            get : function (key) {
                var value = Store.getItem(key);
                return typeof value == 'string' ? JSON.parse(value) : value;
            },
            del : function (key) {
                Store.removeItem(key);
                return this;
            }
        }
    });
});