const toolbarOptions = [
    { size : ['large']}
]; 

const quill = new Quill('#editor', {
    theme: 'snow', 
    modules : {
        toolbar : toolbarOptions
    }
});
quill.format('size', 'large'); 

const setTextFromFile = function (textFromFile){
    // Create a Delta object with the text and size format
    var delta = textFromFile.map(line => ({
        insert: line.replace(/\t/g, '\t\t\t'),
        attributes: { size: 'large' }
    }));

    // Use setContents to populate the editor with the Delta object
    quill.setContents(delta);
}

const getTextFromQuill = function (){
    text = quill.getText(); 
    return text.replace(/\t{3}/g, '\t'); 
}

quill.root.addEventListener("keydown", (event) => {
    if (event.key === 'Backspace' || event.key === 'Delete') {
        // If the key is Backspace or Delete, do not apply the large size format
        return;
    } else if (event.key === 'Tab' ) {
        event.preventDefault(); // Prevent the default tab behavior

        // Get the current selection range
        const range = quill.getSelection(true);

        // Insert two tab characters (\t\t) at the current cursor position
        quill.insertText(range.index, '\t\t', { size: 'large' });

        // Move the cursor to the position after the inserted text
        quill.setSelection(range.index + 2);
    } else {
        quill.format('size', 'large');
    }
});