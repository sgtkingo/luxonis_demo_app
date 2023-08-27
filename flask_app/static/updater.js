$( document ).ready(function() {
    let timer;
    timer = setInterval(updateProgress, 1000);  // Update every 1 second

    function updateProgress() {
        $.ajax({
            url: '/api/get_progress',  // Flask route to fetch progress
            type: 'GET',
            success: function(response) {
                $('#progress-value').text(response.progress_value + '%');
                $('#progress-status').text(response.progress_status);

                console.log('progress:'+ response.progress_value);
                console.log('status:'+ response.progress_status);

                if (response.progress_status === "Status.DONE"){
                    clearInterval(timer);
                    $("#progress-container").hide();
                    fetchData();
                }
            }
        })
    }    

    function fetchData() {
        $.ajax({
            url: '/api/get_data',  // Flask route to fetch data
            type: 'GET',
            success: function(response) {
                console.log(response.data)
            }
        });
        $("#table-container").show();
    }      
});

