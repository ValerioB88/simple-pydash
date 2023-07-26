var textInfoId = 0;

function TextInfo(width, height, replace, use_scroll, location) {
  let preElement = document.createElement("pre");
  preElement.id = "textinfo" + textInfoId++;
  preElement.style.width = width;
  preElement.style.height = height;
  preElement.style.overflow = use_scroll ? "scroll" : "visible";
  preElement.style.display = "flex";
  preElement.style.flexDirection = "column-reverse";

  let locationElement = document.getElementById(location + "Col");
  locationElement.appendChild(preElement);

  this.render = function (data) {
    if (replace) {
      preElement.innerText = data;
    } else {
      preElement.innerText += data;
    }
  };

  this.reset = function () {
    preElement.innerText = "";
  };
}
