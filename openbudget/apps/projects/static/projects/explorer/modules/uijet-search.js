define([
    'uijet_dir/uijet'
], function (uijet) {

    function SearchIndex (options) {
        if ( ! (this instanceof  SearchIndex) ) return new SearchIndex(options);
        options = options || {};
        this.fields = options.fields;
        this.ref = options.ref || 'id';
        this.documents = []
    }
    
    SearchIndex.prototype = {
        constructor : SearchIndex,
        add         : function () {
            this.documents = this.documents.concat.apply(this.documents, arguments);
            return this;
        },
        search      : function (term) {
            var results = [],
                fields = this.fields,
                re = new RegExp(term);
            this.documents.forEach(function (item) {
                var field;
                for ( field in fields ) {
                    if ( fields in item && re.test(item[field]) ) {
                        results.push(item[this.ref]);
                        break;
                    }
                }
            }, this);
            return results;
        }
    };

    uijet.use({
        search  : {
            Index   : SearchIndex
        }
    });

});
