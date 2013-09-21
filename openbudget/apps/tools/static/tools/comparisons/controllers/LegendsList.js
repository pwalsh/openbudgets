define([
    'uijet_dir/uijet',
    'comparisons'
], function (uijet, comparisons) {

    uijet.Adapter('LegendsList', {
        createItemModel : function (state, index) {
            var model = new comparisons.LegendItemModel(state || {
                title       : '',
                placeholder : gettext('Insert title'),
                muni        : '',
                nodes       : [],
                amount_type : 'budget',
                color       : this.resource.colors.shift()
            });
            // make sure color is unique
            if ( state ) {
                model.set('color', this.resource.colors.shift());
            }
            this.resource.add(model, { at : index });
            return model;
        },
        createItemWidget: function (model, index) {
            var $el = uijet.$('<li>', {
                id  : this.id + '_item_' + model.id
            });
            if ( index ) {
                $el.insertAfter(this.$element.children().eq(index - 1));
            }
            else {
                $el.prependTo(this.$element);
            }
            uijet.start({
                factory : 'LegendItem',
                config  : {
                    element : $el,
                    resource: model,
                    index   : index,
                    signals : {
                        post_full_render: '-legend_item_added',
                        pre_destroy     : '-legend_item_removed'
                    },
                    picking : this.picking
                }
            }, true);
            return this;
        },
        createItem      : function (use_model) {
            var state = use_model ? use_model.attributes : null,
                new_index = use_model ? this.resource.indexOf(use_model) + 1 : 0,
                model;

            // make sure id is removed
            delete state.id;

            model = this.createItemModel(state, new_index);
            this.createItemWidget(model, new_index);

            return model;
        },
        addItem         : function (use_model) {
            this.picking = true;
            return this.selectItem( this.createItem(use_model) );
        },
        setEntity       : function (id) {
            this.current_model.set({
                muni: uijet.Resource('Munis').get(id)
            });
            return this;
        },
        selectItem      : function (model) {
            var muni;
            if ( model !== this.current_model ) {
                this.resource.where({
                    disabled: false
                }).forEach(function (m) {
                    m.set('disabled', true);
                });
                model.set('disabled', false);
                muni = model.get('muni');
                this.current_model = model;
                if ( muni ) {
                    this.updateState(model, muni);
                }
            }
            return this;
        },
        updateState     : function (model, muni) {
            if ( ! model ) {
                model = this.current_model;
            }
            if ( ! muni ) {
                muni = model.get('muni');
            }
            this.publish('select_state', {
                entity_id   : muni.get('id'),
                selection   : model.get('state'),
                amount_type : model.get('amount_type')
            });
        },
        deleteItem      : function (model) {
            var is_current_model = model === this.current_model,
                new_length;
            this.resource.remove(model);
            // if the user is currently viewing the item s/he's deleting
            if ( is_current_model ) {
                this.current_model = null;
            }
            return this;
        },
        removeItem      : function (model) {
            this.deleteItem(model);
            if ( this.resource.length ) {
                if ( this.picking ) {
                    uijet.publish('picker_done.clicked');
                }
            }
            else {
                uijet.publish('welcome');
            }
            this.sizeAndScroll();
        },
        updateSelection : function (data) {
            if ( data && data.reset ) return;
            //TODO: can optimize since we're already looping LatestSheet in nodes_list widget on selection
            var resource = uijet.Resource('LatestSheet'),
                selected_nodes = resource.where({ selected : 'selected' }),
                selected_nodes_ids = selected_nodes.map(uijet.utils.prop('id')),
                partial_nodes = resource.where({ selected : 'partial' })
                                        .map(uijet.utils.prop('id'));
            this.current_model.set({
                nodes   : selected_nodes.filter(function (node) {
                    return !~ selected_nodes_ids.indexOf(node.get('parent'));
                }).map(uijet.utils.prop('id')),
                state   : {
                    selected: selected_nodes_ids,
                    partial : partial_nodes
                }
            });
        },
        resetItems      : function () {
            this.destroyContained();
            this.resource.models.forEach(this.createItemWidget, this);
            this.createOverlay();
            if ( ! this.resource.length ) {
                uijet.publish('welcome');
            }
            return this;
        },
        createOverlay   : function () {
            var overlay_id = this.id + '_overlay';
            uijet.start({
                factory : 'LegendOverlay',
                config  : {
                    element     : uijet.$('<div>', {
                        id      : overlay_id
                    }).appendTo(this.$wrapper),
                    container   : this.id
                }
            });
            return this;
        },
        sizeAndScroll   : function () {
            var $wrapper = this.$wrapper,
                // -44 for normalization_selector
                max_height = $wrapper[0].offsetParent.offsetHeight - 44,
                el_height = this.$element[0].offsetHeight;
            if ( ! this.picking ) {
                // -44 for add_legend
                max_height -= 44;
            }
            this.$wrapper.css({
                'max-height': max_height + 'px',
                height      : (el_height > max_height ? max_height : el_height) + 'px'
            });
            return this.scroll();
        }
    });

});
