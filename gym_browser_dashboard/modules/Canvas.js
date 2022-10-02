var ContinuousVisualization = function(canvas, context, w, h, imgid) {
	this.draw = function(objects) {
		img = document.getElementById(imgid)
		img.src = "data:image/png;charset=utf-8;base64," + objects;
	};
};

var Canvas = function(id, penv_width, penv_height) {
	let imgid = "img" + id
	var canvas_tag = "<img src='' width='480'  height='320' id=" + imgid + ">"
	var canvas = $(canvas_tag)[0];

	$("#elements").append(canvas);
	let context = null // canvas.getContext("2d");
	let canvasDraw = new ContinuousVisualization(canvas, context, penv_width, penv_height, imgid);
	add_checkbox("checkbox" + id, "Render", "elements")

	this.render = function(data) {
		if (document.getElementById("checkbox" + id).checked)
			canvasDraw.draw(data)
	};


	this.reset = function() {
	};

};