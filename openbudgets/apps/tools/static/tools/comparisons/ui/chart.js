define([
    'uijet_dir/uijet',
    'd3',
    'composites/Select',
    'tool_widgets/TimelineChart',
    'controllers/TimelineChart'
], function (uijet, d3) {

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
    }, {
        type    : 'TimelineChart',
        config  : {
            element     : '#chart',
            adapters    : ['TimelineChart'],
            resource    : 'TimeSeries',
            chart       : {
                padding : 20  
            },
            style       : {
                padding : '20px 20px 0'
            },
            signals     : {
                post_init   : function () {
                    var that = this;
                    this.listenTo(uijet.Resource('NodesListState'), 'change', function (model) {
                        var changed = model.changed;
                        if ( ! this.context ) {
                            this.context = {};
                        }

                        if ( 'period_start' in changed ) {
                            this.context.period_start = model.get('period_start');
                        }
                        if ( 'period_end' in changed ) {
                            this.context.period_end = model.get('period_end');
                        }

                        if ( 'normalize_by' in changed ) {
                            that.resource.recalcFactors()
                                .then(function () {
                                    that.draw();
                                });
                        }
                    });
                },
                pre_render  : function () {
                    if ( this.context && this.context.state_loaded ) {
                        this._draw();
                        delete this.context.state_loaded;
                    }
                    else {
                        this.set(uijet.Resource('LegendItems').models).then(this._draw.bind(this));
                    }
                }
            },
            data_events : {
                reset   : function (collection) {
                    collection.length && uijet.publish('chart_reset', uijet.utils.extend(this.context || {}, {
                        state_loaded: true
                    }));
                }
            },
            app_events  : {
                'legends_list.delete'               : function () {
                    if ( this.awake && uijet.Resource('LegendItems').length ) {
                        this.render();
                        this._finally();
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
