define([
    'uijet_dir/uijet',
    'd3',
    'resources'
], function (uijet, d3, resources) {

    var Y_TICKS = 5;

    // depends on resources to define `uijet.utils.prop()`
    var left_sidebar_width = 100,
        period = uijet.utils.prop('period'),
        amount = uijet.utils.prop('amount'),
        dateParser = d3.time.format('%Y').parse,
        commas = d3.format(',.0f'),
        periodParser = function (d) {
            d.period = dateParser(d.period);
        },
        nis_sign = String.fromCharCode(parseInt('20aa', 16)),
        amountFormat = function (d) { return nis_sign + commas(d);};

    uijet.Widget('TimelineChart', {
        options         : {
            type_class  : ['uijet_chart', 'uijet_timelinechart']
        },
        amountFormat    : amountFormat,
        init            : function () {
            this._super.apply(this, arguments);
            // generate a range of colors
            uijet.publish('chart_colors', d3.scale.category10().range());
        },
        prepareElement  : function () {
            this._super();
            var chart_ops = this.options.chart || {},
                element = this.$element[0],
                x, y;

            this.padding = chart_ops.padding || 0;
            this.width = element.offsetWidth;
            this.height = element.offsetHeight;
            // need to expand the width of the SVG element to be able to draw y axis labels outside the chart area
            this.root_svg_width = this.width + this.padding;

            this.createScales()
                .createAxes()
                .createCanvas()
                .createLine();

            this.mouse_target = this.canvas.append('rect')
                .attr('height', this.height)
                .attr('width', this.width)
                .attr('id', 'mouse_target');

            return this;
        },
        createScales    : function () {
            var padding = this.padding;

            this.x_scale = d3.time.scale()
                .range([padding, this.width - padding]);
            this.y_scale = d3.scale.linear()
                .range([this.height, padding + 10]);
            
            return this;
        },
        createAxes      : function () {
            var chart_ops = this.options.chart;

            this.x_axis = d3.svg.axis()
                .scale(this.x_scale)
                .orient(chart_ops.axes_x_orient || 'bottom')
                .ticks(d3.time.years);

            this.y_axis = d3.svg.axis()
                .scale(this.y_scale)
                .orient(chart_ops.axes_y_orient || 'left')
                .ticks(Y_TICKS)
                .tickFormat(amountFormat);

            return this;
        },
        createCanvas    : function () {
            // expand the root canvas width to cover left sidebar so that Y axis' tick labels can render over it
            this.root_svg_width += left_sidebar_width;

            this.root_svg = d3.select(this.$element[0]).append('svg')
                .attr('width', this.root_svg_width)
                .attr('height', this.height + 70);
            this.canvas = this.root_svg.append('g')
                .attr('transform', 'translate(' + (this.root_svg_width - this.width) + ',0)')
                .append('svg')
                    .attr('width', this.width)
                    .attr('height', this.height + 70);

            return this;
        },
        createLine      : function () {
            var x = this.x_scale,
                y = this.y_scale;

            this.line = d3.svg.line()
                .x( function(d) { return x(d.period); } )
                .y( function(d) { return y(d.amount); } );

            return this;
        },
        _draw           : function () {
            this.publish('fetched', this.resource)
                .draw();
            return this;
        },
        draw            : function () {
            var series = this.resource.models,
                ids = [],
                data = [],
                context = this.getContext(),
                y_max;
            
            series.forEach(function (item) {
                var id = item.id + '-' + item.get('updated'),
                    title = item.get('title'),
                    muni = item.get('muni'),
                    type = item.get('amount_type'),
                    series_type_index = type === 'actual' ? 0 : 1,
                    color = item.get('color'),
                    item_series = item.toSeries();
                item_series[series_type_index].forEach(periodParser);
                ids.push(id);
                data.push({
                    id      : id,
                    title   : title,
                    type    : type,
                    muni    : muni,
                    values  : item_series[series_type_index],
                    color   : color
                });
            });

            y_max = d3.max(data, function (d) { return d3.max(d.values, amount); });

            this.x_scale.domain([
                d3.min(data, function (d) { return d3.min(d.values, period); }),
                d3.max(data, function (d) { return d3.max(d.values, period); })
            ]);
            this.y_scale.domain([
                0,
                y_max
            ]);

            this.drawAxes()
                .drawTimelines(data);

            this.mouse_target.on('mouseover', this.hoverOn.bind(this));
            this.mouse_target.on('mouseout', this.hoverOff.bind(this));

            var periods = this.resource.periods();
            this.timeContext(
                String(context.period_start || periods[0]),
                String(context.period_end || periods[periods.length - 1])
            );

            return this;
        },
        drawAxes        : function () {
            // clean axes
            this.root_svg.selectAll('.axis')
                .remove();

            this.canvas.insert('g', '#mouse_target')
                .attr('class', 'axis x_axis')
                .attr('transform', 'translate(0,' + (this.height + this.padding - 3) + ')')
                .call(this.x_axis);

            this.root_svg.insert('g', ':first-child')
                .attr('class', 'axis y_axis')
                .attr('transform', 'translate(' + left_sidebar_width + ',0)')
                .call(this.y_axis)
                .selectAll('line')
                    .attr('x2', this.padding)
                    .attr('x1', this.width + this.padding);

            return this;
        },
        drawTimelines   : function (data) {
            var line = this.line,
                timelines;

            // clean timelines
            this.canvas.selectAll('.timeline').remove();

            timelines = this.canvas.selectAll('.timeline')
                .data(data, function (d) {
                    return d.id;
                });

            timelines.enter()
                .insert('g', '#mouse_target')
                    .attr('class', 'timeline')
                    .append('path')
                        .attr('class', 'line')
                        .attr('d', function(d) {
                            return line(d.values);
                        })
                        .style('stroke', function(d) { return d.color; });
            return this;
        },
        timeContext     : function (from, to) {
            var domain = this.x_scale.domain();

            if ( ! from ) {
                from = domain[0];
            }
            else {
                from = dateParser(from);
            }
            if ( ! to ) {
                to = domain[1];
            }
            else {
                to = dateParser(to);
            }

            this.x_scale.domain([from, to]);

            this.drawTimeContext(
                from.valueOf(),
                to.valueOf()
            );

            if ( this.hover_on ) {
                // reset mouseover handler
                this.hoverOff()
                    .hoverOn();
            }

            return this;
        },
        drawTimeContext : function (from, to) {
            var line = this.line,
                x_axis = this.canvas.select('.x_axis');

            x_axis.call(this.x_axis)
                .selectAll('line')
                    .attr('x1', 0)
                    .attr('y2', -this.padding + 3)
                    .attr('y1', -(this.height));

            this.canvas.selectAll('.line').attr('d', function (d) {
                return line(d.values);
            });

            // hide max and min of X axis tick labels
            x_axis.selectAll('text')
                .each(function (d) {
                    var value = d.valueOf(),
                        hide = value === to || value === from;
                    d3.select(this).classed('hide', hide);
                });

            return this;
        },
        hoverOn         : function () {
            this.hover_on = true;
            this.mouse_target.on('mousemove', this.mousemove());
            return this;
        },
        hoverOff        : function () {
            this.hover_on = false;
            this.mouse_target.on('mousemove', null);
            this.hoverMark();
            this.current_hovered_index = null;
            return this;
        },
        mousemove       : function () {
            var x = this.x_scale,
                ticks_values = x.ticks(d3.time.years),
                x_ticks_coords = ticks_values.map(function (value) {
                    return x(value);
                }),
                that = this;

            return function () {
                var mouse_x = d3.mouse(this)[0],
                    right_index = d3.bisectLeft(x_ticks_coords, mouse_x),
                    left_index = right_index ? right_index - 1 : right_index,
                    new_index;
                if ( right_index !== left_index ) {
                    if ( mouse_x - x_ticks_coords[left_index] < x_ticks_coords[right_index] - mouse_x ) {
                        new_index = left_index;
                    }
                    else {
                        new_index = right_index;
                    }
                }
                else {
                    new_index = right_index;
                }
                if ( that.current_hovered_index !== new_index ) {
                    that.current_hovered_index = new_index;
                    that.hoverMark(ticks_values[new_index]);
                }
            };
        },
        hoverMark       : function (value) {
            if ( value ) {
                //TODO: this is based on assumption that data is yearly
                var year = value.getFullYear();
                d3.select('.x_axis').selectAll('.tick').classed('mark', function (d) {
                    return d.getFullYear() === year;
                });
                this.markValues(value);
            }
            else {
                d3.select('.tick.mark').classed('mark', false);
                d3.selectAll('.value_mark').remove();
            }
        },
        markValues      : function (x_value) {
            var markers,
                datums = [],
                x = this.x_scale,
                y = this.y_scale,
                added_markers;
            this.canvas.selectAll('.timeline').each(function (d, i) {
                d.values.some(function (point_datum) {
                    if ( point_datum.period.valueOf() === x_value.valueOf() ) {
                        datums.push({
                            period  : point_datum.period,
                            amount  : point_datum.amount,
                            id      : d.id,
                            title   : d.title,
                            muni    : d.muni,
                            color   : d.color
                        });
                        return true;
                    }
                });
            });
            datums.sort(function (a, b) {
                return a.amount - b.amount;
            });
            datums.forEach(function (d, i) {
                d.x = x(d.period);
                d.y = y(d.amount);
            });

            markers = this.canvas.selectAll('.value_mark')
                .data(datums, function (d) {
                    return d.id + d.period;
                });

            markers.exit().remove();

            added_markers = markers.enter().append('g')
                .attr('class', 'value_mark');

            markers.sort(function (a, b) { return a.amount - b.amount; });

            markers.attr('transform', function (d) {
                return 'translate(' + d.x + ',' + d.y + ')';
            });

            this.drawMarkedValues(datums, markers, added_markers);
        },
        drawMarkedValues: function (datums, markers, added_markers) {
            var width = this.width,
                label_transforms = [],
                labels_y_margin = 20,
                marker_values;

            this.drawMarkTexts(markers, added_markers);

            marker_values = d3.selectAll('.value_label')
                .each(function (d, i) {
                    var y_pos = -10,
                        x_pos = 0,
                        matrix = this.getCTM(),
                        bbox = this.getBBox(),
                        prev, prev_y, dy;
                    if ( i ) {
                        prev = datums[i - 1];
                        prev_y = prev.title_y || prev.y;
                        dy = prev_y - (d.y - 10);
                        // make sure we have a margin of 20px between labels' texts
                        if ( dy <= 0 ) {
                            y_pos = prev_y - d.y - (labels_y_margin + 10);
                        }
                        else if ( dy < labels_y_margin ) {
                            y_pos -= labels_y_margin;
                        }
                    }
                    // cache title position
                    d.title_y = d.y + y_pos;

                    // check if the label is exceeding the size of the canvas
                    x_pos = bbox.x + matrix.e;
                    if ( x_pos < 0 ) {
                        x_pos = -x_pos;
                    }
                    else if ( x_pos + bbox.width > width ) {
                        x_pos = width - (x_pos + bbox.width);
                    }
                    else {
                        x_pos = 0;
                    }

                    label_transforms.push([x_pos, y_pos, bbox.y + matrix.f]);
                });

            var prev_title_y = null, current_transform;
            for ( var l = label_transforms.length; l--; ) {
                current_transform = label_transforms[l];
                // if this is first iteration
                if ( prev_title_y === null ) {
                    // if current_position + y_translation < 0 -> exceeding canvas' height
                    if ( current_transform[2] + current_transform[1] < 0 ) {
                        // this is first iteration so just drop highest title to y=0
                        current_transform[1] = -current_transform[2];
                    }
                    // cache previous calculated title y position
                    prev_title_y = current_transform.pop() + current_transform[1];
                }
                // on subsequent iterations
                else {
                    // if current_position - previous_position < labels_y_margin -> less than minimal margin
                    if ( current_transform[2] + current_transform[1] - prev_title_y - labels_y_margin < 0 ) {
                        // new y_translation = previous_position - current_position + labels_y_margin
                        current_transform[1] = prev_title_y - current_transform[2] + labels_y_margin;
                    }
                    // cache previous calculated title y position
                    prev_title_y = current_transform[1] + current_transform.pop();
                }
            }

            marker_values.attr('transform', function (d, i) {
                return 'translate(' + label_transforms[i].join() + ')';
            });

            this.drawMarkCircles(markers, added_markers);

            return this;
        },
        drawMarkTexts : function (markers, added_markers) {
            added_markers.append('g')
                .attr('class', 'value_label')
                .attr('transform', 'translate(0,-10)')
                .append('text')
                    .attr('class', 'amount');

            markers.selectAll('text')
                .attr('fill', function (d) { return d.color; });
            markers.selectAll('.amount')
                .text(function (d) { return amountFormat(d.amount); })
                .attr('x', function () {
                    return - (this.getBBox().width + 10);
                });

            return this;
        },
        drawMarkCircles : function (markers, added_markers) {
            added_markers.append('circle');

            markers.select('circle')
                .attr('r', 5)
                .style('fill', function (d) { return d.color; });

            return this;
        },
        setTitle        : function (id, title) {
            if ( uijet.utils.isObj(id) ) {
                title = id.title;
                id = id.id;
            }
            d3.selectAll('.timeline').filter(function (d) {
                return d.id.indexOf(id) === 0;
            }).datum(function (d) {
                d.title = title + ' ' + d.type;
                return d;
            });
            return this;
        }
    });

});
