$(document).ready(function() {
    $('#similaritiesForm').on('submit', function() {
        $('#loadingSpinner1').show();
        
        var kValue = $('#kValue').val();
        $(this).append('<input type="hidden" name="k" value="' + kValue + '">');
    });

    $('#memberSimilaritiesForm').on('submit', function() {
        $('#loadingSpinner2').show();
        
        var kValue = $('#kValue').val();
        $(this).append('<input type="hidden" name="k" value="' + kValue + '">');
    });

    $('#memberName').on('keyup', function() {
        let query = $(this).val();
        
        if (query.length >= 2) {
            $.ajax({
                url: '/autocomplete',
                method: 'GET',
                data: { q: query },
                success: function(data) {
                    $('#suggestions').empty();
                    if (data.length > 0) {
                        data.forEach(function(name) {
                            $('#suggestions').append('<li class="list-group-item">' + name + '</li>');
                        });
                    }
                }
            });
        } else {
            $('#suggestions').empty();
        }
    });

    $(document).on('click', '#suggestions li', function() {
        $('#memberName').val($(this).text());
        $('#suggestions').empty();
    });
});
