define([
    'uijet_dir/uijet',
    'd3'
], function (uijet, d3) {

    uijet.Widget('BarChart', {
        init  : function () {
            var res = this._super.apply(this, arguments);

            var margin = {top: 20, right: 20, bottom: 30, left: 40},
                width = 960 - margin.left - margin.right,
                height = 500 - margin.top - margin.bottom;

            this.margin = margin;
            this.height = height;
            this.width = width;

            this.x0 = d3.scale.ordinal()
                .rangeRoundBands([0, width], .1);

            this.x1 = d3.scale.ordinal();

            this.y = d3.scale.linear()
                .range([height, 0]);

            this.color = d3.scale.ordinal()
                .range(["#00CCC2", "#CCC200", "#C200CC", "#CC00C2", "#CC00C2"]);

            this.xAxis = d3.svg.axis()
                .scale(this.x0)
                .orient("bottom");

            this.yAxis = d3.svg.axis()
                .scale(this.y)
                .orient("left")
                .tickFormat(d3.format(".2s"));

            this.svg = d3.select(this.$element[0]).append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            return res;
        },
        render: function () {
            var data = this.resource.byParent(uijet.Resource('ItemsListState')
                    .get('scope'))
                    .map(function (model) {
                        return model.attributes;
                    }),
                height = this.height,
                color = this.color,
                x0 = this.x0,
                x1 = this.x1,
                y = this.y,
                xAxis = this.xAxis,
                yAxis = this.yAxis,
                amount_types = ['actual', 'budget'];

            x0.domain(data.map(function (d) {
                return d.code;
            }));
            x1.domain(amount_types).rangeRoundBands([0, x0.rangeBand()]);
            y.domain([
                0, d3.max(data, function (d) {
                    return d3.max([d.actual, d.budget]);
                })
            ]);

            var axes = this.svg.selectAll('.axis');
            if ( ! axes.empty() ) {
                axes.remove();
            }

            this.svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            this.svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", ".71em")
                .style("text-anchor", "end")
                .text("Amount");

            var item = this.svg.selectAll(".item")
                .data(data, function (d) {
                    return d.id;
                });

            item.exit().remove();

            var entered = item.enter().append("g")
                .attr("class", "g item")
                .attr("transform", function (d) {
                    return "translate(" + x0(d.code) + ",0)";
                });

            // draw bars
            entered.selectAll(".bar")
                .data(function (d) {
                    return [{type: 'budget', amount: d.budget},
                            {type: 'actual', amount: d.actual}];
                })
                .enter().append("rect")
                .attr('class', 'bar')
                .attr("width", x1.rangeBand())
                .attr("x", function (d) {
                    return x1(d.type);
                })
                .attr("y", function (d) {
                    return y(d.amount);
                })
                .attr("height", function (d) {
                    return height - y(d.amount);
                })
                .style("fill", function (d) {
                    return color(d.type);
                });

            // draw titles
            var titles = entered.append('g')
                .attr('class', 'bar_titles')
                .attr('transform', function () {
                    // 20 for margin from bottom
                    // 8 for height/2
                    return 'translate(' + (x1.rangeBand() + 8) + ',' + (height - 20) + ') rotate(-90)';
                });

            // draw title backgrounds
            titles.append('rect');

            // enter text
            titles.append('text')
                .text(function (d) {
                    return d.name;
                }).each(function () {
                    var margin = 10,
                        box = this.getBBox(),
                        height = box.height + margin;
                    d3.select(this.previousSibling)
                        .attr('width', box.width + margin)
                        .attr('height', height)
                        .attr('y', - height / 2 - margin / 2)
                        .attr('x', - margin / 2);
                });

//            var legend = svg.selectAll(".legend")
//                .data(ageNames.slice().reverse())
//                .enter().append("g")
//                .attr("class", "legend")
//                .attr("transform", function (d, i) {
//                    return "translate(0," + i * 20 + ")";
//                });
//
//            legend.append("rect")
//                .attr("x", width - 18)
//                .attr("width", 18)
//                .attr("height", 18)
//                .style("fill", color);
//
//            legend.append("text")
//                .attr("x", width - 24)
//                .attr("y", 9)
//                .attr("dy", ".35em")
//                .style("text-anchor", "end")
//                .text(function (d) {
//                    return d;
//                });
        }
    });
});
