define([
    'uijet_dir/uijet',
    'tool_widgets/TimelineChart',
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

    return {
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
    };

});
