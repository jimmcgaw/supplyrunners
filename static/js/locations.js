var map;
var markers = [];
var infoWindows = [];
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.7790262, lng: -122.4199061},
        zoom: 13
    });
}

const locationTemplate = document.getElementById('locationtemplate');
const results = document.getElementById('results');


function createPlaceElement(data){
    console.log(data)
    var clone = locationTemplate.content.cloneNode(true);
    clone.querySelectorAll(".name")[0].textContent = data.name;
    clone.querySelectorAll(".address")[0].textContent = data.formatted_address;
    clone.querySelectorAll(".place_id")[0].textContent = data.place_id;
    return clone;
}

function onLoadResults(data){
    console.info(data.candidates);

    data.candidates.map(createPlaceElement).forEach(function(locationElement){
        console.log(locationElement)
        results.appendChild(locationElement);
    })
}

function getJsonResponse(response){
    return response.json();
}

$(function() {
    $('form#search').submit(function(e){
        e.preventDefault();
        var form = $(e.target);
        var query = form.find('input#query').val();
        var url = form.attr('action') + '?' + $.param({'q': query })

        fetch(url)
            .then(getJsonResponse)
            .then(onLoadResults);
    });
});