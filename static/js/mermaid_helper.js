$(function() {
    $('a#delete_mermaid').bind('click', function() {
        $.ajax({
            url: $SCRIPT_ROOT + '/delete_mermaid',
            type: 'DELETE',
            data: {
                'unique_id': $('td#unique_id').html()
            }, 
            success: function(result){
                if(result.delete_done){
                    window.location.href = result.redirect_location; 
                    alert('Deleted Mermaid');
                }else{
                    alert("Error: Unable to Delete");
                }
            }, 
            error: function(){
                alert("Error: Unable to Delete");
            }
        })
        return false;
    });
});

$(function() {
    $('a#open_codefile').bind('click', function() {
        $.ajax({
            url: $SCRIPT_ROOT + '/get_file',
            type: 'POST',
            data: {
                'unique_id': $('td#unique_id').html(), 
                'file': 'codefile.txt'
            }, 
            success: function(data){
                if(data.result){
                    setTextFromFile(data.file_contents);
                }else{
                    alert('Could not open the codefile')  ;                 
                }
            }, 
            error: function(){
                alert("Error: Unable to fetch file");
            }
        })
        return false;
    });
});

$(function() {
    $('a#codearea_save').bind('click', function() {
        $.ajax({
            url: $SCRIPT_ROOT + '/save_file',
            type: 'POST',
            data: {
                'unique_id': $('td#unique_id').html(), 
                'file_contents': getTextFromQuill(quill), 
                'file': 'codefile.txt'
            }, 
            success: function(data){
                if(data.result){
                    $.ajax({
                        url: $SCRIPT_ROOT + '/process_codefile',
                        type: 'POST',
                        data: {
                            'unique_id': $('td#unique_id').html(), 
                        }, 
                        success: function(data){
                            if(data.result){
                                alert('Code File Saved successfully and Mermaid file created'); 
                            }else{
                                alert('Code File Saved but Mermaid File not generated');                    
                            }
                        }
                    })
                }else{
                    alert('Could not save file');                    
                }
            }, 
            error: function(){
                alert("Error: Unable to save file");
            }
        })
        return false;
    });
});

