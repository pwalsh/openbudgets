define([
    'uijet_dir/uijet',
    'composites/Select',
    'project_widgets/TimelineChart',
    'controllers/TimelineChart'
], function (uijet) {

    function initPeriodsSelectedHandler () {
        if ( this.period_selectors_started ) {
            this.hoverOn();
        }
        else {
            this.period_selectors_started = true;
        }
    }

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
        type    : 'Pane',
        config  : {
            element     : '#chart_heading',
            mixins      : ['Templated', 'Translated'],
            resource    : 'ProjectState',
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
                                name: 'title'
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
    }, {
        type    : 'TimelineChart',
        config  : {
            element     : '#chart',
            adapters    : ['TimelineChart'],
            resource    : 'TimeSeries',
            style       : {
                padding : '20px 20px 0'
            },
            signals     : {
                post_init   : function () {
                    this.listenTo(uijet.Resource('NodesListState'), 'change:normalize_by', function (model) {
                        if ( 'normalize_by' in model.changed ) {
                            uijet.Resource('Contexts')
                                .fetch()
                                .then(
                                    this.render.bind(this),
                                    function (err) {
                                        console.error(err);
                                        this.render();
                                    }.bind(this)
                                );
                        }
                    }.bind(this));
                },
                fetched     : function () {
                    var periods = this.resource.periods();
                    this.timeContext(String(periods[0]), String(periods[periods.length - 1]));
                }
            },
            data_events : {
                reset   : function (collection) {
                    collection.length && uijet.publish('chart_reset', {
                        state_loaded: true
                    });
                }
            },
            app_events  : {
                'legends_list.delete'               : function () {
                    if ( this.awake && uijet.Resource('LegendItems').length ) {
                        this.render();
                    }
                },
                'legend_item_title.updated'         : 'setTitle+',
                'chart_period_start_menu.rendered'  : initPeriodsSelectedHandler,
                'chart_period_end_menu.rendered'    : initPeriodsSelectedHandler,
                'chart_period_start.selected'       : function ($selected) {
                    this.timeContext($selected.text());
                },
                'chart_period_end.selected'         : function ($selected) {
                    this.timeContext(null, $selected.text());
                }
            }
        }
    }, {
        factory : 'ChartPeriodSelect',
        config  : {
            element     : '#chart_period_start',
            menu        : {
                signals     : {
                    rendered: function () {
                        this.floatPosition('top: -' + this.$wrapper[0].offsetHeight + 'px;');
                        this.setSelected(this.$element.find(':first-child'));
                        this.publish('rendered', this.$selected);
                    }
                },
                app_events  : {
                    'chart.fetched' : function (collection) {
                        var periods = collection.periods().slice(0, -1);
                        this.setData({
                            periods         : periods, 
                            periods_cache   : periods 
                        })
                        .render()
                            .then(this.notify.bind(this, 'rendered'));
                    },
                    'chart_period_end.selected' : function ($selected) {
                        if ( this.has_data ) {
                            //TODO: assuming text is a number representing a year
                            var end_period = +$selected.text();
                            this.data.periods = this.data.periods_cache.filter(function (period) {
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
                    rendered: function () {
                        this.floatPosition('top: -' + this.$wrapper[0].offsetHeight + 'px;');
                        this.setSelected(this.$element.find(':last-child'));
                        this.publish('rendered', this.$selected);
                    }
                },
                app_events  : {
                    'chart.fetched'                 : function (collection) {
                        var periods = collection.periods().slice(1);
                        this.setData({
                            periods         : periods, 
                            periods_cache   : periods 
                        })
                        .render()
                            .then(this.notify.bind(this, 'rendered'));
                    },
                    'chart_period_start.selected'   : function ($selected) {
                        if ( this.has_data ) {
                            //TODO: assuming text is a number representing a year
                            var start_period = +$selected.text();
                            this.data.periods = this.data.periods_cache.filter(function (period) {
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
