define([
    'uijet_dir/uijet',
    'explorer'
], function (uijet, Explorer) {

    uijet.Adapter('LegendsList', {
        createItemModel : function () {
            var model = new Explorer.LegendItemModel({
                title       : 'Title me',
                description : 'Describe me',
                muni        : '',
                nodes       : []
            });
            this.current_index = this.resource.add(model).length - 1;
            return model;
        },
        setEntity       : function (id) {
            this.resource.at(this.current_index).set({
                muni: uijet.Resource('Munis').get(id)
            });
        },
        selectItem      : function (index) {
            var model;
            if ( index !== this.current_index ) {
                model = this.resource.at(index);
                this.current_index = index;
                this.publish('change_state', {
                    entity_id   : model.get('muni').get('id'),
                    selection   : model.get('state')
                });
            }
        },
        deleteItem      : function (index) {
            this.resource.remove(this.resource.at(index));
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
