var map;
var markers = [];
var infoWindows = [];
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.7790262, lng: -122.4199061},
        zoom: 13
    });
}

function onLoadResults(places){
    console.info(places)
}

$('form#search').submit(function(e){
    e.preventDefault();
    var form = $(e.target);
    var query = form.find('input#query').val();
    var url = form.attr('action') + $.param({'q': query })

    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then(onLoadResults);
});