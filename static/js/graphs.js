var type_name = "Packet Size";
var chart;
var original_quic_data;
var original_https_data;
var quic_data;
var https_data;
var deleted = [];


//$(document).ready(function() { $("#loader").append("<img src='./static/images/radio.gif') }}"+ Math.random() + "'/>"); })

function changeMetric(event){
    event = event || window.event;
    var source = event.target || event.srcElement;
    type_name = source.innerHTML;

    var table = document.getElementById("trace_table");
    table.style.display = "none";

    var chart_div = document.getElementById("chart");
    chart_div.style.display = "block";

    var chartTitle = document.getElementById("con33");
    chartTitle.innerHTML = type_name + " Graph";

    var trace_file = document.getElementById("trace_file_name");
    trace_file.style.display = "block";

    var options = document.getElementById("con33333");
    options.style.display = "none";

    var sampling_div = document.getElementById("sampling_div")
    if(type_name == "Packet Size" || type_name == "Payload Size")
        sampling_div.style.display = "block";
    else
        sampling_div.style.display = "none";

    changeTraceFile();
}

function changeTraceFile(){
    var video_options = document.getElementById("con333");
    video_options.style.display = "block";


    var trace_file = document.getElementById("trace_file_name");
    var trace_file_selected = trace_file.value;

    var sampling_type_element = document.getElementById("sampling_type");
    var sampling_type = sampling_type_element.value;

    var sampling_no_element = document.getElementById("samplingNo");
    var samplingNo = sampling_no_element.value;

    if(type_name == "HTTPS/QUIC"){
        var trace_table = document.getElementById("table");
        trace_table.style.display = "none";
//        var radio = document.getElementById("radio");
//        temp = radio.src;
//        radio.src ="none";
//        radio.src=temp;
        var loader = document.getElementById("loader");
        loader.style.display = "block";
    }



	$.ajax({
		type: 'POST',
		url: '/metrics',
		data: {
		    'type_name': type_name,
			'trace_file': trace_file_selected,
            'sampling_type': sampling_type,
            'samplingNo': samplingNo,
		},
		success: function(msg){
		    var parsed = JSON.parse(msg)
            d3.select("svg").remove();
            if (type_name == "Packet Size" || type_name == "Payload Size")
		        drawBarChart(parsed['all_packets']);
		    else if (type_name == "Packet Loss Rate")
		        drawDonutChart(parsed['all_packets']);
		    else if (type_name == "HTTPS/QUIC")
		        makeTraceTable(parsed['all_packets'])
//		    drawScatterPlot(parsed['vis_results'], parsed['sampled_labels'])
		}
	});
}


function changeComp(event){
    event = event || window.event;
    var source = event.target || event.srcElement;
    type_name = source.innerHTML;

    var trace_table = document.getElementById("trace_table");
    trace_table.style.display = "none";

    var chart_div = document.getElementById("chart");
    chart_div.style.display = "block";

    var chartTitle = document.getElementById("con33");
    chartTitle.innerHTML = type_name + " Graph";

    var video_options = document.getElementById("con333");
    video_options.style.display = "none";

    var trace_file = document.getElementById("trace_file_name");
    trace_file.style.display = "none";

    var options = document.getElementById("con33333");
    options.style.display = "block";

    $.ajax({
		type: 'POST',
		url: '/compare',
		data: {
		    'type_name': type_name,
		},
		success: function(msg){
		    var parsed = JSON.parse(msg)
            d3.select("svg").remove();
            original_https_data = parsed['https_packets'];
            original_quic_data = parsed['quic_packets']
            drawComparisonBarChart(original_quic_data, original_https_data);
            showVideoOptions(original_quic_data.length);
//            if (type_name == "Packet Size" || type_name == "Payload Size")
//		        drawBarChart(parsed['all_packets']);
//		    else if (type_name == "Packet Loss Rate")
//		        drawPieChart(parsed['all_packets']);
//		    drawScatterPlot(parsed['vis_results'], parsed['sampled_labels'])
		}
	});
}


function showTrace(event){

    event = event || window.event;
    var source = event.target || event.srcElement;
    type_name = source.innerHTML;

    var trace_table = document.getElementById("trace_table");
    trace_table.style.display = "block";

    var trace_file = document.getElementById("trace_file_name");
    trace_file.style.display = "block";

    var chartTitle = document.getElementById("con33");
    chartTitle.innerHTML = "Packet Trace";

    var options = document.getElementById("con333");
    options.style.display = "block";

    var sampling_div = document.getElementById("sampling_div")
    sampling_div.style.display = "none";

    changeTraceFile();
}

function makeTraceTable(packets){
    var trace_table = document.getElementById("table");
    $("#table:not(:first) tr").remove();
    for(i = 0; i < packets.length; i++){
        var row = trace_table.insertRow(i+1);
        var packet = packets[i].split(" ");
        for(j = 0; j < packet.length; j++){
            var cell1 = row.insertCell(j);
            cell1.innerHTML = packet[j];
        }
    };

    loader.style.display = "none";
    trace_table.style.display = "block";
}

