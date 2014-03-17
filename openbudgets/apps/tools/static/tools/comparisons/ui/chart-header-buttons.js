define([
    'uijet_dir/uijet',
    'composites/DropmenuButton',
    'composites/Select'
], function (uijet) {

    function enableMenuButton () {
        this.spinOff().enable();
    }

    uijet.Factory('ChartMenuButton', {
        type    : 'Button',
        config  : {
            adapters    : ['Spin'],
            dont_wake   : function () {
                return ! uijet.Resource('ToolState').has('id');
            },
            spinner_options : {
                lines   : 10,
                length  : 8,
                radius  : 6,
                width   : 4
            },
            signals         : {
                pre_click   : function () {
                    this.disable().spin();
                }
            },
            app_events      : {
                state_save_failed   : enableMenuButton
            }
        }
    });

    return [{
        type    : 'Button',
        config  : {
            element : '#viz_new'
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#viz_export',
            dont_wake   : function () {
                return ! uijet.Resource('ToolState').has('id');
            },
            app_events  : {
                chart_saved: 'wake'
            }
        }
    }, {
        type    : 'DropmenuButton',
        config  : {
            element     : '#viz_publish',
            dont_wrap   : true,
            dont_wake   : function () {
                return ! uijet.Resource('ToolState').has('id');
            },
            app_events  : {
                chart_saved: 'wake'
            },
            signals         : {
                post_init   : function () {
                    this.$wrapper.on('mouseleave', this.publish.bind(this, 'mouse_left'));
                }
            },
            menu        : {
                element        : '#viz_publish_menu',
                float_position : 'top: 44px',
                signals        : {
                    post_select: function ($selected) {
                        var value = $selected.data('value'),
                            enc = encodeURIComponent,
                            url, popup;

                        switch (value) {
                            case 'facebook':
                                url = 'https://www.facebook.com/sharer/sharer.php?u={url}'.replace('{url}', enc(document.location.href));
                                popup = window.open(url);
                                break;

                            case 'twitter':
                                url = 'https://twitter.com/share?url={url}'.replace('{url}', enc(document.location.href));
                                popup = window.open(url);
                                break;
                        }
                    }
                },
                dom_events     : {
                    mouseleave  : function () {
                        this.mouse_over = false;
                        this.sleep();
                    },
                    mouseenter  : function (e) {
                        this.mouse_over = true;
                    }
                }
            }
        }
    }, {
        factory : 'ChartMenuButton',
        config  : {
            element     : '#viz_delete',
            dont_wake   : function () {
                var state = uijet.Resource('ToolState');
                if ( uijet.Resource('LoggedinUser').get('uuid') === state.get('author') ) {
                    return ! state.has('id');
                }

                return true;
            },
            app_events  : {
                state_cleared       : enableMenuButton,
                state_delete_failed : enableMenuButton,
                chart_saved: 'wake'
            }
        }
    }, {
        factory : 'ChartMenuButton',
        config  : {
            element     : '#viz_duplicate',
            app_events  : {
                state_saved         : enableMenuButton,
                state_save_failed   : enableMenuButton,
                chart_saved         : 'wake'
            }
        }
    }, {
        factory : 'ChartMenuButton',
        config  : {
            element     : '#viz_save',
            dont_wake   : false,
            signals     : {
                pre_click   : function () {
                    if ( ! uijet.Resource('LoggedinUser').has('uuid') ) {
                        uijet.publish('login');
                        return false;
                    }
                    else {
                        this.disable().spin();
                        uijet.publish('chart_saved');
                    }
                }
            },
            app_events  : {
                state_saved : enableMenuButton
            }
        }
    }];
});
