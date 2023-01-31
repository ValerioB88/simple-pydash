var Histogram = function (series, width, height, location, chart_title = '') {

    var canvas_tag = "<canvas width='" + width + "' height='" + height + "' ";
    canvas_tag += "style='border:1px dotted'></canvas>";
    var canvas = $(canvas_tag)[0];
    location = location + 'Col'
    $("#" + location).append(canvas);

    var context = canvas.getContext("2d");

    var convertColorOpacity = function (hex, opacity) {

        if (hex.indexOf('#') != 0) {
            return 'rgba(0,0,0,0.1)';
        }

        hex = hex.replace('#', '');
        r = parseInt(hex.substring(0, 2), 16);
        g = parseInt(hex.substring(2, 4), 16);
        b = parseInt(hex.substring(4, 6), 16);
        return 'rgba(' + r + ',' + g + ',' + b + ', ' + opacity + ')';
    };

    // Prep the chart properties and series:
    var datasets = []
    for (var i in series) {
        var s = series[i];
        var new_series = {
            label: s.Label, borderWidth:1, borderColor: convertColorOpacity(s.Color, 1), backgroundColor: convertColorOpacity(s.Color, 0.2), data: [], replace: (s.Replace === "false") ? false : true
        };
        datasets.push(new_series);
    }

    var chartData = {
        labels: [], datasets: datasets
    };

    var chartOptions = {
        animation: false, responsive: true, intersect: true, interaction: {
            mode: 'nearest' //'point'
        },

        // maintainAspectRatio: false,
        tooltips: {
            mode: 'index', intersect: false

        },
        scales: {
            x: {
                type: 'linear',
                offset: false,
                grid: {
                    offset: false
                },
                ticks: {
                    stepSize: 1
                },
            }
        },
        plugins: {
            title: {
                display: true, text: chart_title
            },
            zoom: {
                zoom: {
                    wheel: {
                        enabled: true,
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'xy',
                },
                pan: {
                    enabled: true,
                }
            }
        }
    };

        var chart = new Chart(context, {
            type: 'bar',  // line plot doesn't work well when adding many points in one go
            data: chartData, options: chartOptions
        });



        this.render = function (newdata) {
            if (newdata != null) {
                for (i = 0; i < newdata.length; i++) {
                    if (newdata[i] == 'clear') {
                        chart.data.datasets[i].data = []
                    } else {
                        if (chart.data.datasets[i].replace) {
                            if (newdata[i].length == 0) {
                                chart.data.datasets[i].data = []
                            } else {
                                chart.data.datasets[i].data = newdata[i]
                            }
                        } else {
                            for (d = 0; d < newdata[i].length; d++) {
                                chart.data.datasets[i].data.push(newdata[i][d])
                            }
                        }
                        // if (xmax != null) {
                        //     var this_data = chart.data.datasets[i].data
                        //     xdatamax = Math.max.apply(Math, this_data.map(v => v['x']))
                        //     xdatamin = Math.min.apply(Math, this_data.map(v => v['x']))
                        //     var range = xdatamax - xdatamin
                        //
                        //     if (range > xmax) {
                        //         var idx = xdatamax - xmax
                        //         chart.data.datasets[i].data = this_data.filter(v => v['x'] > idx)
                        //         this_data = chart.data.datasets[i].data
                        //     }
                        //     xdatamax = Math.max.apply(Math, this_data.map(v => v['x']))
                        //     Object.assign(chartOptions.scales.x, {max: xdatamax, min: xdatamax - xmax})
                        // }
                    }
                }

                // for (i = 0; i < newdata.length; i++) {
                //  chart.data.datasets[i].data.push(newdata[i])
                // chart.data.datasets[i].data.push(newdata[i])

                // }

                // for (i = 0; i < newdata.length; i++) {
                // if (chart.data.datasets[i].data.length > this.max_length_data) {
                // 	chart.data.datasets[i].data.shift();
                // }
                // chart.data.datasets[0].data.push([{x: 1, y:1}, {x: 2, y:2},  {x: 3, y:3});
                // chart.data.datasets[0].data.push({ label: 'prova', fill: false, data:[{x: 1, y: 1}, {x: 2, y: 2}]})

                // chart.data.datasets[0].data.push(   {x:5, y:2} ,{x:10, y:12},{x:50, y:25}      )
                // chart.data.datasets[0].data.push([{x: 2, y:2}]);
                // chart.data.datasets[0].data.push([{x: 5, y:2}]);


                // }
                chart.update();
            }
        };

        this.reset = function () {
            //while (chart.data.labels.length) { chart.data.labels.pop(); }
            chart.data.datasets.forEach(function (dataset) {
                {
                    dataset.data = []
                }
            });
            chart.update();
        };
    };
