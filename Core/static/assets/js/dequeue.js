function extract_image_names(images){
    var names = [];
    for(let i = 0; i < images.length; i++){
        names.push(images[i].image_name);
    }
    return names;
}

function extract_documents_names(documents){
    var names = [];
    for(let i = 0; i < documents.length; i++){
        names.push(documents[i].file);
    }
    return names;
}

function create_list_tag(names){
    var tag = "<ul>";
    for(let i = 0; i < names.length; i++){
        var li = "<li>" + names[i] + "</li>";
        tag += li;
    }

    tag += "</ul>";
    return tag;
}

function appendDataAsTable(data){

    tbl = document.getElementById('sub-link-table').getElementsByTagName('tbody')[0];
    tbl.innerHTML = '';
    row_length = tbl.rows.length;
    dequeue = data.dequeue;

    for (let i = 0; i < dequeue.length; i++) {
        var rowData = dequeue[i];

        var myHtmlContent = "<td>" + rowData.id + "</td>"
        + "<td><a href=\"" + rowData.sub_url + "\">" + rowData.sub_url + "</a></td>"
        + "<td>" + rowData.master_url + "</td>"
        + "<td>" + rowData.content.id + "</td>"
        + "<td>" + rowData.content.text + "</td>"
        + "<td>" + (rowData.completed ? 'True' : 'False') + "</td>"
        + "<td>" + create_list_tag(extract_image_names(rowData.images)) + "</td>"
        + "<td>" + create_list_tag(extract_documents_names(rowData.documents)) + "</td>";

        var newRow = tbl.insertRow(row_length);
        newRow.innerHTML = myHtmlContent;
    }
}

function fetchQueue() {
    current = window.location.href;

    link = current + 'dequeue/';

    csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    $.ajax({
        type: 'GET',
        headers: {'X-CSRFToken': csrf_token},
        url: link,
        crossDomain: true,
        data: null,
        success: function(responseData, textStatus, jqXHR) {
            console.log(responseData);
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