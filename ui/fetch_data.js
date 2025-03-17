$(document).ready(function() {
    $("#fetch_data").click(function() {
        $.ajax({
            url: 'mitre_work/setup_environment.py',
            type: 'GET',
            success: function(data) {
                $("#output").html(data);
            },
            error: function(error) {
                $("#output").html('Error: ' + error.responseText);
            }
        });
    });
});