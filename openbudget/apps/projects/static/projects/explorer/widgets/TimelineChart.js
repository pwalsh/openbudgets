define([
    'uijet_dir/uijet',
    'resources',
    'api',
    'd3'
], function (uijet, resources, api) {

    var Y_TICKS = 5;

    var d3 = window.d3,
        period = uijet.utils.prop('period'),
        amount = uijet.utils.prop('amount'),
        dateParser = d3.time.format('%Y').parse,
        commas = d3.format(','),
        periodParser = function (d) {
            d.period = dateParser(d.period);
        };

    uijet.Widget('TimelineChart', {
        options         : {
            type_class  : ['uijet_chart', 'uijet_timelinechart']
        },
        init            : function () {
            this._super.apply(this, arguments);
            this.colors = d3.scale.category10();
            uijet.publish('chart_colors', this.colors.range());
        },
        prepareElement  : function () {
            this._super();
            var element = this.$element[0],
                padding = 20,
                left_sidebar_width = 100,
                width = element.offsetWidth,
                // need to expand the width of the SVG element to be able to draw y axis labels outside the chart area
                svg_width = width + padding + left_sidebar_width,
                height = element.offsetHeight,
//                x = d3.time.scale()
                x = d3.time.scale()
                    .range([padding, width - padding]),
                y = d3.scale.linear()
                    .range([height, padding]),
                x_axis = d3.svg.axis()
                    .scale(x)
                    .orient('bottom')
                    .ticks(d3.time.years),
                y_axis = d3.svg.axis()
                    .scale(y)
                    .orient('left')
                    .ticks(Y_TICKS);

            this.padding = padding;
            this.left_sidebar_width = left_sidebar_width;
            this.svg_width = svg_width;
            this.width = width;
            this.height = height;
            this.x_axis = x_axis;
            this.y_axis = y_axis;
            this.x_scale = x;
            this.y_scale = y;

            this.line = d3.svg.line()
                .x( function(d) { return x(d.period); } )
                .y( function(d) { return y(d.amount); } );

            this.svg_element = d3.select(this.$element[0]).append('svg')
                .attr('width', svg_width)
                .attr('height', height + 70);
            this.svg = this.svg_element.append('g')
                .attr('transform', 'translate(' + (svg_width - width) + ',0)')
                .append('svg')
                    .attr('width', width)
                    .attr('height', height + 70);
            this.mouse_target = this.svg.append('rect')
                .attr('height', height)
                .attr('width', width)
                .attr('id', 'mouse_target');
            return this;
        },
        _draw           : function () {
            return this.publish('fetched', this.resource)
                .draw(this.resource.models);
        },
        render          : function () {
            this._super();

            if ( this.context && this.context.state_loaded ) {
                this._draw();
                delete this.context.state_loaded;
            }
            else {
                this.set(uijet.Resource('LegendItems').models).then(this._draw.bind(this));
            }
            return this;
        },
        draw            : function (series) {
            var line = this.line,
                colors = this.colors,
                ids = [],
                data = [],
                y_max;
            
            series.forEach(function (item) {
                var id = item.id + '-' + item.get('updated'),
                    title = item.get('title'),
                    muni = item.get('muni'),
                    type = item.get('amount_type'),
                    series_type_index = type === 'actual' ? 0 : 1,
                    item_series = item.toSeries();
                item_series[series_type_index].forEach(periodParser);
                ids.push(id);
                data.push({
                    id      : id,
                    title   : title,
                    type    : type,
                    muni    : muni,
                    values  : item_series[series_type_index]
                });
            });

            y_max = d3.max(data, function (d) { return d3.max(d.values, amount); });

            this.colors.domain(ids);

            this.x_scale.domain([
                d3.min(data, function (d) { return d3.min(d.values, period); }),
                d3.max(data, function (d) { return d3.max(d.values, period); })
            ]);
            this.y_scale.domain([
                0,
                y_max
            ]);

            // clean axes
            this.svg_element.selectAll('.axis')
                .remove();

            this.svg.insert('g', '#mouse_target')
                .attr('class', 'axis x_axis')
                .attr('transform', 'translate(0,' + (this.height + this.padding) + ')')
                .call(this.x_axis);

            this.svg_element.insert('g', ':first-child')
                .attr('class', 'axis y_axis')
                .attr('transform', 'translate(' + this.left_sidebar_width + ',0)')
                .call(this.y_axis)
                .selectAll('line')
                    .attr('x2', this.padding)
                    .attr('x1', this.width + this.padding);

            this.svg.selectAll('.timeline').remove();

            var timelines = this.svg.selectAll('.timeline')
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
                        .style('stroke', function(d) { return colors(d.id); });

            this.mouse_target.on('mouseover', this.hoverOn.bind(this));
            this.mouse_target.on('mouseout', this.hoverOff.bind(this));
        },
        timeContext     : function (from, to) {
            var domain = this.x_scale.domain(),
                line = this.line,
                from_value, to_value, x_axis;
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

            from_value = from.valueOf();
            to_value = to.valueOf();

            this.x_scale.domain([from, to]);

            x_axis = this.svg.select('.x_axis');
            x_axis.call(this.x_axis)
                .selectAll('line')
                    .attr('x1', 0)
                    .attr('y2', -this.padding)
                    .attr('y1', -(this.height));
            x_axis.selectAll('text')
                .each(function (d) {
                    var value = d.valueOf(),
                        hide = value === to_value || value === from_value;
                    d3.select(this).classed('hide', hide);
                });

            this.svg.selectAll('.line').attr('d', function (d) {
                return line(d.values);
            });

            // reset mouseover handler
            this.hoverOff();
            this.mouse_target.on('mouseover', this.hoverOn.bind(this));

            return this;
        },
        hoverOn         : function () {
            this.mouse_target.on('mousemove', this.mousemove());
        },
        hoverOff        : function () {
            this.mouse_target.on('mousemove', null);
            this.hoverMark();
            this.current_hovered_index = null;
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
                d3.selectAll('.value_circle').remove();
            }
        },
        markValues      : function (x_value) {
            var labels,
                datums = [],
                x = this.x_scale,
                y = this.y_scale,
                width = this.width,
                color = this.colors,
                added_label, added_label_texts;
            d3.selectAll('.timeline').each(function (d, i) {
                d.values.some(function (point_datum) {
                    if ( point_datum.period.valueOf() === x_value.valueOf() ) {
                        datums.push({
                            period  : point_datum.period,
                            amount  : point_datum.amount,
                            id      : d.id,
                            title   : d.title,
                            muni    : d.muni
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
                d.color = color(d.id);
            });

            labels = this.svg.selectAll('.value_circle').data(datums, function (d) { return d.id + d.period; });

            labels.exit().remove();

            added_label = labels.enter().append('g')
                .attr('class', 'value_circle');
            
            added_label_texts = added_label.append('g')
                .attr('class', 'value_label')
                .attr('transform', 'translate(0,-10)');

//            added_label_texts.append('text')
//                .attr('class', 'title');

            added_label_texts.append('text')
                .attr('class', 'amount');

            added_label.append('circle');

            labels.sort(function (a, b) { return a.amount - b.amount; });

            labels.attr('transform', function (d) {
                return 'translate(' + d.x + ',' + d.y + ')';
            });

            labels.selectAll('text')
                .attr('fill', function (d) { return d.color; });
            labels.selectAll('.amount')
                .text(function (d) { return commas(d.amount); })
                .attr('x', function () {
                    return - (this.getBBox().width + 10);
                });
//            labels.selectAll('.title')
//                .text(function (d) { return d.muni + ': ' + d.title; });

            d3.selectAll('.value_label')
                .attr('transform', function (d, i) {
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
                            y_pos = prev_y - d.y - 30
                        }
                        else if ( dy < 20 ) {
                            y_pos = -30;
                        }
                        else {
                            y_pos = -10;
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

                    return 'translate(' + x_pos + ',' + y_pos + ')';
                });

            labels.select('circle')
                .attr('r', 5)
                .style('fill', function (d) { return d.color; });
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
