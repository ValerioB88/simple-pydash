var numCanvasId = 0;

function Canvas(width, height, location, add_checkb) {
  let imgId = "canvas" + numCanvasId++;

  let canvas = document.createElement("img");
  canvas.id = imgId;

  canvas.style.width = width + "px";
  canvas.style.height = height + "px";

  let locationElement = document.getElementById(location + "Col");
  locationElement.appendChild(canvas);

  if (add_checkb) {
    add_checkbox("checkbox" + id, "Render", "#" + location);
  }

  this.render = function (data) {
    if (!add_checkb || document.getElementById("checkbox" + id).checked) {
      let img = document.getElementById(imgId);
      img.src = "data:image/png;charset=utf-8;base64," + data;
    }
  };

  this.reset = function () {
    // reset logic goes here
  };
}
