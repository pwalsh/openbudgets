define([
    'uijet_dir/uijet',
    'composites/DropmenuButton'
], function (uijet) {

    var BREADCRUMB_CLASS = 'node_breadcrumb';

    uijet.Widget('Breadcrumbs', {
        //TODO: the type_class still gets messed up if not specified - need to fix inside uijet
        init        : function () {
            var res = this._super.apply(this, arguments);

            this._wrap();

            uijet.start([{
                type    : 'Button',
                config  : {
                    element     : '#node_breadcrumb_main',
                    container   : this.id,
                    dont_wake   : true,
                    disabled    : true,
                    signals     : {
                        pre_appear      : function () {
                            this.$element.removeClass('hide');
                        },
                        post_disappear  : function () {
                            this.$element.addClass('hide');
                        }
                    },
                    app_events  : {
                        'nodes_breadcrumbs.hide_root'   : 'sleep',
                        'nodes_breadcrumbs.enable_root' : function () {
                            this.wake();
                            this.enable();
                        },
                        'nodes_breadcrumbs.disable_root': function () {
                            this.wake();
                            this.disable();
                        }
                    }
                }
            }, {
                type    : 'Button',
                config  : {
                    element     : '#node_breadcrumb_back',
                    container   : this.id,
                    dont_wake   : true,
                    signals     : {
                        pre_wake        : function () {
                            this.$element.text(this.context.name);
                        },
                        pre_appear      : function () {
                            this.$element.removeClass('hide');
                        },
                        post_disappear  : function () {
                            this.$element.addClass('hide');
                        }
                    },
                    app_events  : {
                        'nodes_breadcrumbs.hide_back'   : 'sleep',
                        'nodes_breadcrumbs.set_back'    : 'wake+'
                    }
                }
            }, {
                type    : 'DropmenuButton',
                config  : {
                    element         : '#nodes_breadcrumbs_history',
                    container       : this.id,
                    dont_wake       : true,
                    wrapper_class   : 'hide',
                    menu            : {
                        mixins          : ['Templated'],
                        float_position  : 'top: 2rem',
                        signals         : {
                            pre_select  : function ($selected) {
                                var id = +$selected.attr('data-id'),
                                    i = 0;
                                if ( id ) {
                                    //! Array.prototype.some
                                    this.context.some(function (crumb) {
                                        if ( crumb.id == id ) {
                                            return true;
                                        }
                                        i++;
                                    });
                                }
                                this.context.length = i;
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
                    app_events  : {
                        'nodes_breadcrumbs.updated' : function (crumbs) {
                            if ( crumbs && crumbs.length ) {
                                this.wake(crumbs);
                            }
                            else {
                                this.sleep();
                            }
                        }
                    }
                }
            }]);

            this.subscribe('node_breadcrumb_main.clicked', function () {
                this.resource.reset([]);
            });
            this.subscribe('node_breadcrumb_back.clicked', function (data) {
                var id = data.context.id,
                    models = [];
                if ( id ) {
                    //! Array.prototype.some
                    this.resource.models.some(function (model) {
                        models.push(model);
                        if ( model.id === id ) {
                            return true;
                        }
                    });
                }
                this.resource.reset(models);
            });
            this.subscribe('nodes_breadcrumbs_history_menu.selected', function ($selected) {
                var node_id = +$selected.attr('data-id');
                this.resource.reset(
                    uijet.Resource('LatestSheet').branch(node_id)
                );
            });

            return res;
        },
        render      : function () {
            var length = this.resource.length,
                history;
            this._super();

            switch ( length ) {
                case 0:
                    this.publish('disable_root')
                        .publish('hide_back');
                    break;
                case 1:
                    this.publish('enable_root')
                        .publish('hide_back');
                    break;
                case 2:
                    this.publish('enable_root')
                        .publish('set_back', this.resource.at(length - 2).attributes);
                    break;
                default:
                    this.publish('hide_root')
                        .publish('set_back', this.resource.at(length - 2).attributes);
                    break;
            }
            if ( length ) {
                history = this.resource.slice(0, -2).map(uijet.utils.prop('attributes'));
            }
            this.publish('updated', history);
            return this;
        }
    });

});
