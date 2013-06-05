define([
    'uijet_dir/uijet',
    'composites/DropmenuButton'
], function (uijet) {

    uijet.Widget('Breadcrumbs', {
        init        : function () {
            var res = this._super.apply(this, arguments),
                history_menu_events = {};

            this.crumbs = [];
            this._wrap();

            this.$main_crumb = this.$element.find('#node_breadcrumb_main');

            history_menu_events[this.id + '.updated'] = function (crumbs) {
                if ( crumbs.length > 1 ) {
                    this.wake(crumbs);
                }
                else {
                    this.sleep();
                }
            };
            history_menu_events[this.id + '_history_menu.cleared'] = 'sleep';

            uijet.start({
                type    : 'DropmenuButton',
                config  : {
                    element         : uijet.$('<span>', {
                        id  : this.id + '_history',
                        text: '...'
                    }).prependTo(this.$wrapper),
                    container       : this.id,
                    dont_wake       : true,
                    wrapper_class   : 'hide',
                    menu            : {
                        mixins  : ['Templated'],
                        signals : {
                            post_select     : function ($selected) {
                                var id = +$selected.attr('data-id'),
                                    i = 0;
                                if ( id ) {
                                    //! Array.prototype.some
                                    this.context.some(function (crumb) {
                                        if ( crumb.id == id ) {
                                            return true
                                        }
                                        i++;
                                    });
                                }
                                this.context.length = i;
                                if ( ! i ) {
                                    this.publish('cleared');
                                }
                            }
                        }
                    },
                    signals         : {
                        pre_appear      : function () {
                            this.$wrapper.removeClass('hide');
                        },
                        post_disappear  : function () {
                            this.$wrapper.addClass('hide');
                        }
                    },
                    app_events  : history_menu_events
                }
            });

            return res;
        },
        render      : function () {
            this._super();

            switch ( this.crumbs.length ) {
                case 0:
                    this.$main_crumb.removeClass('hide');
                    break;
                case 1:
                    this.$main_crumb.removeClass('hide');
                    this.$last_crumb = uijet.$('<span>', {}).appendTo(this.$element);
                    break;
                default:
                    this.$main_crumb.addClass('hide');
                    break;
            }
            return this.publish('updated', this.crumbs.slice(0, -1));
        },
        setCrumbs   : function (crumbs) {
            this.crumbs = crumbs;
            return this.render();
        }
    }, {
        widgets : 'List'
    });

});
