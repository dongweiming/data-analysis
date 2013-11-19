var i = -1, toastCount = 0, $toastlast, total, des;
var SmipleColumn = function (chartData) {
	// SERIAL CHART
	var chart;
	chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData.result;
	chart.categoryField = chartData.title;
	// the following two lines makes chart 3D
	chart.depth3D = 20;
	chart.angle = 30;

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	categoryAxis.labelRotation = 90;
	categoryAxis.ashLength = 5;
	categoryAxis.gridPosition = "start";

	// value
	var valueAxis = new AmCharts.ValueAxis();
	valueAxis.title = chartData.category;
	valueAxis.dashLength = 5;
	chart.addValueAxis(valueAxis);

	// GRAPH
	var graph = new AmCharts.AmGraph();
	graph.valueField = chartData.value;
	graph.colorField = "color";
	graph.balloonText = "<span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	chart.addGraph(graph);

	// CURSOR
	var chartCursor = new AmCharts.ChartCursor();
	chartCursor.cursorAlpha = 0;
	chartCursor.zoomable = false;
	chartCursor.categoryBalloonEnabled = false;
	chart.addChartCursor(chartCursor);

	// WRITE
	chart.write("chartdiv");
};

var Pie = function (chartData) {
    // PIE CHART
    chart = new AmCharts.AmPieChart();
    chart.dataProvider = chartData.result;
    chart.titleField = chartData.title;
    chart.valueField = chartData.value;
    chart.outlineColor = "#FFFFFF";
    chart.outlineAlpha = 0.8;
    chart.outlineThickness = 2;
    chart.balloonText = "[[title]]<br><span style='font-size:14px'><b>[[value]]</b> ([[percents]]%)</span>";
    // this makes the chart 3D
    chart.depth3D = 15;
    chart.angle = 30;

    // WRITE
    chart.write("chartdiv");
};

var Table = function (chartData) {
	var html = '<table class="pure-table"><thead><tr>'
	//$.each(chartData.th, function( index, record ) {
	//	html += '<th>' + record  + '</th>'
    //    html += '</tr></thead>'
	//});
	html += '<th>' + chartData.title  + '</th>' + '<th>' + chartData.value  + '</th>' + '<th>' + chartData.include  + '</th>'
	$.each(chartData.result, function( index, record ) {
		if (index % 2 == 0){
			html += '<tr class="pure-table-odd"><td>' + record.name + '</td><td>' + record.call + '</td><td>' + record.include + '</td></tr>';
			}
		else
			{
	    html += '<tr><td>' + record.name + '</td><td>' + record.call + '</td><td>' + record.include + '</td></tr>';
		}
	});
	html += '</table>';
	$("#chartdiv").append(html);
};

var SelectThis = function (a, toastCount, toastr) {
	var b = 0;
	var url = window.location.pathname.replace(/(.*)/,"/json$1");
	$.getJSON(url, function(result){
		$.each(result, function(k, v) {
			var vt = $('#vt').val();
			if (vt == k) {
				if (typeof(a) == 'undefined') {
					$.each(v, function(index, type) {
						$('#st').append("<option>" + type[0] + "</option>");
					});
				}
				else {
					$.each(v, function(index, type) {
						if (a == type[0]) {
							b = index;
					}
				})};
				$.each(v[b][1], function(index, type) {
					$('#ct').append("<option>" + type + "</option>");
				});
			}
		});
		}
	);
	MyChart();
}

var Toastr = function (toastCount, toastr, title, msg) {
	var shortCutFunction = "success";
    var toastIndex = toastCount++;
	var $toast = toastr[shortCutFunction](title, msg);
	$toastlast = $toast;
};

var MyChart = function () {
	var vt = $('#vt').val();
	var type = $('#st').val();
	var chart = $('#ct').val();
	$.ajax(
	   {
	      type: "POST",
	      dataType: "json",
	      data: {"type": type, "chart": chart, "vt": vt},
		  success: function(chartData){
		  	switch(chartData.chart)
		  	{
		  	case 'pie':
		  	  var Chartit = Pie;
		  	  break;
		  	case 'simple_column':
		  	  var Chartit = SmipleColumn;
		  	  break;
		  	case 'multi_column':
		  	  var Chartit = MultiColumn;
		  	  break;
		  	default:
		  	  var Chartit = SmipleColumn;
		  	}
		     Chartit(chartData);
			 Toastr(toastCount, toastr, chartData.total, chartData.des);		 
		  }
		});
}

var MultiColumn = function (chartData) {
    // SERIAL CHART
    chart = new AmCharts.AmSerialChart();
    chart.dataProvider = chartData.result;
    chart.categoryField = chartData.title;
    chart.color = "#FFFFFF";
    chart.fontSize = 14;
    chart.startDuration = 1;
    chart.plotAreaFillAlphas = 0.2;
    // the following two lines makes chart 3D
    chart.angle = 30;
    chart.depth3D = 60;

    // AXES
    // category
    var categoryAxis = chart.categoryAxis;
    categoryAxis.gridAlpha = 0.2;
    categoryAxis.gridPosition = "start";
    categoryAxis.gridColor = "#FFFFFF";
    categoryAxis.axisColor = "#FFFFFF";
    categoryAxis.axisAlpha = 0.5;
    categoryAxis.dashLength = 5;

    // value
    var valueAxis = new AmCharts.ValueAxis();
    valueAxis.stackType = "3d"; // This line makes chart 3D stacked (columns are placed one behind another)
    valueAxis.gridAlpha = 0.2;
    valueAxis.gridColor = "#FFFFFF";
    valueAxis.axisColor = "#FFFFFF";
    valueAxis.axisAlpha = 0.5;
    valueAxis.dashLength = 5;
    valueAxis.titleColor = "#FFFFFF";
    valueAxis.unit = "%";
    chart.addValueAxis(valueAxis);

	// GRAPHS         
    // first graph
    var graph1 = new AmCharts.AmGraph();
    graph1.title = chartData.titles[0];
    graph1.valueField = chartData.values[0];
    graph1.type = "column";
	graph1.colorField = "color1";
    graph1.lineAlpha = 0;
    graph1.fillAlphas = 1;
    graph1.balloonText = chartData.titles[0] + " [[category]] : <b>[[value]]</b>";
    chart.addGraph(graph1);

    // second graph
    var graph2 = new AmCharts.AmGraph();
    graph2.title = chartData.titles[1];
    graph2.valueField = chartData.values[1];
    graph2.type = "column";
	graph2.colorField = "color2";
    graph2.lineAlpha = 0;
    graph2.fillAlphas = 1;
    graph2.balloonText = chartData.titles[1] + " [[category]] : <b>[[value]]</b>";
    chart.addGraph(graph2);
	
    var graph3 = new AmCharts.AmGraph();
    graph3.title = chartData.titles[2];
    graph3.valueField = chartData.values[2];
    graph3.type = "column";
	graph3.colorField = "color3";
    graph3.lineAlpha = 0;
    graph3.fillAlphas = 1;
    graph3.balloonText = chartData.titles[2] + " [[category]] : <b>[[value]]</b>";
    chart.addGraph(graph3);

    chart.write("chartdiv");
    };