function showVideoOptions(videoNo){
    var i;
    var options_div = document.getElementById("videos");
    while (options_div.hasChildNodes()) {
        options_div.removeChild(options_div.lastChild);
    };
    for(i = 1; i < videoNo; i++){
        var checkbox = document.createElement('input');
        var checkbox_id = "Video"+(i-1);
        checkbox.type = "checkbox";
        checkbox.name = checkbox_id;
        checkbox.value = i;
        checkbox.id = checkbox_id;
        checkbox.checked = "true";
        checkbox.onclick = function (){
            if(this.checked)
                add_video(this.value);
            else
                delete_video(this.value);
        }
        options_div.appendChild(checkbox);

        var label = document.createElement('label');
        label.htmlFor = checkbox_id;
        label.appendChild(document.createTextNode(checkbox_id));

        options_div.appendChild(label);
        options_div.appendChild(document.createElement("br"));
    }

}

function add_video(index){
    index = parseInt(index);
    deleted.splice(deleted.indexOf(index));
    update_data();
}

function delete_video(index){
    index = parseInt(index);
    deleted.push(index);
    update_data();
}

function update_data(){
    quic_data = [];
    https_data = [];
    for(i = 0; i < original_quic_data.length; i++){
        if(deleted.indexOf(i) == -1){
            quic_data.push(original_quic_data[i]);
            https_data.push(original_https_data[i]);
        }
    }
    chart.load({
        columns: [
            https_data,
            quic_data
        ],
        unload: ['QUIC', 'HTTPS'],
    });
}

function changeProtocol(){
    var HTTPS_protocol = document.getElementById("HTTPS_protocol");
    if(HTTPS_protocol.checked)
        chart.show(['HTTPS']);
    else
        chart.hide(['HTTPS']);

    var QUIC_protocol = document.getElementById("QUIC_protocol");
    if(QUIC_protocol.checked)
        chart.show(['QUIC']);
    else
        chart.hide(['QUIC']);
}

function drawBarChart(data){
    labelPadding = 70;
    d3.select("svg").remove();
    var margin = {top: 50, right: 20, bottom: 30, left: 50},
    width = 870 - margin.left - margin.right,
    height = 570 - margin.top - margin.bottom;
    barPadding = 1;
    var dataset = [];
    obj = {'attr':0, 'amount':0}
        dataset[0] = obj
    for(i = 1; i < data.length+1; i++){
        obj = {'attr':i, 'amount':+data[i-1]}
        dataset[i] = obj
    }
    console.log(data.length+1)
    obj = {'attr':(data.length+1), 'amount':0}
        dataset[data.length+1] = obj

    var x = d3.scale.linear().range([labelPadding, width]);
    var y = d3.scale.linear().range([height - labelPadding, 0]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(40);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(10);


    // Adds the svg canvas
    var svg = d3.select("#chart")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");


        // Scale the range of the data
        x.domain(d3.extent(dataset, function(d) { return +d.attr; }));
        y.domain(d3.extent(dataset, function(d) { return +d.amount; }));

        // Add the X Axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + (height - labelPadding) + ")")
            .call(xAxis);
//            .append("text")
////          .attr("transform", "rotate(-270)")
//          .attr("x", 1)
//          .attr("dx", ".1em")
//          .style("text-anchor", "start")
//          .text("PacketNo.");

        // Add the Y Axis
        svg.append("g")
          .attr("class", "y axis")
          .attr("transform", "translate("+labelPadding+",0)")
          .call(yAxis);
//        .append("text")
////          .attr("transform", "rotate(-270)")
//          .attr("y", 1)
//          .attr("dy", ".1em")
//          .style("text-anchor", "end")
//          .text(type_name);

        svg.selectAll(".xaxis text")  // select all the text elements for the xaxis
          .attr("transform", function(d) {
             return "translate(" + this.getBBox().height*-2 + "," + this.getBBox().height + ")rotate(-45)";
         });

         svg.append("text")
            .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
            .attr("transform", "translate("+ (labelPadding/2) +","+(height/2)+")rotate(-90)")  // text is drawn off the screen top left, move down and out and rotate
            .text(type_name);

        svg.append("text")
            .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
            .attr("transform", "translate("+ (width/2) +","+(height-(labelPadding/3))+")")  // centre below axis
            .text("PacketNo.");

        svg.selectAll(".bar")
        .data(dataset)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(+d.attr) - ((width - labelPadding) / dataset.length - barPadding)/2; })
        .attr("width", (width - labelPadding) / dataset.length - barPadding)
        .attr("y", function(d) { return y(+d.amount); })
        .attr("height", function(d) { return ((height - labelPadding) - y(+d.amount)); })
        .attr("fill", "darkblue");
};


