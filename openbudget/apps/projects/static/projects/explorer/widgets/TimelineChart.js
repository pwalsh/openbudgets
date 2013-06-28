define([
    'uijet_dir/uijet',
    'resources',
    'api',
    'd3'
], function (uijet, resources, api) {

    var d3 = window.d3,
        period = uijet.Utils.prop('period'),
        amount = uijet.Utils.prop('amount'),
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
        },
        prepareElement  : function () {
            this._super();
            var element = this.$element[0],
                width = element.offsetWidth,
                height = element.offsetHeight,
//                x = d3.time.scale()
                x = d3.time.scale()
                    .range([0, width]),
                y = d3.scale.linear()
                    .range([height, 0]),
                x_axis = d3.svg.axis()
                    .scale(x)
                    .orient('bottom')
                    .ticks(d3.time.years),
                y_axis = d3.svg.axis()
                    .scale(y)
                    .orient('left');

            this.width = width;
            this.height = height;
            this.x_axis = x_axis;
            this.y_axis = y_axis;
            this.x_scale = x;
            this.y_scale = y;

            this.line = d3.svg.line()
//                .interpolate('basis')
                .x( function(d) { return x(d.period); } )
                .y( function(d) { return y(d.amount); } );

            this.svg = d3.select(this.$element[0]).append('svg')
                .attr('width', width)
                .attr('height', height)
                .append('g');
//                    .attr('transform', 'translate(20,20)');
        },
        render          : function () {
            this._super();
            this.set(uijet.Resource('LegendItems').models).then(function () {
                this.draw(this.resource.models);
            }.bind(this));
            return this;
        },
        draw            : function (series) {
            var line = this.line,
                ids = [],
                data = [],
                colors = this.colors;

            series.forEach(function (item) {
                var id = item.cid,
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

            this.svg.append('g')
                .attr('class', 'x_axis')
                .attr('transform', 'translate(0,' + (this.height - 20) + ')')
                .call(this.x_axis);

            this.svg.append('g')
                .attr('class', 'y_axis')
                .attr('transform', 'translate(20,0)')
                .call(this.y_axis);

            var timeline = this.svg.selectAll('.timeline')
                .data(data)
                .enter()
                .append('g')
                    .attr('class', 'timeline');

            timeline.append('path')
                .attr('class', 'line')
                .attr('d', function(d) {
                    return line(d.values);
                })
                .style('stroke', function(d) { return colors(d.id); });
        }
    });

});
