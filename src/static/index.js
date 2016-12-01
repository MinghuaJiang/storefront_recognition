var panorama;
$("#search_loc").click(function() {
    var txt = $("#location").val();
    var location = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ txt +'&key=AIzaSyC5BG3tKK5d_5c5g94vRqQi3rVT5ox1mZw'
    $.post(location).done(function(data){
        new_lat = data.results[0].geometry.location.lat
        new_lng = data.results[0].geometry.location.lng
        new_pos = {lat: new_lat, lng: new_lng};
        panorama.setPosition(new_pos);
    });
});

$("#recognize_btn").click(function() {
    var positionCell = document.getElementById('position-cell');
    var txt = positionCell.firstChild.nodeValue;
    var regExp = /\((.+),(.+)\)/;
    var matches = regExp.exec(txt);
    var lat = matches[1];
    var lng = matches[2];
    $.post('/business_v2', {latitude:lat, longitude:lng}).done(function(data) {
        json = JSON.parse(data)
        var nameCell = document.getElementById('name-cell');
        nameCell.firstChild.nodeValue = json["name"]
        var addressCell = document.getElementById('address-cell');
        addressCell.firstChild.nodeValue = json["address"]
        var categoryCell = document.getElementById('category-cell');
        categoryCell.firstChild.nodeValue = json["category"]
        var ratingCell = document.getElementById('rating-cell');
        ratingCell.firstChild.nodeValue = json["rating"]
        var phoneCell = document.getElementById('phone-cell');
        phoneCell.firstChild.nodeValue = json["phone"]

    });
});

function initPano() {
    panorama = new google.maps.StreetViewPanorama(
        document.getElementById('pano'), {
        position: {lat: 38.035440578, lng: -78.5010249},
        visible: true
    });
    panorama.addListener('position_changed', function() {
        var positionCell = document.getElementById('position-cell');
        positionCell.firstChild.nodeValue = panorama.getPosition() + '';
        var nameCell = document.getElementById('name-cell');
        nameCell.firstChild.nodeValue = ''
        var addressCell = document.getElementById('address-cell');
        addressCell.firstChild.nodeValue = ''
        var categoryCell = document.getElementById('category-cell');
        categoryCell.firstChild.nodeValue = ''
        var ratingCell = document.getElementById('rating-cell');
        ratingCell.firstChild.nodeValue = ''
        var phoneCell = document.getElementById('phone-cell');
        phoneCell.firstChild.nodeValue = ''
    });
    panorama.addListener('pov_changed', function() {
        var nameCell = document.getElementById('name-cell');
        nameCell.firstChild.nodeValue = ''
        var addressCell = document.getElementById('address-cell');
        addressCell.firstChild.nodeValue = ''
        var categoryCell = document.getElementById('category-cell');
        categoryCell.firstChild.nodeValue = ''
        var ratingCell = document.getElementById('rating-cell');
        ratingCell.firstChild.nodeValue = ''
        var phoneCell = document.getElementById('phone-cell');
        phoneCell.firstChild.nodeValue = ''
  });
}