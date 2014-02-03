define([
    'uijet_dir/uijet',
    'composites/DropmenuButton'
], function (uijet) {

    return {
        type    : 'DropmenuButton',
        config  : {
            element         : '#search_filter',
            click_event     : 'mouseenter',
            wrapper_class   : 'nodes_header_menu_button',
            dom_events      : {
                click       : function () {
                    this.sleep();
                    uijet.publish('search_filter_menu.selected', {
                        type: 'search'
                    });
                }
            },
            signals         : {
                post_init   : function () {
                    this.$wrapper.on('mouseleave', this.publish.bind(this, 'mouse_left'));
                }
            },
            menu            : {
                mixins          : ['Templated', 'Translated'],
                float_position  : 'top: 66px',
                dom_events      : {
                    mouseleave  : function () {
                        this.mouse_over = false;
                        this.sleep();
                    },
                    mouseenter  : function (e) {
                        this.mouse_over = true;
                    }
                },
                signals         : {
                    post_init   : function () {
                        this.prev_search_terms = [];
                    },
                    pre_wake    : function () {
                        this.context || (this.context = {});
                        this.context.prev_search_terms = this.prev_search_terms;
                    },
                    pre_select  : function ($selected) {
                        var type = $selected.attr('data-type'),
                            value;
                        if ( type === 'search' ) {
                            if ( $selected.attr('data-old') ) {
                                value = $selected.text();
                            }
                        }
                        return {
                            type    : type,
                            value   : value
                        };
                    },
                    post_select : 'sleep'
                },
                app_events      : {
                    'search_filter.mouse_left'  : function () {
                        this.mouse_over || this.sleep();
                    },
                    'nodes_search.entered'      : function (query) {
                        if ( query ) {
                            var index = this.prev_search_terms.indexOf(query);
                            if ( ~ index ) {
                                this.prev_search_terms.splice(index, 1);
                            }
                            this.prev_search_terms.unshift(query);
                        }
                    }
                }
            },
            app_events      : {
                'nodes_search.entered'          : 'wake',
                'nodes_search.cancelled'        : 'wake',
                'search_filter_menu.selected'   : 'sleep'
            }
        }
    };

});
