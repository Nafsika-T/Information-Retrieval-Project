$(document).ready(function() {


    $('#entity').on('keyup', function() {
        let query = $(this).val();
        let type = $('#keywordType').val();
        
        if (query.length >= 1) {
            $.ajax({
                url: '/autocomplete_entity',
                method: 'GET',
                data: { q: query, type: type },
                success: function(data) {
                    $('#suggestions').empty();
                    if (data.length > 0) {
                        data.forEach(function(item) {
                            $('#suggestions').append('<li class="list-group-item">' + item + '</li>');
                        });
                    }
                }
            });
        } else {
            $('#suggestions').empty();
        }
    });

    $(document).on('click', '#suggestions li', function() {
        $('#entity').val($(this).text());
        $('#suggestions').empty();
    });

    $('#keywordForm').on('submit', function() {
        $('#loadingSpinner').show();
    });
});