function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

$(function() {
    $('a#save_svg').bind('click', function() {
        $.post($SCRIPT_ROOT + '/save_file', {
            file_contents: $('#mermaid_code').html(), 
            unique_id: readCookie('mermaid_unique_id'), 
            file: 'svg_render.svg'
        }, function(data) {
            console.log(data);
            if (!data.result) {
                alert("SVG Saving Failed ⚠️⚠️");
            } else {
                alert("SVG Saved!");
            }
        }, 'json')
        .fail(function() {
            alert("Error: Unable to save SVG.");
        });
        
        return false;
    });
});
