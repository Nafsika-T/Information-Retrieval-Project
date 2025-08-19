$(document).ready(function() {
    $("#memberInput").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/autocomplete_entity",
                dataType: "json",
                data: {
                    q: request.term,
                    type: "member"
                },
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 2, 
    });
});

function entity_recognition() {
    const member = document.getElementById('memberInput').value;
    fetch(`http://127.0.0.1:5000/entity_recognition`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ member: member })
    })
    .then(response => response.json())
    .then(data => {
        let resultsDiv = document.getElementById('results');
        if (data.image_path) {
            resultsDiv.innerHTML = `<img src="${data.image_path}" alt="NER Image for ${member}" class="img-fluid" style="max-width: 70%;">`;
        } else {
            resultsDiv.innerHTML = `<p>${data.message}</p>`;
        }
    });
}