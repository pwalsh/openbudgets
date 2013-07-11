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
        periodParser = function (d) {
            d.period = dateParser(d.period);
        };

    uijet.Widget('TimelineChart', {
        options         : {
            type_class  : ['uijet_chart', 'uijet_timelinechart']
        },
        init            : function () {
            this._super.apply(this, arguments);
            this.colors = d3.scale.category20();
            uijet.publish('chart_colors', this.colors.range());
        },
        prepareElement  : function () {
            this._super();
            var element = this.$element[0],
                width = element.offsetWidth,
                height = element.offsetHeight,
//                x = d3.time.scale()
                x = d3.time.scale()
                    .range([20, width - 20]),
                y = d3.scale.linear()
                    .range([height - 20, 20]),
                x_axis = d3.svg.axis()
                    .scale(x)
                    .orient('bottom')
                    .ticks(d3.time.years),
                y_axis = d3.svg.axis()
                    .scale(y)
                    .orient('right')
                    .ticks(Y_TICKS);

            this.width = width;
            this.height = height;
            this.x_axis = x_axis;
            this.y_axis = y_axis;
            this.x_scale = x;
            this.y_scale = y;

            this.line = d3.svg.line()
                .x( function(d) { return x(d.period); } )
                .y( function(d) { return y(d.amount); } );

            this.svg = d3.select(this.$element[0]).append('svg')
                .attr('width', width)
                .attr('height', height);
            return this;
        },
        render          : function () {
            this._super();
            this.set(uijet.Resource('LegendItems').models).then(function () {
                this.publish('fetched', this.resource)
                    .draw(this.resource.models);
            }.bind(this));
            return this;
        },
        draw            : function (series) {
            var line = this.line,
                colors = this.colors,
                width = this.width,
                ids = [],
                data = [];

            series.forEach(function (item) {
                var id = item.cid + '-' + item.get('updated'),
                    actual_id = id + '-actual',
                    budget_id = id + '-budget',
                    title = item.get('title'),
                    item_series = item.toSeries();
                item_series[0].forEach(periodParser);
                item_series[1].forEach(periodParser);
                ids.push(actual_id, budget_id);
                data.push({
                    id      : actual_id,
                    name    : title + ' actual',
                    values  : item_series[0]
                }, {
                    id      : budget_id,
                    name    : title + ' budget',
                    values  : item_series[1]
                });
            });

            this.colors.domain(ids);

            this.x_scale.domain([
                d3.min(data, function (d) { return d3.min(d.values, period); }),
                d3.max(data, function (d) { return d3.max(d.values, period); })
            ]);
            this.y_scale.domain([
                d3.min(data, function (d) { return d3.min(d.values, amount); }),
                d3.max(data, function (d) { return d3.max(d.values, amount); })
            ]);

            // clean axes
            this.svg.selectAll('.axis')
                .remove();

            this.svg.append('g')
                .attr('class', 'axis x_axis')
                .attr('transform', 'translate(0,' + (this.height - 20) + ')')
                .call(this.x_axis)
                .selectAll('line')
                    .attr('x1', 0)
                    .attr('y2', 20)
                    .attr('y1', -(this.height - 20));

            this.svg.append('g')
                .attr('class', 'axis y_axis')
                .attr('transform', 'translate(10,0)')
                .call(this.y_axis)
                .selectAll('line')
                    .attr('x2', 20)
                    .attr('x1', this.width - 20);

            this.svg.selectAll('.timeline').remove();

            var timelines = this.svg.selectAll('.timeline')
                .data(data, function (d) {
                    return d.id;
                });

            timelines.enter()
                .append('g')
                    .attr('class', 'timeline')
                    .append('path')
                        .attr('class', 'line')
                        .attr('d', function(d) {
                            return line(d.values);
                        })
                        .style('stroke', function(d) { return colors(d.id); });

            this.svg.on('mouseover', this.hoverOn.bind(this));
            this.svg.on('mouseout', this.hoverOff.bind(this));
        },
        timeContext     : function (from, to) {
            var domain = this.x_scale.domain(),
                line = this.line;
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
            this.svg.select('.x_axis')
                .call(this.x_axis)
                .selectAll('line')
                    .attr('x1', 0)
                    .attr('y2', 20)
                    .attr('y1', -(this.height - 20));
            this.svg.selectAll('.line').attr('d', function (d) {
                return line(d.values);
            });

            // reset mouseover handler
            this.hoverOff();
            this.svg.on('mouseover', this.hoverOn.bind(this));

            return this;
        },
        hoverOn         : function () {
            this.svg.on('mousemove', this.mousemove());
        },
        hoverOff        : function () {
            this.svg.on('mousemove', null);
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
                d3.select('.x_axis').selectAll('line').classed('mark', function (d) {
                    return d.getFullYear()   === year;
                });
            }
            else {
                d3.select('line.mark').classed('mark', false);
            }
        }
    });

});
