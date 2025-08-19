function searchSpeeches() {
    const query = document.getElementById('searchQuery').value;
    const k = 20;
    $.ajax({
        url: '/search_speeches',
        method: 'POST',
        data: { query: query, k: k },
        success: function(response) {
            $('#results').html(response);
        },
        error: function() {
            $('#results').html('<p>An error occurred while searching.</p>');
        }
    });
}





