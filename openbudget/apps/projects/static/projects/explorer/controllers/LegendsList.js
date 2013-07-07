define([
    'uijet_dir/uijet',
    'explorer'
], function (uijet, explorer) {

    uijet.Adapter('LegendsList', {
        createItemModel : function (state) {
            var model = new explorer.LegendItemModel(state || {
                title       : gettext('Insert title'),
                muni        : '',
                nodes       : []
            });
            this.resource.add(model);
            return model;
        },
        createItem      : function (model_index) {
            var index = this.resource.length,
                state = typeof model_index == 'number' ? this.resource.at(model_index).attributes : model_index,
                model = this.createItemModel(state);

            uijet.start({
                factory : 'LegendItem',
                config  : {
                    element : uijet.$('<li>', {
                        id          : this.id + '_item_' + model.cid
                    }).appendTo(this.$element),
                    resource: model,
                    index   : index,
                    signals : {
                        post_full_render: '-legend_item_added'
                    },
                    color   : this.resource.colors[index * 2]
                }
            }, true);
            return this;
        },
        addItem         : function (model_index) {
            this.createItem(model_index)
                .selectItem(this.resource.length - 1);
            return this;
        },
        setEntity       : function (id) {
            this.resource.at(this.current_index).set({
                muni: uijet.Resource('Munis').get(id)
            });
            return this;
        },
        selectItem      : function (index) {
            var model, muni;
            if ( index !== this.current_index ) {
                model = this.resource.at(index);
                muni = model.get('muni');
                this.current_index = index;
                if ( muni ) {
                    this.updateState(model, muni);
                }
            }
        },
        updateState     : function (model, muni) {
            if ( ! model ) {
                model = this.resource.at(this.current_index);
            }
            if ( ! muni ) {
                muni = model.get('muni');
            }
            this.publish('change_state', {
                entity_id   : muni.get('id'),
                selection   : model.get('state')
            });
        },
        deleteItem      : function (index) {
            var is_current_index = index === this.current_index,
                new_length;
            this.resource.remove(this.resource.at(index));
            // if the user is currently viewing the item s/he's deleting
            if ( is_current_index ) {
                new_length = this.resource.length;
                // if we still have other legend items left
                // and it was the last item in the list
                if ( new_length && new_length === index ) {
                    index--;
                }
            }
            // if current selected item is below the deleted one then need to shift the index by 1
            else if ( index < this.current_index ) {
                this.current_index--;
            }
        },
        removeItem      : function (index) {
            this.deleteItem(index);
            if ( this.resource.length ) {
                if ( this.picking ) {
                    uijet.publish('legends_list.selected', this.current_index);
                }
            }
            else {
                uijet.publish('welcome');
            }
            this.scroll();
        },
        updateSelection : function (data) {
            if ( data && data.reset ) return;
            var resource = uijet.Resource('LatestSheet'),
                selected_nodes = resource.where({ selected : 'selected' }),
                selected_nodes_ids = selected_nodes.map(uijet.Utils.prop('id')),
                partial_nodes = resource.where({ selected : 'partial' })
                                        .map(uijet.Utils.prop('id'));
            this.resource.at(this.current_index).set({
                nodes   : selected_nodes.filter(function (node) {
                    return !~ selected_nodes_ids.indexOf(node.get('parent'));
                }).map(uijet.Utils.prop('id')),
                state   : {
                    selected: selected_nodes_ids,
                    partial : partial_nodes
                }
            });
        }
    });

});