function drawPieChart(data) {
    var dataset = [];
    for(i = 0; i < data.length; i++){
        if(i == 0){
            obj = {'name':'Packets Loss', 'count':+data[i]};
        }
        else{
            obj = {'name':'Packets Received', 'count':+data[i]};
        }
        dataset[i] = obj;
    }

    d3.select("svg").remove();
    var margin = {top: 50, right: 20, bottom: 30, left: 50},
    width = 870 - margin.left - margin.right,
    height = 570 - margin.top - margin.bottom;
    var radius = Math.min(width, height) / 2;
    var color = d3.scale.category20b();

    var svg = d3.select('body')
            .append('svg')
            .data([dataset])
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', 'translate(' + (width / 2) + ',' + (height / 2) + ')');
    var arc = d3.svg.arc()
            .outerRadius(radius - 40);
    var pie = d3.layout.pie()
            .value(function (d) {
                return d.count;
            })
            .sort(function (d) {
                return null;
            });
    var g = svg.selectAll("g.slice")
            .data(pie)
            .enter()
            .append("g")
            .attr("class", "slice");
            g.append("path")
            .attr("d", arc)
            .style("fill", function (d) {
                return color(d.value);
            });

    g.append("svg:title").text(function (d, i) {
        return dataset[i].name;
    });

    g.append("svg:text")
      .attr("transform", function(d) { //set the label's origin to the center of the arc
        //we have to make sure to set these before calling arc.centroid
        d.outerRadius = radius; // Set Outer Coordinate
        d.innerRadius = radius - 5; // Set Inner Coordinate
        return "translate(" + arc.centroid(d) + ")rotate(" + angle(d) + ")";
      })
      .attr("text-anchor", "middle") //center the text on it's origin
      .style("fill", "darkblue")
      .style("font", "bold 12px Arial")
      .text(function(d, i) { return dataset[i].name; });

    g.append("text")
    .attr("transform", function (d, i) {
        d.outerRadius = radius; // Set Outer Coordinate
        d.innerRadius = radius * 2 / 3;
        return "translate(" + arc.centroid(d) + ")";
    })
    .style("fill", "Black")
    .style("font", "bold 10px Arial")
    .style("text-anchor", "middle")
    .text(function (d, i) {
        return dataset[i].count + "%";
    });
}

function angle(d) {
  var a = (d.startAngle + d.endAngle) * 90 / Math.PI - 180;
  console.log(a);
  return a < 0 ? a + 180 : a;
}

function drawComparisonBarChart(){
    chart = c3.generate({
        bindto: '#chart',
        data: {
            columns: [
                original_https_data,
                original_quic_data
            ],
            type: 'bar'
        },
        bar: {
            width: {
                ratio: 0.5 // this makes bar width 50% of length between ticks
            }
        }
    });

//    chart.resize({height:500, width:800});
}

function groupData(){

    var groupDataButton = document.getElementById("Group_Data");
    if(groupDataButton.checked == true)
        chart.groups([['HTTPS', 'QUIC']])
    else{
        drawComparisonBarChart();
//        chart.load({
//            columns: [original_https_data, original_quic_data]
//        });
    }
}

function drawDonutChart(data){

    var chart = c3.generate({
    data: {
        columns: [
            ['Packets Loss', data[0]],
            ['Packets Received', data[1]],
        ],
        type : 'donut',
//        onclick: function (d, i) { console.log("onclick", d, i); },
//        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
//        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
    },
    donut: {
        title: type_name
    }
});
}

function drawLineChart(data){

    d3.select("svg").remove();
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = 800 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    var dataset = []
    for(i = 0; i < data.length; i++){
        obj = {'attr':i+1, 'amount':data[i]}
        dataset[i] = obj
    }
    var x = d3.scale.linear().range([0, width]);
    var y = d3.scale.linear().range([height - 30, 30]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(1000);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(10);

    // Define the line
    var valueline = d3.svg.line()
        .x(function(d) { return x(d.attr); })
        .y(function(d) { return y(d.amount); })
        .interpolate("basis");

    // Adds the svg canvas
    var svg = d3.select("#chart")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");


        // Scale the range of the data
        x.domain(d3.extent(dataset, function(d) { return +d.attr; }));
        y.domain(d3.extent(dataset, function(d) { return +d.amount; }));

        // Add the valueline path.
        svg.append("path")
            .attr("class", "line")
            .attr("d", valueline(dataset));

        // Add the X Axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        // Add the Y Axis
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);
};

function drawScatterPlot(xy_data, labels){
    var data = [];
    var x_data = xy_data[0];
    var y_data = xy_data[1];
    for(i = 0; i < x_data.length; i++){
        obj = {'xdata':x_data[i], 'ydata':y_data[i], 'label':labels[i]};
        data[i] = obj;
    }

    var margin = {top: 20, right: 20, bottom: 30, left: 80},
    width = 900 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.category10();

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

    x.domain(d3.extent(data, function(d) { return d.xdata; })).nice();
    y.domain(d3.extent(data, function(d) { return d.ydata; })).nice();

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

    svg.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 3.5)
      .attr("cx", function(d) { return x(d.xdata); })
      .attr("cy", function(d) { return y(d.ydata); })
      .style("fill", function(d) { return color(d.label); });
};