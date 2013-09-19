define([
    'uijet_dir/uijet',
    'project_widgets/TimelineChart'
], function (uijet) {
    
    uijet.Widget('TimelineChartEmbed', {
        createCanvas    : function () {
            this.canvas = d3.select(this.$element[0]).append('svg')
                .attr('width', this.root_svg_width)
                .attr('height', this.height)
                .append('g');

            return this;
        },
        createScales    : function () {
            var padding = this.padding;

            this.x_scale = d3.time.scale()
                .range([padding, this.width - padding]);
            this.y_scale = d3.scale.linear()
                .range([this.height - 50, padding + 10]);
            
            return this;
        },
        drawAxes        : function () {
            var before = '#mouse_target',
                y_axis;
            // clean axes
            this.canvas.selectAll('.axis')
                .remove();

            // create axes
            this.canvas.insert('g', before)
                .attr('class', 'axis x_axis')
                .attr('transform', 'translate(0,' + (this.height - 50) + ')')
                .call(this.x_axis);

            y_axis = this.canvas.insert('g', before)
                .attr('class', 'axis y_axis')
                .call(this.y_axis);

            y_axis.selectAll('line')
//                .attr('x2', -this.padding)
                .attr('x1', this.width);

            y_axis.selectAll('text')
                .attr('dy', 0)
                .attr('y', -4);

            return this;
        },
        drawTimelines   : function (data) {
            var line = this.line,
                x = this.x_scale,
                y = this.y_scale,
                timelines, timeline_containers;

            // clean timelines
            this.canvas.selectAll('.timeline').remove();

            timelines = this.canvas.selectAll('.timeline')
                .data(data, function (d) {
                    return d.id;
                });

            timeline_containers = timelines.enter()
                .insert('g', '#mouse_target')
                    .attr('class', 'timeline');

            timeline_containers.append('path')
                .attr('class', 'line')
                .attr('d', function(d) {
                    return line(d.values);
                })
                .style('stroke', function(d) { return d.color; });

            timeline_containers.selectAll('.value_dot')
                .data(function (d) {
                    return d.values.map(function (val) {
                        // tag every point with it's series' color
                        val.color = d.color;
                        return val;
                    });
                })
                .enter().append('circle')
                    .attr('class', 'value_dot')
                    .attr('cx', function (d, i) {
                        return x(d.period);
                    })
                    .attr('cy', function (d, i) {
                        return y(d.amount);
                    })
                    .attr('r', 4)
                    .style('fill', function (d) { return d.color; });

            return this;
        },
        drawTimeContext : function (from, to) {
            var line = this.line,
                x_axis = this.canvas.select('.x_axis');

            x_axis.call(this.x_axis)
                .selectAll('line')
                    .attr('x1', 0)
                    .attr('y2', 0)
                    .attr('y1', -(this.height));

            this.canvas.selectAll('.line').attr('d', function (d) {
                return line(d.values);
            });

            return this;
        }
    }, {
        widgets : ['TimelineChart']
    });

});
