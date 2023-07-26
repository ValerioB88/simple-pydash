var injectHtmlId = 0;

function InjectHTML(location) {
    let div = document.createElement('div');
    div.style.width = '800px';
    div.style.height = '600px';
    div.id = 'inject_html' + injectHtmlId++;
    
    let locationElement = document.getElementById(location + 'Col');
    locationElement.appendChild(div);
    
    this.render = function(newHtml) {
        if (newHtml !== null) {
            div.innerHTML = newHtml;
        }
    };

    this.reset = function() {
        div.innerHTML = '';
    };
}
