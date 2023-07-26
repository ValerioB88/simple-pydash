var plotlyPlotsId=0;


var PlotlyPlot = function (location, width, height) {
    // Create the div element
    var div = document.createElement('div');
    div.style.width = width + 'px';
    div.style.height = height + 'px';
    div.id = "plotly" + plotlyPlotsId++

    // Append the div to the specified location
    document.getElementById(location + 'Col').appendChild(div);

    this.render = function(new_data) {
        if (new_data != null) {
            var fig = JSON.parse(new_data);
    
            Plotly.react(div.id, fig.data, fig.layout, {displayModeBar: false});
        }
    };


    this.reset = function() {
        Plotly.purge(div.id);
    };
};
