$(document).ready(function() {
    $('#results').html('<p>Topics are being extracted...</p>');
    
    $.ajax({
        url: '/extract_topics_action',
        method: 'POST',
        success: function(response) {
            $('#results').html(response);
        },
        error: function() {
            $('#results').html('<p>An error occurred while extracting topics.</p>');
        }
    });
});