Eventbox.js
===========

About:
------
Eventbox.js is a robust yet simple app-level events observer.  
It enables loose coupling of modules and emitting custom events.


Dependencies:
------------
Eventbox.js has no dependencies what so ever and is library agnostic.


How to use:
-----------
Include the eventbox.js script at the top of your inclusion stack.
Then, anywhere in the code, you can simply call the eventbox instance with:
	Eventbox

Note: Since Eventbox is a property of the global object it is better to reference it
with a local variable for better performance.
Like: 
	var eventbox = window.Eventbox;

Eventbox.js can be used to notify/listen to notifications between different modules, like so:

Listening/notifying:

	Eventbox.listen({
		'action-a' : function (data [, arguments]) {
			// do stuff after action-a has been done
		}
	});
	Eventbox.notify({
		'action-b' : {
			stuff: 'data to send to listening handlers'
		}
	} [, arguments ]);

Or:

	Eventbox.listen('action-a', function (data [, arguments]) {
		// do stuff after action-a has been done
	});
	Eventbox.notify('action-b', {
		stuff: 'data to send to listening handlers'
	} [, arguments ]);


If .listen receives an Object as a handler it wraps it in a function that calls .notify with that Object as its param:

	Eventbox.listen({
		'action-a' : {
			'another-action': {
				//more data
			}
		}
	});

The example above means that by notifying 'action-a' 'another-action' will be notified with the corresponding object as data.


Unlistening:

	Eventbox.unlisten(type [, index]);

When unlisten receives a string it deals with it as a type and removes all event handlers
for this type.
You can also send an optional index param that will make Eventbox try to remove a specific handler from the set
of handlers registered for that type.

Mass listening/notifying:

    var types_to_indices_map = Eventbox.listen({
        'action-a' : callback_a,
        'action-b' : callback_b
        // ...
    });

    Eventbox.notify({
        'action-a' : {a:1, b:2},
        'action-b' : {c:3, d:4}
        // ...
    });

The variable "types_to_indices_map" is an object returned from Eventbox.listen that equals a map
of types to the specific index of the event handler created for it on that call.
You can send this map later to Eventbox.unlisten to remove these specific handlers, like so:

    Eventbox.unlisten(types_to_indices_map);

You can set the handlers' scope for a single .listen call (single stack):

    Eventbox.bind(my_scope).listen({
        'action-a' : callback_a,
    });

In the example above callback_a will run with my_scope as its [[this]] variable (scope).

* Note: after one call to .listen, if the scope was set with .bind it will be reset back to the
        global scope.