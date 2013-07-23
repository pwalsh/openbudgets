define([
    'uijet_dir/uijet',
    'project_widgets/TimelineChart',
    'project_widgets/Select',
    'controllers/TimelineChart'
], function (uijet) {

    function updateAuthorName () {
        var name = uijet.Resource('Author').name();
        ! this.context && (this.context = {});
        this.context.author_name = name;
    }

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
                wrapper_class   : 'chart_period_select_wrapper',
                signals         : {
                    pre_wake    : function () {
                        return false;
                    }
                },
                app_events      : {
                    'chart.fetched' : function (collection) {
                        var periods = collection.periods();
                        this.setData({
                            periods         : periods, 
                            periods_cache   : periods 
                        })
                        .render();
                    }
                }
            }
        }
    });

    return [{
        type    : 'Pane',
        config  : {
            element         : '#chart_section',
            mixins          : ['Transitioned', 'Layered'],
            dont_wake       : true,
            animation_type  : 'fade',
            app_events      : {
                'picker_done.clicked'       : 'wake',
                'add_legend_cancel.clicked' : function () {
                    var has_legend_items = uijet.Resource('LegendItems').length;
                    if ( has_legend_items ) {
                        this.wake();
                    }
                    else {
                        uijet.publish('welcome');
                    }
                },
                'chart_reset'               : 'wake+'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#viz_new'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#viz_duplicate'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#viz_delete'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#viz_export'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#viz_publish'
        }
    }, {
        type    : 'Button',
        config  : {
            element         : '#viz_save',
            adapters        : ['Spin'],
            spinner_options : {
                lines   : 10,
                length  : 8,
                radius  : 6,
                width   : 4
            },
            signals         : {
                pre_click   : 'spin'
            },
            app_events      : {
                state_saved : 'spinOff'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#chart_heading',
            mixins      : ['Templated'],
            resource    : 'ProjectState',
            data_events : {
                'change:title'  : 'title_changed'
            },
            signals     : {
                post_init   : function () {
                    var author_model = uijet.Resource('Author');
                    author_model.on('change', function () {
                        updateAuthorName.call(this);
                        if ( this.has_content ) {
                            uijet.$('#state_author_name').text(this.context.author_name);
                        }
                    }.bind(this));
                },
                pre_wake    : function () {
                    updateAuthorName.call(this);
                    return ! this.has_content;
                },
                post_render : function () {
                    uijet.start({
                        type    : 'ContentEditable',
                        config  : {
                            element     : '#chart_heading h1',
                            id          : this.id + '_title',
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
            data_events : {
                reset   : function (collection) {
                    uijet.publish('chart_reset', {
                        state_loaded: collection.length
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
                    post_render : function () {
                        this.floatPosition('top: -' + this.$wrapper[0].offsetHeight + 'px;');
                        if ( this.silent_render ) {
                            this.setSelected(this.$element.find(':first-child'));
                            this.silent_render = false;
                        }
                        else {
                            this.select(':first-child');
                        }
                        this.publish('rendered');
                    }
                },
                app_events  : {
                    'chart_period_end.selected' : function ($selected) {
                        if ( this.has_data ) {
                            //TODO: assuming text is a number representing a year
                            var end_period = +$selected.text();
                            this.data.periods = this.data.periods_cache.filter(function (period) {
                                return period <= end_period;
                            });
                            this.silent_render = true;
                            this.render();
                        }
                    }
                }
            },
            app_events  : {
                'chart_period_start_menu.rendered'  : 'wake'
            }
        }
    }, {
        factory : 'ChartPeriodSelect',
        config  : {
            element     : '#chart_period_end',
            menu        : {
                signals     : {
                    post_render : function () {
                        this.floatPosition('top: -' + this.$wrapper[0].offsetHeight + 'px;');
                        if ( this.silent_render ) {
                            this.setSelected(this.$element.find(':last-child'));
                            this.silent_render = false;
                        }
                        else {
                            this.select(':last-child');
                        }
                        this.publish('rendered');
                    }
                },
                app_events  : {
                    'chart_period_start.selected'   : function ($selected) {
                        if ( this.has_data ) {
                            //TODO: assuming text is a number representing a year
                            var start_period = +$selected.text();
                            this.data.periods = this.data.periods_cache.filter(function (period) {
                                return period >= start_period;
                            });
                            this.silent_render = true;
                            this.render();
                        }
                    }
                }
            },
            app_events  : {
                'chart_period_end_menu.rendered': 'wake'
            }
        }
    }];

});
