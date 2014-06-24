define([
    'uijet_dir/uijet'
], function (uijet) {

    return [{
        type    : 'Button',
        config  : {
            element     : '#right_edge_detector',
            click_event : 'mouseover'
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#site_menu_open',
            click_event : 'mouseover',
            signals     : {
                post_init   : function () {
                    // use right since transforms cause the header's layer to lose its proper z-index
                    this.header_anim_props = { right: this.$element[0].offsetWidth };
                    this.anim_props = { translateX: -276 };

                    this.$header = uijet.$('#sheet_header_top_container');
                    this.header_anim_callback = function () {
                        uijet.publish('sheet_header_moved');
                    }.bind(this);

                    this.anim_options = { duration: 200, easing: 'ease-in' };
                }
            },
            app_events  : {
                open_comments   : function () {
                    uijet.animate(this.$header, this.header_anim_props, this.anim_options, this.header_anim_callback);
                    uijet.animate(this.$element, this.anim_props, this.anim_options);
                },
                close_comments  : function () {
                    uijet.animate(this.$header, { right : 0 }, this.anim_options, this.header_anim_callback);
                    uijet.animate(this.$element, { translateX: 0 }, this.anim_options);
                }
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element         : '#panel-nav',
            mixins          : ['Transitioned'],
            dont_wake       : true,
            animation_type  : {
                properties  : {
                    translateX: '-300'
                },
                options     : {
                    duration: 100,
                    easing  : 'ease-in'
                }
            },
            dom_events      : {
                mouseleave  : 'sleep'
            },
            app_events      : {
                'site_menu_open.clicked'        : 'wake',
                'right_edge_detector.clicked'   : 'wake',
                'panel-nav-close.clicked'       : 'sleep'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#panel-nav-close'
        }
    }];

});
