(function (root, factory) {
    if ( typeof module != 'undefined' && module.exports ) {
        module.exports = factory(root);
    }
    else if ( typeof define === 'function' && define.amd ) {
        define(function () {
            return factory(root);
        });
    }
    else {
        root.obudget = factory(root);
    }
}(this, function (root) {

    var CSRF_TOKEN_RE = /csrftoken=([a-zA-Z0-9]+)/,
        global_xhr_settings = {
            headers : {}
        },
        loc = root.location,
        API_INDEX = root.API_INDEX || (loc.protocol + '//api.' + loc.host + '/'),
        API_VERSION = root.API_VERSION || 'v1',
        API_URL = API_INDEX,
        AUTH_DATA = {
            client_id       : '751be246011e8a6198d7',
            client_secret   : 'c62cb3b66fcbe46b82ecda2ed146b7bfe24fdea4',
            grant_type      : 'password',
            username        : 'admin',
            password        : 'morelove!'
        },
        obudget;

    /**
     * Looks for Django's CSRF token in cookies and gets the token if found.
     * 
     * Example using with jQuery:
     * 
     * $(document).ajaxSend(function (event, xhr, settings) {
     *     if ( ! settings.headers )
     *         settings.headers = {};
     *
     *     if ( ! ('X-CSRFToken' in settings.headers) )
     *         settings.headers['X-CSRFToken'] = api.getCSRFToken();
     *  });
     * 
     * @returns {String|null} CSRF token
     */
    function getCSRFToken () {
        var match = document.cookie && document.cookie.match(CSRF_TOKEN_RE);
        return match && match[1];
    }

    function isObject (obj) {
        return Object.prototype.toString.call(obj) == '[object Object]';
    }

    function extend () {
        var args = Array.prototype.slice.call(arguments),
            target = args.shift(),
            source,
            is_deep,
            s;
        if ( typeof target == 'boolean' ) {
            is_deep = target;
            target = args.shift();
        }
        
        while ( source = args.shift() ) {
            if ( is_deep ) {
                for ( s in source ) {
                    if ( isObject(source[s]) && isObject(target[s]) ) {
                        target[s] = extend(true, {}, target[s], source[s]);
                    }
                    else {
                        target[s] = source[s];
                    }
                }
            }
            else {
                for ( s in source ) {
                    target[s] = source[s];
                }
            }
        }
        return target;
    }

    function urlSerialize (data) {
        if ( isObject(data) ) {
            var result = [];
            var key;
            for ( key in data ) {
                if ( isObject(data[key]) ) {
                    result.push(key + '=' + JSON.stringify(data[key]));
                }
                else {
                    result.push(key + '=' + data[key]);
                }
            }
            result = result.join('&');
            return result;
        }
        return data;
    }

    function Request (url, ops) {
        if ( !(this instanceof Request) ) return new Request(url, ops);
        var options;
        if ( isObject(url) ) {
            options = url;
        }
        else {
            if ( isObject(ops) ) {
                options = ops;
            }
            else {
                options = {};
            }
            if ( typeof url == 'string' ) {
                options.url = url;
            }
        }
        this.options = extend(true, {}, global_xhr_settings, ops || {});
        return this.request();
    }
    Request.prototype = {
        request : function () {
            var xhr, h, data = [];
            if ( root.XMLHttpRequest ) {
                xhr = new XMLHttpRequest();
            }

            if ( xhr ) {
                this.xhr = xhr;
            }
            else {
                throw new Error('XMLHttpRequest object not supported.');
            }

            xhr.onreadystatechange = this.response.bind(this);

            xhr.open(this.options.method || this.options.type || 'GET', this.options.url);

            if ( this.options.headers ) {
                for ( h in this.options.headers ) {
                    xhr.setRequestHeader(h, this.options.headers[h]);
                }
            }
            else {
                this.options.headers = {};
            }

            if ( ! this.options.headers['Contet-Type'] ) {
                    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
            }
            if ( ! this.options.headers['Accept'] ) {
                xhr.setRequestHeader('Accept', 'application/json');
            }
            if ( ! this.options.headers['X-CSRFToken'] ) {
                xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
            }

            data = urlSerialize(this.options.data);

            xhr.send(data || this.options.data);

            return this;
        },
        response: function () {
            var xhr = this.xhr, 
                ops = this.options,
                response;

            try {
                if ( xhr.readyState === 4 ) {
                    if ( xhr.status === 200 || xhr.status === 201 ) {
                        if ( typeof ops.success == 'function') {
                            response = xhr.responseText;
                            if ( ops.dataType === 'json' ) {
                                try {
                                    response = JSON.parse(response);
                                }
                                catch (e) {}
                            }
                            ops.success(response);
                        }
                    }
                    else if ( typeof ops.error == 'function') {
                        ops.error(xhr.responseText, xhr.status);
                    }
                }
            }
            catch (e) {
                if ( typeof ops.error == 'function') {
                    ops.error(xhr.responseText);
                }
            }
        }
    };
    Request.options = function (options) {
        extend(true, global_xhr_settings, options || {});
        return this;
    };
    Request.setHeader = function (header, value) {
        global_xhr_settings.headers[header] = value;
        return this;
    };
    function setEndpoint (name, endpint) {
        obudget[name] = function (options) {
            return new Request(endpint, extend(true, {
                method  : 'GET',
                dataType: 'json',
                error   : function (response) {
                    throw new Error('Request to' + endpint + ' failed: ' + response);
                }
            }, options || {}));
        };
    }

    obudget = {
        Request         : Request,
        getCSRFToken    : getCSRFToken,
        getVersion      : function (options) {
            return new Request(API_URL, extend(true, {
                method  : 'GET',
                dataType: 'json',
                success : function (response) {
                    API_URL = response[API_VERSION];
                    obudget.has_version_endpoint = true;
                },
                error   : function (response) {
                    throw new Error('Request to' + API_URL + ' failed: ' + response);
                }
            }, options || {}));
        },
        versionWrapper  : function (method, options) {
            if ( obudget.has_version_endpoint ) {
                return method(options);
            }
            else {
                return obudget.getVersion({
                    success : function (response) {
                        API_URL = response[API_VERSION];
                        obudget.has_version_endpoint = true;
                        method(options);
                    }
                });
            }
        },
        /**
         * Generate an OAuth2 token URI from `AUTH_DATA`
         */
        _authTokenURI   : function (options) {
            var splitter = '://',
                index_split = API_INDEX.split(splitter);
            return index_split[0] + splitter +
                options.client_id + ':' + 
                options.client_secret + '@' + 
                index_split[1] + 'auth/token/';
        },
        /**
         * Get an OAuth2 token
         */
        auth           : function (options) {
            return new Request(obudget._authTokenURI(options.data), extend(true, {
                method  : 'POST',
                data    : options.data || AUTH_DATA,
                dataType: 'json',
                success : function (response) {
                    Request.setHeader('Authorization', 'Bearer ' + response.access_token);
                    obudget.getRoutes();
                },
                error   : function (response) {
                    throw new Error('Auth failed: ' + response);
                }
            }, options || {}));
        },
        _getRoutes      : function (options) {
            return new Request(API_URL, extend(true, {
                method  : 'GET',
                dataType: 'json',
                success : obudget._setRoutes,
                error   : function (response) {
                    throw new Error('Request to' + API_URL + ' failed: ' + response);
                }
            }, options || {}));
        },
        getRoutes       : function (options) {
            return obudget.versionWrapper(obudget._getRoutes, options);
        },
        _setRoutes      : function (routes) {
            var route, split_route, route_name;

            obudget.routes = {};

            for ( route in routes ) {
                split_route = route.split(' ');
                if ( split_route.length > 1 ) {
                    route_name = split_route.shift().toLowerCase() + split_route.join('');
                }
                else {
                    route_name = split_route[0].toLowerCase();
                }
                obudget.routes[route_name] = routes[route];
                setEndpoint(route_name, routes[route]);
            }
        },
        getRoute        : function (name) {
            return obudget.routes[name];
        },
        getTimelineRoute: function (entity, nodes) {
            return obudget.getRoute('sheets') +
                'timeline/' + entity +
                '/?nodes=' + nodes.join(',');
        }
    };
    return obudget;
}));
