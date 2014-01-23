define([
    'uijet_dir/uijet',
    'api',
    'comparisons',
    'tool_widgets/FilteredList'
], function (uijet, ui, comparisons) {

    return {
        type    : 'FilteredList',
        config  : {
            element         : '#entities_list',
            mixins          : ['Templated', 'Scrolled', 'Deferred'],
            adapters        : ['jqWheelScroll', 'Spin'],
            resource        : 'Munis',
            promise         : comparisons.routes_set_promise,
            position        : 'top|120px bottom fluid',
            fetch_options   : {
                data: {
                    has_sheets  : true,
                    page_by     : 300,
                    ordering    : 'name'
                }
            },
            search          : {
                fields  : {
                    code    : 20,
                    name    : 10,
                    name_en : 10,
                    name_ru : 10,
                    name_ar : 10
                }
            },
            filters         : {
                search  : 'search'
            },
            data_events     : {
                'change:selected'   : function () {
                    uijet.Resource('Contexts').fetch({
                        data: {
                            entities: this.resource.where({ selected : true }).map(function (model) {
                                return model.id;
                            }).toString()
                        },
                        remove  : false
                    });
                }
            },
            signals         : {
                pre_wake        : function () {
                    return ! this.has_content;
                },
                pre_update      : 'spin',
                post_fetch_data : function () {
                    this.spinOff()
                        .index().search_index.add( this.resource.toJSON() );
                },
                post_render     : function () {
                    this.$children = this.$element.children();
                    if ( this.queued_filters ) {
                        this.publish('rendered');
                        setImmediate(this.filterChildren.bind(this));
                    }
                },
                pre_select      : function ($selected) {
                    var id = $selected.attr('data-id');
                    this.resource.get(id).set('selected', true);
                    return id;
                },
                post_filtered   : function (ids) {
                    var search_term = this.last_search_term;
                    uijet.utils.requestAnimFrame( function () {
                        var resource = this.resource,
                            highlight = this.highlight.bind(this);
                        if ( this.$last_filter_result ) {
                            this.$last_filter_result.each(function (i, item) {
                                var text = resource.get(item.getAttribute('data-id')).get('name');
                                if ( search_term ) {
                                    item.innerHTML = highlight(text, search_term);
                                }
                                else {
                                    item.innerHTML = '';
                                    item.appendChild(document.createTextNode(text));
                                }
                            });
                        }
                    }.bind(this) );
                }
            },
            app_events      : {
                'entity_field.changed'  : function (value) {
                    this.last_search_term = value || null;
                    this.filterBySearch(this.last_search_term);
                    if ( ! this.queued_filters ) {
                        this.filterChildren();
                        uijet.utils.requestAnimFrame(this.scroll.bind(this));
                    }
                }
            }
        }
    };

});
