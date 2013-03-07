/**!
 * Eventbox Pub/Sub - simple, tiny and robust.
 * Copyright (C) 2011 Yehonatan Daniv <maggotfish@gmail.com> under the WTFPL license
 *
 *          DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
 * TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
 *
 * 0. You just DO WHAT THE FUCK YOU WANT TO.
 *
 */
(function (_window, factory) {
	if ( typeof define === 'function' && define.amd ) {
		define(function () {
			return factory(_window);
		});
	} else {
		_window.Eventbox = factory(_window);
	}
}(window, function (global) {

	var _self, _scope,
		Box = {},
		objToString = global.Object.prototype.toString,
		_token = 0;


	function isObj(obj) {
		return objToString.call(obj) == '[object Object]';
	}


	function add(topic, fn, context) {

		var scope = context || _scope;

		if ( ! (topic in Box) )
			Box[topic] = {};

		Box[topic][_token] = scope ? fn.bind(_scope) : fn;

		return _token += 1;
	}


	function remove(type, token) {

		var t;

		if ( typeof token == 'function' && Box[type] ) {
			// `token` is a reference to a handler 
			for ( t in Box[type] )
				if ( token === Box[type][t] )
					delete Box[type][t];
		}

		else if ( Box[type] && Box[type][token] ) {
			delete Box[type][token];
		}

		else {
			delete Box[type];
		}
	}

	function emit(fn, data) {
		setTimeout(function () {
			return fn.call(this, data);
		}, 0);
	}

	return _self = {

		notify	: function (notification, data) {

			var handler, topic;

			if ( isObj(notification) ) {

				for ( topic in notification )

					if ( topic in Box )

						for ( handler in Box[topic] )
							emit(Box[topic][handler], notification[topic]);
			}

			else if ( typeof notification == 'string' && notification in Box ) {

				for ( handler in Box[notification] )
					emit(Box[notification][handler], data);

			}

			return _self;
		},


		listen	: function (notification, handler, context) {

			var handlers_map = {}, key;

			if ( isObj(notification) ) {

				if ( isObj(handler) ) {
					context = handler;
				}

				for ( key in notification )
					handlers_map[key] = add(key, notification[key], context);

			}

			else if ( typeof notification == 'string' ) {

				handlers_map = add(notification, handler, context);

			}

			if (_scope)
				_scope = null;

			return handlers_map;
		},


		unlisten: function (types, idx) {

			var topic;

			if (typeof types == 'string')
				remove(types, idx);

			else if ( isObj(types) )
				for ( topic in types )
					remove(topic, types[topic]);

			return _self;
		},


		bind	: function (scope) {
			return _scope = scope, _self;
		}


	};
}));