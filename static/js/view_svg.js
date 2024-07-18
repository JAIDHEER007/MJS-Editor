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

$(window).load(function() {
    if(readCookie('svg_exists') == 'True'){
        $.ajax({
            url: $SCRIPT_ROOT + '/get_file',
            type: 'POST',
            data: {
                'unique_id': readCookie('mermaid_unique_id'), 
                'file': 'svg_render.svg'
            }, 
            success: function(data){
                if(data.result){
                    var $svg = $(data.file_contents[0]); 
                    $svg.removeAttr('xlmns:a'); 
                    $('#svg_image').append($svg);
                }else{
                    alert('Could not open the SVG File');                 
                }
            }, 
            error: function(){
                alert("Error: Unable to fetch file");
            }
        })
    }else{
        $.ajax({
            url: $SCRIPT_ROOT + '/static/imgs/' + 'no_image.svg',
            type: 'GET',
            success: function(data){
                var $svg = $(data.documentElement); 
                $svg.removeAttr('xlmns:a'); 
                $('#svg_image').append($svg);
            }, 
            error: function (request, status, error) {
                alert(error);
            }
        })
    }
    return false;
});