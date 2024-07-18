const toolbarOptions = [
    { size : ['large']}, 
    [{ 'save': 'Save' }] 
]; 

const quill = new Quill('#editor', {
    theme: 'snow', 
    modules : {
        toolbar : toolbarOptions
    }
});
quill.disable(); 
quill.format('size', 'large'); 

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

const setTextFromFile = function (textFromFile){
    // Create a Delta object with the text and size format
    var delta = textFromFile.map(line => ({
        insert: line.replace(/\t/g, '\t\t\t'),
        attributes: { size: 'large' }
    }));

    // Use setContents to populate the editor with the Delta object
    quill.setContents(delta);
}

$(window).load(function() {
    $.ajax({
        url: $SCRIPT_ROOT + '/get_file',
        type: 'POST',
        data: {
            'unique_id': readCookie('mermaid_unique_id'), 
            'file': 'mermaid_code.txt'
        }, 
        success: function(data){
            if(data.result){
                setTextFromFile(data.file_contents);
            }else{
                alert('Could not open the codefile');                 
            }
        }, 
        error: function(){
            alert("Error: Unable to fetch file");
        }
    })
    return false;
});
