define([
    'uijet_dir/uijet',
    //'composites/Modal'
], function (uijet) {
    uijet.Factory('ShareDialog', {
        type: 'Pane',
        config: {
            dont_wake: true,
            app_events: {
                'chart_share_tabs.selected': function ($selected) {
                    if (this.options.sharer_type === $selected.data('value')) {
                        this.wake();
                    }
                    else {
                        this.sleep();
                    }
                }
            }
        }
    });

    return [{
        type: 'Pane',
        config: {
            element: '#chart_share_dialog',
            dont_wake: true,
            signals: {
                post_wake: function () {
                    this.$element.addClass('awake');
                },
                pre_sleep: function () {
                    this.$element.removeClass('awake');
                }
            },
            app_events: {
                'viz_publish.clicked': function () {
                    this.wake();
                }
            }
        }
    }, {
        type: 'List',
        config: {
            element: '#chart_share_tabs',
            initial: ':first-child',
            signals: {
                post_wake: function () {
                    this.publish('selected', this.$selected);
                }
            }
        }
    }, {
        factory: 'ShareDialog',
        config: {
            element: '#chart_share_fb',
            sharer_type: 'fb',
            signals: {
                post_init: function () {
                    this.loaded_src = null;
                },
                post_wake: function () {
                    var url         = document.location.href,
                        iframe      = document.createElement('iframe'),
                        iframe_src  = '//www.facebook.com/sharer/sharer.php?u=' + url;

                    if (this.loaded_src !== iframe_src) {
                        iframe.src = iframe_src;
                        this.$element.html(iframe);
                        this.loaded_src = iframe_src;
                    }
                }
            }
        }
    }];
});
