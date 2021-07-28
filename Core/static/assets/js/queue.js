function appendDataAsTable(data){

    tbl = document.getElementById('sub-link-table').getElementsByTagName('tbody')[0];
    tbl.innerHTML = '';
    row_length = tbl.rows.length;
    queue = data.queue;

    for (let i = 0; i < queue.length; i++) {
        var rowData = queue[i];
        var myHtmlContent = "<td>" + rowData.id + "</td>"
        + "<td><a href=\"" + rowData.sub_url + "\">" + rowData.sub_url + "</a></td>"
        + "<td>" + rowData.master_url + "</td>"
        + "<td>" + rowData.content + "</td>"
        + "<td>" + (rowData.completed ? 'True' : 'False') + "</td>";

        var newRow = tbl.insertRow(row_length);
        newRow.innerHTML = myHtmlContent;
    }
}

function fetchQueue() {
    current = window.location.href;

    link = current + 'queue/';

    csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    $.ajax({
        type: 'GET',
        headers: {'X-CSRFToken': csrf_token},
        url: link,
        crossDomain: true,
        data: null,
        success: function(responseData, textStatus, jqXHR) {
            appendDataAsTable(responseData);
        },
        error: function (responseData, textStatus, errorThrown) {
            alert('Unable to update the table... \nTry reconnecting or refreshing the page!');
            clearInterval(window.custom_interval);
        }
    });
}

window.addEventListener('load', function () {
    // Your document is loaded.
    var fetchInterval = 5000; // 5 seconds.

    // Invoke the request every 5 seconds.
    window.custom_interval = setInterval(fetchQueue, fetchInterval);
});

function start_crawler(){
    current = window.location.href;

    link = current + 'start_queue/';

    csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    packet_data = {
        'csrf_token': csrf_token
    }

    $.ajax({
        type: 'GET',
        headers: {'X-CSRFToken': csrf_token},
        url: link,
        crossDomain: true,
        data: packet_data,
        success: function(responseData, textStatus, jqXHR) {
            alert(responseData.message);
        },
        error: function (responseData, textStatus, errorThrown) {
            alert('Unable to start crawler... Please check you internet connection or try again!');
        }
    });
}

function stop_crawler(){
    current = window.location.href;

    link = current + 'stop_queue/';

    csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    alert('Crawler Service will be stopped after it process the current link... Please wait for confirmation alert!');

    $.ajax({
        type: 'GET',
        headers: {'X-CSRFToken': csrf_token},
        url: link,
        crossDomain: true,
        data: null,
        success: function(responseData, textStatus, jqXHR) {
            alert(responseData.message);
        },
        error: function (responseData, textStatus, errorThrown) {
            alert('Unable to stop crawler... Please check you internet connection or try again!');
        }
    });
}