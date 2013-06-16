define([
    'uijet_dir/uijet',
    'importer/app',
    'controllers/ImportForm',
    'importer/widgets/DatepickerInput'
], function (uijet, Importer, ImportFormController) {

    var FORM_TYPE_EXT_ID = '#import_form_type_ext';

    uijet.Adapter('ImportForm', ImportFormController);

    uijet.Factory('import_form_ext', {
        type    : 'Pane',
        config  : {
            element         : FORM_TYPE_EXT_ID,
            mixins          : ['Templated'],
            template_name   : 'template-form',
            partials_dir    : 'partials/',
            app_events      : {
                destroy_form_ext: function (new_config) {
                    this.destroy()
                        .publish('destroyed', new_config);
                }
            }
        }
    });

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element : '#form_container'
        }
    }, {
        type    : 'Form',
        config  : {
            element     : '#import_form',
            adapters    : ['Spin', 'ImportForm'],
            signals     : {
                post_init       : function () {
                    var type_ext = this.$element.find(FORM_TYPE_EXT_ID)[0];
                    this.type_ext_html = type_ext.outerHTML;
                    this.type_ext_position = type_ext.nextElementSibling;
                },
                start_form_ext  : function (config) {
                    uijet.start({
                        factory : 'import_form_ext',
                        config  : config
                    })
                    .then(function () {
                        this.has_type_ext = true;
                        this.wakeContained();
                    }.bind(this));
                }
            },
            app_events  : {
                'import_form_type.changed'      : function (data) {
                    var config = this.formExtConfigByType(data.value);

                    if ( this.has_type_ext ) {
                        var new_el = uijet.$(this.type_ext_html)[0];
                        this.type_ext_position.parentNode.insertBefore(new_el, this.type_ext_position);
                        uijet.publish('destroy_form_ext', config);
                    }
                    else {
                        this.notify('start_form_ext', config);
                    }
                },
                'period_start_picker.picked'    : function (date) {
                    this.$element.find('[name=period_start]').val(this.parseDate(date));
                },
                'period_end_picker.picked'      : function (date) {
                    this.$element.find('[name=period_end]').val(this.parseDate(date));
                },
                'import_form_submit.clicked'    : function () {
                    this.spin()
                        .submit({
                            file: this.$element.find('[name=sourcefile]')[0].files[0]
                        });
                },
                'import_form_type_ext.destroyed': function (config) {
                    this.notify('start_form_ext', config);
                },
                'upload.failed'                 : 'spinOff',
                'upload.done'                   : 'spinOff'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#import_form_submit',
            signals     : {
                pre_click   : function () {
                    this.disable();
                }
            },
            app_events  : {
                'upload.failed' : 'enable',
                'upload.done'   : 'enable'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element : '#import_message',
            dont_wake   : true,
            signals     : {
                post_init   : function () {
                    this.$import_message_exp = uijet.$('#import_message_exp');
                }
            },
            app_events  : {
                'upload.failed'             : function () {
                    this.$element.text('Import failed due to:');
                    this.wake(true);
                },
                'upload.done'               : function () {
                    this.$element.text('Import succeeded!');
                    this.$import_message_exp.removeClass('hide');
                    this.wake(true);
                },
                'import_form_submit.clicked': function () {
                    this.$import_message_exp.addClass('hide');
                    this.sleep();
                }
            }
        }
    }, {
        type    : 'List',
        config  : {
            element     : '#import_errors',
            mixins      : ['Templated', 'Scrolled'],
            adapters    : 'jqWheelScroll',
            dont_wake   : true,
            app_events  : {
                'upload.failed'             : 'wake+',
                'import_form_submit.clicked': function () {
                    this.sleep()
                        .$element.empty();
                }
            }
        }
    }]);

    return Importer;

});
