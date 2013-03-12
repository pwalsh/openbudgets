define([
    'uijet_dir/uijet',
    'resources/budget'
], function (uijet) {

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element         : '#heading',
            position        : 'top:50',
            wake_on_startup : true
        }
    }, {
        type    : 'List',
        config  : {
            element         : '#budgets_list',
            mixins          : ['Templated'],
            resource        : 'Budgets',
            wake_on_startup : true,
            position        : 'top:50|50',
            signals         : {
                pre_select  : function ($selected) {
                    return this.resource.get($selected[0].id).toJSON();
                }
            }
        }
    }, {
        type    : 'Table',
        config  : {
            element     : '#spreadsheet',
            head        : {
                columns : ['code', 'name', 'amount', 'description']
            },
            grid        : {
                mixins          : ['Templated'],
                template_name   : 'spreadsheet-grid',
                signals         : {
                    pre_wake    : function () {
                        return false;
                    }
                },
                app_events      : {
                    'budgets_list.selected' : function (data) {
                        var that = this;console.log(data);
                        this.data = data;
                        this.render().then(function () {
                            that.publish('rendered');
                        });
                    }
                }
            },
            position    : 'fluid',
            app_events  : {
                'spreadsheet_grid.rendered' : 'wake'
            }
        }
    }]);

});