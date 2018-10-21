var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
  google.maps.event.trigger(map, 'resize');
}

function addPoint(lon, lat) {

}
// <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB9QanEBVf2jJZH1-0uTvHXf39Su026rEY&callback=initMap"
