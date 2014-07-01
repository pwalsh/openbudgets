LIBRARY_FILES = \
	node_modules/d3/src/start.js \
	node_modules/d3/src/compat/index.js \
	node_modules/d3/src/arrays/min.js \
	node_modules/d3/src/arrays/max.js \
	node_modules/d3/src/format/format.js \
	node_modules/d3/src/selection/selection.js \
	node_modules/d3/src/scale/linear.js \
	node_modules/d3/src/scale/ordinal.js \
	node_modules/d3/src/svg/axis.js \
	node_modules/d3/src/end.js

explorer.d3: $(LIBRARY_FILES)
	node_modules/.bin/smash $(LIBRARY_FILES) > openbudgets/apps/entities/static/entities/explorer/d3.js
