define([
    'uijet_dir/uijet',
    'ui/nodes'
], function (uijet) {

    var amountTypeChanged = function (model, value) {
            if ( value === this.options.amount_type ) {
                this.activate().disable();
                uijet.publish('amount_type.updated', this.options.amount_type);
            }
            else {
                this.enable().deactivate();
            }
        };

    return [{
        type    : 'Pane',
        config  : {
            element : '#nodes_picker_footer'
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#summarize_budget',
            resource    : 'NodesListState',
            amount_type : 'budget',
            data_events : {
                'change:amount_type': amountTypeChanged
            },
            signals     : {
                pre_click   : function () {
                    if ( ! this.activated ) {
                        this.resource.set('amount_type', 'budget');
                    }
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#summarize_actual',
            resource    : 'NodesListState',
            amount_type : 'actual',
            data_events : {
                'change:amount_type': amountTypeChanged
            },
            signals     : {
                pre_click   : function () {
                    if ( ! this.activated ) {
                        this.resource.set('amount_type', 'actual');
                    }
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#picker_done',
            app_events  : {
                'entities_list.selected'        : 'disable',
                'legends_list.delete'           : 'enable',
                'selected_nodes_count.updated'  : function (count) {
                    count ? this.enable() : this.disable();
                }
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#results_count',
            dont_wake   : true,
            app_events  : {
                'nodes_list.filter_count'   : function (count) {
                    if ( typeof count == 'number' ) {
                        this.$element.text(interpolate(gettext('%(count)s results found'), { count : count }, true));
                        this.wake();
                    }
                },
                'search.changed'            : function (data) {
                    if ( ! data.args[1] && ! data.args[0].get('selected') ) {
                        this.sleep();
                    }
                },
                'selected.changed'          : function (data) {
                    if ( ! data.args[1] && ! data.args[0].get('search') ) {
                        this.sleep();
                    }
                }
            }
        }
    }];
});
