function makeGraph(){
	$.ajax({
		type: 'GET',
		url: '/text_visualization',
		success: function(msg){
		    var parsed = JSON.parse(msg);
		    drawScatterPlot(parsed['x_data1'], parsed['y_data1'], parsed['x_data2'], parsed['y_data2'], parsed['words']);
		}
	});
}


function drawScatterPlot(x_data1, y_data1, x_data2, y_data2, words){
    var data = [];
    for(i = 0; i < x_data1.length; i++){
        obj = {'xdata1':x_data1[i], 'ydata1':y_data1[i], 'label':"circ", 'name':words[i]};
        data[i] = obj;
    }

    for(i = 0; i < x_data2.length; i++){
        obj = {'xdata1':x_data2[i], 'ydata1':y_data2[i], 'label':"rect", 'name':('D'+i)};
        data[x_data1.length + i] = obj;
    }


    var margin = {top: 20, right: 20, bottom: 30, left: 80},
    width = 900 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var svg = d3.select("#scatterplot").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    x.domain(d3.extent(data, function(d) { return d.xdata1; })).nice();
    y.domain(d3.extent(data, function(d) { return d.ydata1; })).nice();

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end");

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end");


    var shapes = svg.selectAll(".shapes")
        .data(data).enter();

    shapes.append("circle")
      .filter(function(d){ if(d.label=="circ") return d })
      .attr("class", "dot")
      .attr("r", 3.5)
      .attr("cx", function(d) { return x(d.xdata1); })
      .attr("cy", function(d) { return y(d.ydata1); })
      .style("fill", "blue")
      .append("title")
        .text(function (d) {
            return d.name;
        });


    shapes.append("rect")
        .filter(function(d){ if(d.label=="rect") return d })
        .attr("class", "dot")
        .attr("width", 7)
        .attr("height", 7)
        .attr("x", function(d) { console.log(d.xdata1); return x(d.xdata1); })
        .attr("y", function(d) { console.log(d.ydata1); return y(d.ydata1); })
        .style("fill", "green")
        .append("title")
        .text(function (d) {
            return d.name;
        });

};