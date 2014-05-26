define([
    'uijet_dir/uijet',
    'composites/Select'
], function (uijet) {

    uijet.Factory('ChartPeriodSelect', {
        type    : 'Select',
        config  : {
            wrapper_class   : 'chart_period_select',
            menu            : {
                mixins          : ['Templated'],
                template_name   : 'chart_period_select',
                signals         : {
                    post_wake   : 'opened',
                    post_sleep  : 'closed',
                    pre_wake    : function () {
                        return false;
                    }
                }
            }
        }
    });

    return [{
        factory : 'ChartPeriodSelect',
        config  : {
            element     : '#chart_period_start',
            menu        : {
                signals     : {
                    rendered    : function () {
                        var period_start = uijet.Resource('NodesListState').get('period_start');
                        this.floatPosition('top: -' + this.$wrapper[0].offsetHeight + 'px;');
                        this.setSelected(this.$element.find(
                            period_start ?
                                '[data-period="' + period_start + '"]' :
                                ':first-child'
                        ));
                        this.publish('rendered', this.$selected);
                    },
                    post_select : function ($selected) {
                        uijet.Resource('NodesListState').set('period_start', $selected.text());
                    }
                },
                app_events  : {
                    'chart.fetched' : function (collection) {
                        var periods = collection.periods().slice(0, -1);
                        this.setContext({
                            periods         : periods, 
                            periods_cache   : periods 
                        })
                        .render()
                            .then(this.notify.bind(this, 'rendered'));
                    },
                    'chart_period_end.selected' : function ($selected) {
                        var context = this.getContext();
                        if ( context.periods ) {
                            //TODO: assuming text is a number representing a year
                            var end_period = +$selected.text();
                            context.periods = context.periods_cache.filter(function (period) {
                                return period < end_period;
                            });
                            this.render()
                                .then(this.notify.bind(this, 'rendered'));
                        }
                    }
                }
            },
            app_events  : {
                'chart_period_start_menu.rendered'  : function ($selected) {
                    this.options.content.text($selected.text());
                    this.wake();
                },
                'chart_period_start_menu.opened'    : function () {
                    this.$wrapper.addClass('opened');
                },
                'chart_period_start_menu.closed'    : function () {
                    this.$wrapper.removeClass('opened');
                }
            }
        }
    }, {
        factory : 'ChartPeriodSelect',
        config  : {
            element     : '#chart_period_end',
            menu        : {
                signals     : {
                    rendered    : function () {
                        var period_end = uijet.Resource('NodesListState').get('period_end');
                        this.floatPosition('top: -' + this.$wrapper[0].offsetHeight + 'px;');
                        this.setSelected(this.$element.find(
                            period_end ?
                                '[data-period="' + period_end + '"]' :
                                ':last-child'
                        ));
                        this.publish('rendered', this.$selected);
                    },
                    post_select : function ($selected) {
                        uijet.Resource('NodesListState').set('period_end', $selected.text());
                    }
                },
                app_events  : {
                    'chart.fetched'                 : function (collection) {
                        var periods = collection.periods().slice(1);
                        this.setContext({
                            periods         : periods, 
                            periods_cache   : periods 
                        })
                        .render()
                            .then(this.notify.bind(this, 'rendered'));
                    },
                    'chart_period_start.selected'   : function ($selected) {
                        var context = this.getContext();
                        if ( context.periods ) {
                            //TODO: assuming text is a number representing a year
                            var start_period = +$selected.text();
                            context.periods = context.periods_cache.filter(function (period) {
                                return period > start_period;
                            });
                            this.render()
                                .then(this.notify.bind(this, 'rendered'));
                        }
                    }
                }
            },
            app_events  : {
                'chart_period_end_menu.rendered': function ($selected) {
                    this.options.content.text($selected.text());
                    this.wake();
                },
                'chart_period_end_menu.opened'  : function () {
                    this.$wrapper.addClass('opened');
                },      
                'chart_period_end_menu.closed'  : function () {
                    this.$wrapper.removeClass('opened');
                }
            }
        }
    }];
});
