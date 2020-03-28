// var map;
// var markers = [];
// var infoWindows = [];
// function initMap() {
//     map = new google.maps.Map(document.getElementById('map'), {
//         center: {lat: 37.7790262, lng: -122.4199061},
//         zoom: 13
//     });
// }


// start $(function(){})
window.onload = function() {

// var locationTemplate = document.getElementById('locationtemplate');

// search elements
var searchForm = $('form#search')
var searchThrobber = $('#search-throbber');
var searchButton = $('#search-button');

// search results elements
var results = $('#results');
var resultsEmpty = $('#results-empty');
var resultsError = $('#results-error');

// modal element
var locationModal = $('#locationModal');

// my locations
var myLocations = $('#my-locations');


function createLocationResultElement(data){

    var locationResultTemplate = $('#location-result-template');
    var clone = locationResultTemplate.clone().contents();
    clone.find('.name').text(data.name);
    clone.find('.address').text(data.formatted_address);
    clone.find('.place_id').val(data.place_id);
    return clone;
}

function createLocationElement(data) {
    var locationTemplate = $('#location-template');
    var clone = locationTemplate.clone().contents();
    clone.find('.name').text(data.name)
    clone.find('.address').text(data.address)
    return clone;
}

function clearResults(){
    results.html('');
}

function onLoadResults(data){
    hideSearchProgress();
    clearResults();

    data.candidates.map(createLocationResultElement).forEach(function(locationElement){
        results.append(locationElement);
    });
}

function onLoadResultsError(data){
    resultsError.show();
    hideSearchProgress();
}

function getJsonResponse(response){
    return response.json().then(onLoadResults);
}

function showSearchProgress(){
    searchButton.hide();
    searchThrobber.show();
}

function hideSearchProgress(){
    searchButton.show();
    searchThrobber.hide();
}

function executeSearch(url){
    showSearchProgress();

    fetch(url)
        .then(getJsonResponse);
}


searchForm.off('submit').on('submit', function(e){
    e.preventDefault();

    var form = $(e.target);
    var query = form.find('input#query').val();
    if (query && query.length < 3){
        return;
    }

    var params = {'q': query };
    var latitude = Cookies.get('latitude');
    var longitude = Cookies.get('longitude');
    if (latitude && longitude) {
        params['latitude'] = latitude;
        params['longitude'] = longitude;
    }
    var url = form.attr('action') + '?' + $.param(params);
    executeSearch(url);
});


function onLocationLoadSuccess(data) {
    data.locations.map(createLocationElement).forEach(function(locationElement){
        myLocations.append(locationElement);
    })
}


function onLocationLoadError(data) {
    console.error(data);
}


results.off('submit').on('submit', '.location-result form', function(e){
    e.preventDefault();

    var form = $(e.target);
    var url = form.attr('action');
    var method = form.attr('method');
    var params = {
        'place_id': form.find('input.place_id').val(),
        'csrfmiddlewaretoken': form.find('[name="csrfmiddlewaretoken"]').val()
    };
    $.ajax(url, {
        data: params,
        method: method,
        success: onLocationLoadSuccess,
        error: onLocationLoadError
    });
});


function onLocationSuccess(position){
    Cookies.set('latitude', position.coords.latitude);
    Cookies.set('longitude', position.coords.longitude);
    Cookies.set('location-checked', new Date().toString());
}

function onLocationError(){
    console.info('geolocation denied.');
    Cookies.set('location-checked', new Date().toString());
}

function checkLocation(){
    if (navigator && 'geolocation' in navigator){
        navigator.geolocation.getCurrentPosition(onLocationSuccess, onLocationError);
    }
}

locationModal.on('hidden.bs.modal', function (e) {
    checkLocation();
});

if (!Cookies.get('location-checked')){
    if (navigator && navigator.geolocation){
        locationModal.modal();
    }
}



$(document).ready(function(){
    $.ajax('/locations/', 
        {
            success: onLocationLoadSuccess
        }
    );

})

// end $(function(){})
}