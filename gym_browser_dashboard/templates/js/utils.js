
var add_checkbox = function(id, label, elementid, start_checked=true, classtype='row')
{
	// classtype row or container
	let c = '<div class=' + classtype + '><div class="input-group input-group-lg">\n' +
		'                    <label class="label label-primary" style="margin-right: 15px">' + label + '</label>\n' +
		'                    <input id="' + id  + '"' + (start_checked? ' checked':'') + '  type="checkbox"/>\n' +
		'\n' +
		'                </div></div>'
	$("#" + elementid).append($(c)[0])

	return c

}