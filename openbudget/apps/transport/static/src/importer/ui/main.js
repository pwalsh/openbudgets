define([
    'uijet_dir/uijet',
    'importer/app',
    'composites/Datepicker'
], function (uijet, Importer) {

    uijet.Factory('import_form_ext', {
        type    : 'Pane',
        config  : {
            element         : '#import_form_type_ext',
            mixins          : ['Templated'],
            template_name   : 'budgettemplate-form',
            partials_dir    : 'partials/',
            signals         : {
                post_render : function () {
                    var datepicker_id = 'period_start_picker';
                    uijet.start([{
                        type    : 'Datepicker',
                        config  : {
                            element : '#' + datepicker_id
                        }
                    }])
                    .then( this.wakeContained.bind(this) );
                }
            }
        }
    });

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element : '#heading',
            position: 'top:50'
        }
    }, {
        type    : 'Form',
        config  : {
            element     : '#import_form',
            position    : 'fluid',
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
                            config.data_url = Importer.BASE_API_URL + 'domain-divisions/';
                            break;
                    }

                    uijet.start({
                        factory : 'import_form_ext',
                        config  : config
                    })
                    .then( this.wakeContained.bind(this) );
                },
                'period_start_picker.picked': function (date) {
                    this.$element.find('[name=period_start]').val(date.toLocaleString());
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
    }]);

    return Importer;

});
