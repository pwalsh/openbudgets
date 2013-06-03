define([
    'uijet_dir/uijet',
    'explorer',
    'project_widgets/ClearableTextInput'
], function (uijet, Explorer) {

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element : '#legends',
            position: 'right:350 fluid'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#add_legend',
            position: 'top:50px fluid'
        }
    }, {
        type    : 'List',
        config  : {
            element : '#legends_list',
            position: 'fluid'
        }
    }, {
        type    : 'Pane',
        config  : {
            element         : '#entity_filter',
            dont_wake       : true,
            mixins          : ['Transitioned'],
            animation_type  : 'slide',
            app_events      : {
                'add_legend.clicked'            : 'wake',
                'entity_filter_close.clicked'   : 'sleep'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#entity_filter_close'
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
            }
        }
    }, {
        type    : 'List',
        config  : {
            element     : '#entities_list',
            mixins      : ['Templated', 'Scrolled'],
            adapters    : ['jqWheelScroll', 'Spin'],
            resource    : 'Munis',
            position    : 'top|50 fluid',
            search      : {
                fields  : {
                    code    : 20,
                    name    : 10,
                    name_en : 10,
                    name_ru : 10
                }
            },
            signals     : {
                pre_update      : 'spin',
                post_fetch_data : function () {
                    this.spinOff()
                        .index().search_index.add( this.resource.toJSON() );
                },
                pre_wake        : function () {
                    return ! this.has_content;
                },
                post_render     : function () {
                    this.$children = this.$element.children();
                    this.publish('rendered');
                }
            },
            app_events  : {
                'entity_field.changed'  : function (value) {
                    if ( this.has_data && this.$children ) {
                        var results = this.search(value),
                            filter = function (i, item) {
                                return ~ results.indexOf(+uijet.$(item).attr('data-id'));
                            };
                        this.$children.filter(filter).removeClass('removed');
                        this.$children.not(filter).addClass('removed');
                        this.publish('filtered');
                    }
                    else {
                        var _self = arguments.callee;
                        if ( 'cached_value' in this ) {
                            this.cached_value = value;
                        }
                        else {
                            this.cached_value = value;
                            this.subscribe('entities_list.rendered', function () {
                                this.unsubscribe('entities_list.rendered');
                                _self.call(this, this.cached_value);
                                delete this.cached_value;
                            });
                        }
                    }
                },
                'entities_list.filtered': 'scroll'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element : '#nodes_picker',
            position: 'fluid'
        }
    }, {
        type    : 'Pane',
        config  : {
            element : '#nodes_filters',
            position: 'top:100 fluid'
        }
    }, {
        type    : 'ClearableTextInput',
        config  : {
            element : '#nodes_search'
        }
//    }, {
//        type    : 'List',
//        config  : {
//            element     : '#nodes_breadcrumbs',
//            adapters    : ['Breadcrumbs'],
//            horizontal  : true,
//            dont_wake   : true,
//            app_events  : {
//                'nodes_list.ready'  : function () {}
//            }
//        }
    }, {
        type    : 'List',
        config  : {
            element     : '#nodes_list',
            dont_wake   : true,
            position    : 'fluid',
            mixins      : ['Templated', 'Scrolled'],
            adapters    : ['jqWheelScroll', 'Spin'],
            resource    : 'LatestTemplate',
            search      : {
                fields  : {
                    name        : 10,
                    description : 1,
                    code        : 20
                }
            },
            signals     : {
                pre_wake        : function () {
                    return this.changed;
                },
                pre_update      : 'spin',
                post_fetch_data : 'spinOff',
                post_wake       : function () {
                    if ( this.changed ) {
                        this.index().search_index.add(this.getData(this.context)
                            //! Array.prototype.map
                            .map(function (model) {
                                return model.attributes;
                            })
                        );
                        this.publish('ready', this.context);
                    }
                }
            },
            app_events  : {
                'entities_list.selected'    : function ($selected) {
                    var entity_id = $selected.attr('data-id');
                    if ( this.latest_entity_id !== entity_id ) {
                        this.latest_entity_id = entity_id;
                        this.changed = true;
                        this.resource.url = API_URL + 'nodes/latest/' + entity_id + '/';
                        this.wake({
                            parent  : null
                        });
                    }
                    else {
                        this.changed = false;
                        this.wake();
                    }
                }
            }
        }
    }]);

    return Explorer;
});
