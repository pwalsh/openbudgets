define(['uijet_dir/uijet'], function (uijet) {

    return {
        _getChartState  : function () {
            var chart_data = uijet.Resource('TimeSeries').toJSON(),
                legend = uijet.Resource('LegendItems');
    
            chart_data.forEach(function (series) {
                var item = legend.get(series.id).attributes;
                series.title = item.title;
                series.state = item.state;
            });
            return chart_data;
        },
        _saveState      : function (state_model) {
            var nodes_list_state = uijet.Resource('NodesListState');
            return state_model.save({ config : {
                chart       : this._getChartState(),
                title       : state_model.get('title'),
                description : state_model.get('description'),
                normalize_by: nodes_list_state.get('normalize_by')
            } }, {
                success : function () {
                    uijet.publish('state_saved');
                    this.router.navigate(state_model.get('id'));
                }.bind(this),
                error   : function () {
                    uijet.publish('state_save_failed');
                    console.error.apply(console, arguments);
                }
            });
        },
        clearState      : function (deleted) {
            uijet.Resource('TimeSeries').reset();
            uijet.Resource('LegendItems').reset();
            uijet.Resource('ToolState').set(this.default_state);
            uijet.publish('state_cleared');
            this.router.navigate('', deleted && { replace : true });
        },
        duplicateState  : function () {
            var state_clone = uijet.Resource('ToolState').clone(),
                user = uijet.Resource('LoggedinUser');
            state_clone
                .unset('id')
                .unset('url')
                .set({
                    author      : user.get('id'),
                    author_model: user
                });
            return this._saveState(state_clone);
        },
        saveState       : function () {
            var state = uijet.Resource('ToolState'),
                user_id = uijet.Resource('LoggedinUser').get('uuid');
            if ( user_id ) {
                if ( state.get('author') === user_id ) {
                    return this._saveState(state);
                }
                else {
                    return this.duplicateState();
                }
            }
            else {
                return uijet.publish('login')
                    .Promise()
                        .reject('User not logged in')
                        .promise();
            }
        },
        deleteState     : function () {
            //TODO: check (again) if logged in user is really the state author
            return uijet.Resource('ToolState').destroy({
                success : function () {
                    this.clearState(true);
                }.bind(this),
                error   : function () {
                    uijet.publish('state_delete_failed');
                    console.error.apply(console, arguments);
                }
            });
        } 
    };
}
);
