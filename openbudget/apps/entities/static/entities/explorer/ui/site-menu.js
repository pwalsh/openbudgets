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
                    this.anim_key = uijet.utils.getStyleProperty('transform');

                    this.anim_props = {};
                    this.header_anim_props = {};
                        
                    this.header_anim_props = 'right:' + this.$element[0].offsetWidth + 'px';
                    this.anim_props[this.anim_key] = 'translateX(-276px)';

                    this.$header = uijet.$('#sheet_header_top_container');
                    this.header_anim_callback = function () {
                        this.$header.removeClass('transitioned');
                        uijet.publish('sheet_header_moved');
                    }.bind(this);
                }
            },
            app_events  : {
                open_comments   : function () {
                    uijet.animate(this.$header, this.header_anim_props, this.header_anim_callback);
                    uijet.animate(this.$element, this.anim_props);
                },
                close_comments  : function () {
                    var props = {};
                    props[this.anim_key] = 'translateX(0px)';
                    uijet.animate(this.$header, 'right:0px', this.header_anim_callback);
                    uijet.animate(this.$element, props);
                }
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element         : '#panel-nav',
            mixins          : ['Transitioned'],
            dont_wake       : true,
            animation_type  : 'slide',
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
