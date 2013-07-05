define([
    'uijet_dir/uijet',
    'api',
    'explorer',
    'project_widgets/ClearableTextInput',
    'project_widgets/FilteredList'
], function (uijet, api, explorer) {

    return [{
        type    : 'Pane',
        config  : {
            element         : '#entity_selection',
            dont_wake       : true,
            mixins          : ['Transitioned', 'Layered'],
            animation_type  : 'fade',
            app_events      : {
                'add_legend.clicked'        : 'wake',
                'add_legend_cancel.clicked' : 'sleep',
                'entities_list.selected'    : 'sleep'
            }
        }
    }, {
        type    : 'ClearableTextInput',
        config  : {
            element     : '#entity_field',
            button      : {
                signals : {
                    pre_click   : '-entity_field.changed'
                }
            },
            dom_events  : {
                keyup   : function (e) {
                    this.publish('changed', e.target.value);
                }
            },
            signals     : {
                post_wake   : function () {
                    this.$element.focus();
                }
            }
        }
    }, {
        type    : 'FilteredList',
        config  : {
            element     : '#entities_list',
            mixins      : ['Templated', 'Scrolled'],
            adapters    : ['jqWheelScroll', 'Spin'],
            resource    : 'Munis',
            dont_wake   : true,
            position    : 'top|120px bottom fluid',
            search      : {
                fields  : {
                    code    : 20,
                    name    : 10,
                    name_en : 10,
                    name_ru : 10,
                    name_ar : 10
                }
            },
            filters     : {
                search  : 'search'
            },
            signals     : {
                pre_update      : 'spin',
                post_fetch_data : function () {
                    this.spinOff()
                        .index().search_index.add( this.resource.toJSON() );
                },
                pre_wake        : function () {
                    if ( this.has_content ) {
                        return false;
                    }
                    else {
                        this.resource.url = api.getRoute('entities') + '?division__budgeting=True';
                    }
                },
                post_render     : function () {
                    this.$children = this.$element.children();
                    this.publish('rendered');
                },
                pre_select      : function ($selected) {
                    return +$selected.attr('data-id');
                }
            },
            app_events  : {
                'api_routes_set'        : function () {
                    this.options.dont_wake = false;
                    this.wake();
                },
                'entity_field.changed'  : 'filterBySearch+',
                'entities_list.filtered': 'scroll'
            }
        }
    }];

});
