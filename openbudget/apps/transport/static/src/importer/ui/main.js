define([
    'uijet_dir/uijet',
    'importer/app',
    'composites/Datepicker'
], function (uijet, Importer) {

    var FORM_TYPE_EXT_ID = '#import_form_type_ext';

    uijet.Factory('import_form_ext', {
        type    : 'Pane',
        config  : {
            element         : FORM_TYPE_EXT_ID,
            mixins          : ['Templated'],
            template_name   : 'budgettemplate-form',
            partials_dir    : 'partials/'
        }
    });

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element : '#heading',
            position: 'top:50'
        }
    }, {
        type    : 'Pane',
        config  : {
            element : '#form_container',
            position: 'fluid'
        }
    }, {
        type    : 'Form',
        config  : {
            element     : '#import_form',
            signals     : {
                post_init   : function () {
                    var type_ext = this.$element.find(FORM_TYPE_EXT_ID)[0];
                    this.type_ext_html = type_ext.outerHTML;
                    this.type_ext_position = type_ext.nextElementSibling;
                }
            },
            app_events  : {
                'import_form_type.changed'  : function (data) {
                    var value = data.value,
                        config = {
                            template_name   : value + '-form'
                        };

                    switch ( value ) {
                        case 'budgettemplate':
                            config.partials = {
                                divisions   : 'divisions'
                            };
                            config.signals = {
                                post_render : function () {
                                    uijet.start([{
                                        type    : 'Datepicker',
                                        config  : {
                                            element : '#period_start_picker'
                                        }
                                    }])
                                    .then( this.wakeContained.bind(this) );
                                },
                                process_data: function (data) {
                                    //TODO: move this to a controller
                                    //! Array.prototype.filter
                                    data.results = data.results.filter(function (item, i) {
                                        return item.has_budgets;
                                    });
                                }
                            };
                            config.data_url = Importer.BASE_API_URL + 'domain-divisions/';
                            break;
                        case 'budget':
                            config.partials = {
                                entities: 'entities'
                            };
                            config.signals = {
                                post_render : function () {
                                    uijet.start([{
                                        type    : 'Datepicker',
                                        config  : {
                                            element : '#period_start_picker'
                                        }
                                    }, {
                                        type    : 'Datepicker',
                                        config  : {
                                            element : '#period_end_picker'
                                        }
                                    }])
                                    .then( this.wakeContained.bind(this) );
                                }
                            };
                            config.data_url = Importer.BASE_API_URL + 'entities/';
                    }

                    if ( this.has_type_ext ) {
                        this.destroyContained();
                        var new_el = uijet.$(this.type_ext_html)[0];
                        this.type_ext_position.parentNode.insertBefore(new_el, this.type_ext_position);
                    }

                    this.has_type_ext = true;

                    uijet.start({
                        factory : 'import_form_ext',
                        config  : config
                    })
                    .then( this.wakeContained.bind(this) );
                },
                'period_start_picker.picked': function (date) {
                    var date_str = date.toISOString().replace(/([^T]+)(T.*)/, '$1');
                    this.$element.find('[name=period_start]').val(date_str);
                },
                'period_end_picker.picked'  : function (date) {
                    var date_str = date.toISOString().replace(/([^T]+)(T.*)/, '$1');
                    this.$element.find('[name=period_end]').val(date_str);
                },
                'import_form_submit.clicked': function () {
                    this.submit({
                        file: this.$element.find('[name=sourcefile]')[0].files[0]
                    });
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#import_form_submit'
        }
    }, {
        type    : 'List',
        config  : {
            element     : '#import_errors',
            mixins      : ['Templated'],
            dont_wake   : true,
            app_events  : {
                'upload.failed' : 'wake+'
            }
        }
    }]);

    return Importer;

});
