define([
    'uijet_dir/uijet',
    'api',
    'resources'
], function (uijet, api, resources) {

    /**
     * Utility lambdas for formatting template
     */
    var getUserAvatar = function () {
            return function (text, render) {
                return render(text).replace(/s=\d+/, 's=25');
            };
        },
        multiline = function (text) {
            return text.replace(/(\r?\n)/g, '<br/>');
        },
        linesToBRs = function () {
            return function (text, render) {
                return multiline(render(text));
            };
        },
        formatDate = function (date) {
            return date &&
                    [date.getDate(), date.getMonth() + 1, date.getFullYear()].join('.');
        },
        parseCreatedOn = function () {
            return function (text, render) {
                var value = render(text),
                    date = value ? new Date(value) : value;
                return formatDate(date);
            };
        },
        new_comment_data = {
            discussion  : {
                id              : '',
                comment         : '',
                created_on      : '',
                user            : window.LOGGEDIN_USER,
                get_user_avatar : getUserAvatar,
                parse_date      : parseCreatedOn,
                lines_to_brs    : linesToBRs
            }
        },
        rescrollToBottom = function () {
            this.scroll().scrollTo(this.$element.children().last());
        };

    uijet.Resource('NewComment', uijet.Model(), {
        user: window.LOGGEDIN_USER.uuid
    });

    return [{
        type    : 'Button',
        config  : {
            element     : '#items_comments_close',
            dont_wake   : true,
            signals     : {
                pre_click   : function () {
                    uijet.Resource('ItemsListState').set('comments_item', null);
                    this.sleep();
                }
            },
            app_events  : {
                open_comments   : 'wake'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element         : '#items_comments_container',
            mixins          : ['Scrolled'],
            adapters        : ['jqWheelScroll'],
            resource        : 'NewComment',
            dont_wake       : true,
            cloak           : true,
            jqscroll_options: {
                exclude_padding : true
            },
            signals         : {
                post_init   : function () {
                    this.$description = this.$element.find('#item_description');
                }
            },
            data_events     : {
                'change:comment': function (model, comment) {
                    api.itemComments(this.resource.get('item_pk'), {
                        type    : 'POST',
                        data    : {
                            comment : encodeURIComponent(resources._.escape(comment.trim())),
                            user    : model.get('user')
                        },
                        success : function (response) {
                            uijet.publish('comment_created', response);
                        },
                        error   : function (response) {
                            uijet.publish('comment_failed', response);
                        }
                    });
                }
            },
            app_events      : {
                open_comments                   : function ($selected) {
                    var item_id = $selected.attr('data-item'),
                        item = item_id ? uijet.Resource('LatestSheet').get(item_id) : null,
                        //TODO: for now there's no SheetComment model, needs to be implemented server-side 
                        discussion = item && item.get('discussion'),
                        description = item ?
                                      // found an item
                                      item.get('description') :
                                      // if no item it's the sheet's description we need
                                      uijet.Resource('AllSheets').get(
                                          uijet.Resource('ItemsListState').get('sheet')
                                      ).get('description');

                    //TODO: delete this shit
                    this.$element[0].style.setProperty('padding-top', (uijet.utils.getOffsetOf($selected[0], uijet.$element[0]).y + 15) + 'px');
                    if ( description ) {
                        this.$element.removeClass('no_description');
                        this.$description.text(description);
                    }
                    else {
                        this.$element.addClass('no_description');
                    }

                    this.resource.set('item_pk', item_id);

                    this.wake({
                        discussion      : discussion,
                        get_user_avatar : getUserAvatar,
                        parse_date      : parseCreatedOn,
                        lines_to_brs    : linesToBRs
                    });
                },
                close_comments                  : 'sleep',
                'new_comment.line_added'        : rescrollToBottom,
                'new_comment.awake'             : rescrollToBottom,
                'new_comment.asleep'            : rescrollToBottom,
                'item_comments_list.rendered'   : 'scroll'
            }
        }
    }, {
        type    : 'List',
        config  : {
            element         : '#item_comments_list',
            mixins          : ['Templated', 'Translated'],
            adapters        : ['Spin'],
            dont_fetch      : true,
            spinner_options : {
                element     : function () {
                    return this.$new_comment.find('.item_comment_date');
                },
                lines       : 8,
                length      : 5,
                width       : 3,
                radius      : 3
            },
            signals         : {
                post_render : 'rendered'
            },
            app_events      : {
                'add_comment.clicked'       : function () {
                    this.$new_comment = this.$element.append(this.template(new_comment_data))
                        .children().last();
                    uijet._translate(this.$new_comment[0]);
                },
                'new_comment_cancel.clicked': function () {
                    if ( this.$new_comment ) {
                        this.$new_comment.remove();
                        delete this.$new_comment;
                    }
                },
                'new_comment_ok.clicked'    : 'spin',
                comment_created             : function (comment) {
                    if ( this.$new_comment ) {
                        this.$new_comment.find('.item_comment_text').html(multiline(comment.comment));
                        this.$new_comment.find('.item_comment_date').text(formatDate(new Date(comment.created_on)));
                        this.$new_comment.attr('data-id', comment.id);
                        this.$new_comment.removeClass('new_comment');
                        delete this.$new_comment;
                    }
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#add_comment',
            signals     : {
                pre_click   : function  () {
                    if ( ! uijet.Resource('NewComment').has('user') ) {
                        uijet.publish('login');
                        return false
                    }
                    else {
                        this.sleep();
                    }
                }
            },
            app_events  : {
                'new_comment_ok.clicked'    : 'wake',
                'new_comment_cancel.clicked': 'wake'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#new_comment',
            resource    : 'NewComment',
            dont_wake   : true,
            signals     : {
                post_init       : function () {
                    var that = this;
                    this.$textarea = this.$element.find('textarea');
                    this.$textarea.on('keyup', function (e) {
                        if ( this.scrollHeight > this.clientHeight ) {
                            this.style.height = this.scrollHeight + 'px';
                            that.publish('line_added');
                        }
                    });
                },
                pre_wake        : function () {
                    this.$element.removeClass('hide');
                },
                post_appear     : function () {
                    this.$textarea.focus();
                    this.publish('awake');
                },
                post_disappear  : function () {
                    this.publish('asleep');
                },
                pre_sleep       : function () {
                    var textarea = this.$textarea[0];
                    textarea.value = '';
                    textarea.style.removeProperty('height');
                    this.$element.addClass('hide');
                }
            },
            data_events : {},
            app_events  : {
                'add_comment.clicked'       : 'wake',
                'new_comment_ok.clicked'    : function () {
                    this.resource.set('comment', this.$textarea.val());
                },
                comment_created             : function () {
                    this.resource.set('comment', '', { silent : true });
                    this.sleep();
                },
                'new_comment_cancel.clicked': 'sleep',
                open_comments               : 'sleep',
                close_comments              : 'sleep'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#new_comment_ok',
            signals     : {
                pre_click   : 'sleep'
            },
            app_events  : {
                'new_comment_cancel.clicked': 'sleep'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#new_comment_cancel',
            signals     : {
                pre_click   : 'sleep'
            },
            app_events  : {
                'new_comment_ok.clicked': 'sleep'
            }
        }
    }];
});
