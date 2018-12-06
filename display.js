
(function(window, document, undefined) {
  var APIKEY = 'AIzaSyB406GqVRFbEF_fuQYOlC4IisN3CZkjxLM';

  var COLORS = ['#00f', '#f00']

  var map;

  function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
      center: { lat:  32.716682, lng: -117.159450 },
      zoom: 15
    });

    origins = window.origins;
    for (var i = 0; i < origins.length; i++) {
        new google.maps.Marker({ map: map, position: origins[i], icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 3
          } })
    }
    cells = window.cells;
    for (var i = 0; i < cells.length; i++) {
        new google.maps.Polyline({ map: map, path: cells[i], strokeColor: COLORS[0] });
    }

  };

  var script = document.createElement('script');
  var tag = document.getElementsByTagName('script')[0];
  script.src = 'https://maps.googleapis.com/maps/api/js?key=' + APIKEY + '&callback=initMap'
  script.type = 'text/javascript';

  window.initMap = initMap;

  tag.parentNode.insertBefore(script, tag);

})(this, document)
