define([
    'uijet_dir/uijet'
], function (uijet) {

    return [{
        type    : 'Pane',
        config  : {
            element     : '#chart_heading',
            mixins      : ['Templated', 'Translated'],
            resource    : 'ToolState',
            dont_fetch  : true,
            data_events : {
                'change:title'  : 'title_changed'
            },
            signals     : {
                pre_wake    : function () {
                    return ! this.has_content;
                },
                post_render : function () {
                    uijet.start({
                        type    : 'ContentEditable',
                        config  : {
                            element     : '#chart_heading_title',
                            container   : this.id,
                            input       : {
                                name        : 'title',
                                placeholder : gettext('Insert title')
                            },
                            signals     : {
                                post_init   : function () {
                                    this.reset(uijet.Resource('ToolState').get('title'), true);
                                }
                            },
                            app_events  : {
                                'chart_heading.title_changed'   : function (data) {
                                    this.reset(data.args[1], true);
                                }
                            }
                        }
                    });
                    this.wakeContained();
                }
            },
            app_events  : {
                'chart_heading_title.updated'   : function (value) {
                    this.resource.set({ title : value }, { silent : true });
                }
            }
        }
    }];

});
