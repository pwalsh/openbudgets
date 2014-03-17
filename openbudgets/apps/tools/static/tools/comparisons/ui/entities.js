define([
    'uijet_dir/uijet',
    'tool_widgets/ClearableTextInput'
], function (uijet) {

    return [{
        type    : 'Pane',
        config  : {
            element         : '#entity_selection',
            dont_wake       : true,
            mixins          : ['Transitioned', 'Layered'],
            animation_type  : 'fade',
            app_events      : {
                'add_legend.clicked'        : 'wake',
                'add_legend_cancel.clicked' : 'sleep',
                'entities_list.selected'    : 'sleep'
            }
        }
    }, {
        type    : 'ClearableTextInput',
        config  : {
            element     : '#entity_field',
            button      : {
                dont_wake   : true,
                signals     : {
                    pre_click   : function () {
                        uijet.publish('entity_field.changed');
                        this.sleep();
                    }
                },
                app_events  : {
                    'entity_field.move_button'  : function (width) {
                        if ( width ) {
                            this.$element[0].style.right = width + 30 + 'px';
                            if ( ! this.awake ) {
                                this.wake();
                            }
                        }
                        else if ( this.awake ) {
                            this.sleep();
                        }
                    }
                }
            },
            dom_events  : {
                keyup   : function (e) {
                    var val = e.target.value,
                        clean = val.trim();
                    this.publish('changed', clean);
                    this.$shadow_text.text(val);
                    this.publish('move_button', val ? this.$shadow_text.width() : 0);
                }
            },
            signals     : {
                post_init   : function () {
                    this.$shadow_text = uijet.$('<span>', {
                        'class' : 'shadow_text'
                    }).prependTo(this.$wrapper);
                },
                post_wake   : function () {
                    var width = this.$shadow_text.width();
                    this.$element.focus();
                    if ( width ) {
                        this.publish('move_button', width);
                    }
                }
            }
        }
    }];

});
