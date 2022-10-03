var Canvas = function(id, penv_width, penv_height, location, add_checkb) {
	let imgid = "img" + id
	var canvas_tag = "<img src='' width='" + penv_width  + "' height='" + penv_height + "' id=" + imgid + ">"
	var canvas = $(canvas_tag)[0];
	location = location + 'Col'
	$("#" + location).append(canvas);
	var add_ch = add_checkb
	if (add_ch)
	{
		add_checkbox("checkbox" + id, "Render", "#" + location)
	}

	this.render = function(data) {
		if (!add_ch || (add_ch && document.getElementById("checkbox" + id).checked))
		{
			img = document.getElementById(imgid)
			img.src = "data:image/png;charset=utf-8;base64," + data;
		}
	};


	this.reset = function() {
	};

};