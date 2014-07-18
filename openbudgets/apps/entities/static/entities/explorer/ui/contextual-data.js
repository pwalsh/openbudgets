define([
    'uijet_dir/uijet',
    'resources'
], function (uijet) {

    return [{
        type    : 'List',
        config  : {
            element         : '#contextual_data',
            item_selector   : 'p',
            mixins          : ['Templated', 'Translated'],
            resource        : 'ContextualData',
            data_events     : {
                change  : 'render'
            },
            signals         : {
                post_init   : function () {
                    delete this.$original_children;
                }
            }
        }
    }];
});
