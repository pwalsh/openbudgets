define([
    'uijet_dir/uijet',
    'importer/app'
], function (uijet, Importer) {
    return {
        parseDate           : function (date) {
            return [date.getFullYear(), date.getMonth() + 1, date.getDate()].join('-');
        },
        processDivisions    : function (data) {
            //! Array.prototype.filter
            data.results = data.results.filter(function (item, i) {
                return item.has_budgets;
            });
        },
        processEntities     : function (data) {
            //! Array.prototype.filter
            data.results = data.results.filter(function (item, i) {
                return item.division.has_budgets;
            });
        },
        formExtConfigByType : function (type) {
            var config = {
                    template_name   : type + '-form'
                };

            switch ( type ) {
                case 'budgettemplate':
                    config.partials = {
                        divisions   : 'divisions'
                    };
                    config.signals = {
                        post_render : function () {
                            uijet.start({
                                type    : 'DatepickerInput',
                                config  : {
                                    element     : '#period_start',
                                    datepicker  : {
                                        app_events  : {
                                            'period_start_picker.wake'  : 'wake+',
                                            'period_start_picker.sleep' : 'sleep'
                                        }
                                    }
                                }
                            })
                            .then( this.wakeContained.bind(this) );
                        },
                        process_data: this.processDivisions
                    };
                    config.data_url = Importer.BASE_API_URL + 'divisions/';
                    break;
                case 'actual':
                    config.template_name = 'budget-form';
                case 'budget':
                    config.partials = {
                        entities: 'entities'
                    };
                    config.signals = {
                        process_data: this.processEntities,
                        post_render : function () {
                            uijet.start([{
                                type    : 'DatepickerInput',
                                config  : {
                                    element     : '#period_start',
                                    datepicker  : {
                                        app_events  : {
                                            'period_start_picker.wake'  : 'wake+',
                                            'period_end_picker.wake'    : 'sleep',
                                            'period_start_picker.sleep' : 'sleep'
                                        }
                                    }
                                }
                            }, {
                                type    : 'DatepickerInput',
                                config  : {
                                    element     : '#period_end',
                                    datepicker  : {
                                        app_events  : {
                                            'period_end_picker.wake'    : 'wake+',
                                            'period_start_picker.wake'  : 'sleep',
                                            'period_end_picker.sleep'   : 'sleep'
                                        }
                                    }
                                }
                            }])
                            .then( this.wakeContained.bind(this) );
                        }
                    };
                    config.data_url = Importer.BASE_API_URL + 'entities/';
                    break;
            }

            return config;
        }
    };
});
