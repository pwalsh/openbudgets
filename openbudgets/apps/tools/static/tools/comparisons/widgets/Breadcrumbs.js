define([
    'uijet_dir/uijet',
    'composites/DropmenuButton'
], function (uijet) {

    uijet.Widget('Breadcrumbs', {
        options     : {
            type_class  : ['uijet_list', 'uijet_breadcrumbs'],
            signals     : {
                post_render : function () {
                    this.publish('rendered', this.$element.children().slice(2))
                        .checkWrap();
                }
            }
        },
        init        : function () {
            this._super.apply(this, arguments);

            var id = this.id,
                button_id = id + '_button';

            this.fold_index = -1;
            this.children_widths = [];

            uijet.start({
                type    : 'DropmenuButton',
                config  : {
                    element         : '#' + button_id,
                    id              : button_id,
                    container       : id,
                    dont_wake       : true,
                    dont_wrap       : true,
                    extra_class     : 'hide',
                    menu            : {
                        element         : '#' + button_id + '_menu',
                        id              : button_id + '_menu',
                        container       : button_id,
                        float_position  : 'top: 1.3rem',
                        signals         : {
                            post_init       : function () {
                                this.subscribe(id + '.rendered', function ($children) {
                                    if ( this.awake ) {
                                        this.sleep();
                                    }
                                    this.$element
                                        .empty()
                                        .append($children.clone().addClass('hide'));
                                })
                                .subscribe(id + '.fold', function (index) {
                                    this.$element.children().eq(index).removeClass('hide');
                                })
                                .subscribe(id + '.unfold', function (index) {
                                    if ( ~ index )
                                        this.$element.children().eq(index).addClass('hide');
                                });
                            },
                            pre_appear      : 'opening',
                            post_disappear  : 'closing',
                            pre_select      : function ($selected) {
                                return $selected.attr('data-id');
                            },
                            post_select     : '-nodes_breadcrumbs.selected+'
                        }
                    },
                    signals         : {
                        post_init   : function () {
                            this.subscribe(id + '.fold', function () {
                                if ( ! this.awake ) {
                                    this.wake().then(this.publish.bind(this, 'awaken'));
                                }
                            })
                            .subscribe(id + '.unfold', function (index) {
                                if ( ! ~ index )
                                    this.sleep();
                            });
                        },
                        pre_appear      : function () {
                            this.$element.removeClass('hide');
                        },
                        post_disappear  : function () {
                            this.$element.addClass('hide');
                        }
                    }
                }
            });

            this.subscribe('app.resize', this.checkWrap)
                .subscribe(button_id + '.awaken', this.checkWrap)
                .subscribe(button_id + '_menu.opening', this.overflow.bind(this, true))
                .subscribe(button_id + '_menu.closing', this.overflow);

            return this;
        },
        overflow    : function (allow) {
            if ( allow ) {
                this.$element.addClass('overflow');
            }
            else {
                this.$element.removeClass('overflow');
            }
            return this;
        },
        checkWrap   : function () {
            var el = this.$element[0],
                folding = false;

            while ( el.scrollHeight > el.clientHeight ) {
                folding = true;
                if ( ! this.fold() )
                    break;
            }

            if ( ! folding && ~ this.fold_index ) {
                // this is so damn cool!
                while ( this.unfold() ) continue;
            }

            return this;
        },
        fold        : function () {
            var $child;

            this.fold_index++;

            $child = this.$element.children().slice(2).eq(this.fold_index);

            if ( $child.length ) {
                // cache its width so we can later test if it can be unfolded back
                this.children_widths[this.fold_index] = $child[0].offsetWidth;
                // fold
                $child.addClass('hide');
                // inform the drop menu button to reveal this item
                this.publish('fold', this.fold_index);
            }
            else {
                this.fold_index--;
                return false;
            }
            return true;
        },
        unfold      : function () {
            var index = this.fold_index,
                $child, content_width;

            if ( ~ index ) {
                $child = this.$element.children().slice(2).eq(index);
    
                if ( $child.length ) {
                    content_width = Array.prototype.reduce.call(
                        this.$element.children(),
                        function (prev, current) {
                            return prev + current.offsetWidth;
                        },
                        this.children_widths[index]
                    );
                    if ( content_width <= this.$element[0].clientWidth ) {
                        // unfold
                        $child.removeClass('hide');
                        // inform the drop menu button to reveal this item
                        this.publish('unfold', index);
                        this.fold_index--;
                        return true;
                    }
                }
            }
            else {
                this.publish('unfold', index);
            }
            return false;
        }
    }, {
        widgets : ['List']
    });

});
