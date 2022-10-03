var LinePlot = function(series, canvas_width, canvas_height) {
	this.max_length_data = 50
	var canvas_tag = "<canvas width='" + canvas_width + "' height='" + canvas_height + "' ";
	canvas_tag += "style='border:1px dotted'></canvas>";
	var canvas = $(canvas_tag)[0];
	$("#rightCol").append(canvas);
	var context = canvas.getContext("2d");

	var convertColorOpacity = function(hex) {

		if (hex.indexOf('#') != 0) {
			return 'rgba(0,0,0,0.1)';
		}

		hex = hex.replace('#', '');
		r = parseInt(hex.substring(0, 2), 16);
		g = parseInt(hex.substring(2, 4), 16);
		b = parseInt(hex.substring(4, 6), 16);
		return 'rgba(' + r + ',' + g + ',' + b + ',0.1)';
	};

	// Prep the chart properties and series:
	var datasets = []
	for (var i in series) {
		var s = series[i];
		var new_series = {
			label: s.Label,
			borderColor: s.Color,
			backgroundColor: convertColorOpacity(s.Color),
			data: []
		};
		datasets.push(new_series);
	}

	var chartData = {
		labels: [],
		datasets: datasets
	};

	var chartOptions = {
		responsive: true,
		// maintainAspectRatio: false,
		tooltips: {
			mode: 'index',
			intersect: false
		},
		pointRadius: 1,
		hover: {
			mode: 'nearest',
			intersect: true
		},
		scales: {
			y: {
				display: true
			},
			x: {
				display: false
			}
		}

	};

	var chart = new Chart(context, {
		type: 'line',
		data: chartData,
		options: chartOptions
	});

	this.render = function(newdata) {
		if (newdata != null)
		{
				chart.data.labels.push(control.tick);
				if (chart.data.labels.length > this.max_length_data) {
					chart.data.labels.shift();

				}
				for (i = 0; i < newdata.length; i++) {

					if (chart.data.datasets[i].data.length > this.max_length_data) {
						chart.data.datasets[i].data.shift();
					}
					chart.data.datasets[i].data.push(newdata[i])
				}
				chart.update('none');
		}
	};

	this.reset = function() {
		//while (chart.data.labels.length) { chart.data.labels.pop(); }
		chart.data.datasets.forEach(function(dataset) {
			{ dataset.data = [] }
		});
		chart.update();
	};
};
