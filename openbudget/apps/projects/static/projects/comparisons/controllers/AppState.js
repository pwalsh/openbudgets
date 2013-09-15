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
                    this.router.navigate(state_model.get('uuid'));
                }.bind(this),
                error   : function () {
                    uijet.publish('state_save_failed');
                    console.error.apply(console, arguments);
                }
            });
        },
        clearState      : function () {
            uijet.Resource('TimeSeries').reset();
            uijet.Resource('LegendItems').reset();
            uijet.Resource('ProjectState').set(default_state);
            uijet.publish('state_cleared');
            this.router.navigate('');
        },
        duplicateState  : function () {
            var state_clone = uijet.Resource('ProjectState').clone(),
                user = uijet.Resource('LoggedinUser');
            state_clone
                .unset('uuid')
                .unset('id')
                .unset('url')
                .set({
                    author      : user.get('uuid'),
                    author_model: user
                });
            return this._saveState(state_clone);
        },
        saveState       : function () {
            var state = uijet.Resource('ProjectState'),
                user_uuid = uijet.Resource('LoggedinUser').get('uuid');
            if ( user_uuid ) {
                if ( state.get('author') === user_uuid ) {
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
            return uijet.Resource('ProjectState').destroy({
                success : function () {
                    this.clearState();
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
