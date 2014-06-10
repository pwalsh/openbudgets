var BASE_URL = './';
var EXPLORER_URL = 'openbudgets/apps/entities/static/entities/explorer/';
var VENDOR_URL = 'openbudgets/commons/static/vendor/';

module.exports = function (grunt) {
    return {
        explorerjs : {
            options: {
                baseUrl: BASE_URL,
                paths  : {
                    jquery                : VENDOR_URL + 'jquery/dist/jquery',
                    jqscroll              : VENDOR_URL + 'jqScroll/jqscroll',
                    'jquery.mousewheel'   : VENDOR_URL + 'jquery-mousewheel/jquery.mousewheel',
                    backbone              : VENDOR_URL + 'backbone/backbone',
                    'backbone-fetch-cache': VENDOR_URL + 'backbone-fetch-cache/backbone.fetch-cache',
                    d3                    : VENDOR_URL + 'd3/d3',
                    underscore            : VENDOR_URL + 'underscore/dist/lodash.underscore',
                    mustache              : VENDOR_URL + 'mustache/mustache',
                    q                     : VENDOR_URL + 'q/q',
                    spin                  : VENDOR_URL + 'spin/spin',
                    setImmediate          : VENDOR_URL + 'setImmediate/setImmediate',
                    eventbox              : VENDOR_URL + 'eventbox/eventbox',
                    uijet_dir             : VENDOR_URL + 'uijet/src',
                    widgets               : VENDOR_URL + 'uijet/src/widgets',
                    composites            : VENDOR_URL + 'uijet/src/composites',
                    modules               : VENDOR_URL + 'uijet/src/modules',
                    explorer              : EXPLORER_URL + 'explorer',
                    ui                    : EXPLORER_URL + 'ui',
                    resources             : EXPLORER_URL + 'resources',
                    controllers           : EXPLORER_URL + 'controllers',
                    project_modules       : EXPLORER_URL + 'modules',
                    project_widgets       : EXPLORER_URL + 'widgets',
                    project_mixins        : EXPLORER_URL + 'mixins',
                    dictionary            : EXPLORER_URL + 'dictionary',
                    api                   : VENDOR_URL + '../src/api',
                    i18n                  : VENDOR_URL + '../src/i18n',
                    site_base             : VENDOR_URL + '../js/base'
                },
                shim   : {
                    eventbox              : ['setImmediate'],
                    'backbone-fetch-cache': 'modules/data/backbone',
                    backbone              : {
                        deps   : ['underscore', 'jquery'],
                        exports: 'Backbone'
                    }
                },
                out    : BASE_URL + EXPLORER_URL + 'dist.js',
                name   : BASE_URL + VENDOR_URL + 'almond/almond.js',
                wrap   : true,
                include: [
                        BASE_URL + EXPLORER_URL + 'main'
                ],
                done   : function (done, output) {
                    var duplicates = require('rjs-build-analysis').duplicates(output);

                    if ( duplicates.length > 0 ) {
                        grunt.log.subhead('Duplicates found in requirejs build:');
                        grunt.log.warn(duplicates);
                        done(new Error('r.js built duplicate modules, please check the excludes option.'));
                    }
                    else {
                        var bundles = require('rjs-build-hasher')(output, {
                            buildPath: '/',
                            hashSize : 16
                        });

                        // save info about built files to configuration
                        grunt.file.write(BASE_URL + EXPLORER_URL + 'build.json', JSON.stringify(bundles, null, 2));
                    }

                    done();
                }
            }
        },
        explorercss: {
            options: {
                baseUrl    : BASE_URL,
                optimizeCss: 'standard',
                cssIn      : BASE_URL + EXPLORER_URL + 'css/main.css',
                out        : BASE_URL + EXPLORER_URL + 'dist.css',
                done       : function (done, output) {
                    var duplicates = require('rjs-build-analysis').duplicates(output);

                    if ( duplicates.length > 0 ) {
                        grunt.log.subhead('Duplicates found in requirejs build:');
                        grunt.log.warn(duplicates);
                        done(new Error('r.js built duplicate modules, please check the excludes option.'));
                    }
                    else {
                        var bundles = require('rjs-build-hasher')(output, {
                            buildPath: '/',
                            hashSize : 16
                        });

                        // save info about built files to configuration
                        grunt.file.write(BASE_URL + EXPLORER_URL + 'build-css.json', JSON.stringify(bundles, null, 2));
                    }

                    done();
                }
            }
        }
    }
};
