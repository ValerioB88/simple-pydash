var TextInfo = function(id, width, height, replace, use_scroll,location) {
    var text_tag = "<pre id=" + id + " style='width:" + width + ";height:" + height +";overflow:" + (use_scroll?'scroll':'visible') + ";display:flex;flex-direction:column-reverse'></pre>";
    location = location + 'Col'
    $("#" + location).append(text_tag);

    this.render = function(data) {
        if (replace)
            document.getElementById(id).innerText = data;
        else
            document.getElementById(id).innerText += data;
    }

    this.reset = function(data) {
        document.getElementById(id).innerText = '';
    };
}