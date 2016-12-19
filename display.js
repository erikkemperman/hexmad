
(function(window, document, undefined) {
  var APIKEY = 'AIzaSyB406GqVRFbEF_fuQYOlC4IisN3CZkjxLM';

  var COLORS = ['#00f', '#f00']

  var RADIUS = 6371;

  var K = 24;

  function radians(degrees) { return degrees * Math.PI / 180; }
  function degrees(radians) { return radians * 180 / Math.PI; }

  function radians2(latlon) {
    return {
        lat: radians(latlon.lat),
        lng: radians(latlon.lng)
    };
  }

  function degrees2(latlon) {
    return {
        lat: degrees(latlon.lat),
        lng: degrees(latlon.lng)
    };
  }

  var cos = Math.cos, sin = Math.sin, acos = Math.acos, asin = Math.asin, atan2 = Math.atan2,
      abs = Math.abs, sqrt = Math.sqrt, min = Math.min, max = Math.max;

  var lat1 = radians(51.920992), lon1 = radians(4.480494),  // Rotterdam
      //lat2 = radians(-33.854685), lon2 = radians(151.213543);  // Sydney
      // lat2 = radians(52.372384), lon2 = radians(4.897050);  // Amsterdam
      // lat2 = radians(73.496245), lon2 = radians(80.696645);  // Krasnoyarskiy
      lat2 = radians(-36.874737), lon2 = radians(174.788966);  // Auckland


  var map;

  function initMap() {
    var seq = interpol2(lat1, lon1, lat2, lon2, K);

    for (i = 1; i < seq.length; i++) {
      console.log('dist ' + i + ": " + distance(seq[i-1].lat, seq[i-1].lng, seq[i].lat, seq[i].lng) * RADIUS);
    }

    var mid = Math.floor(seq.length / 2);

    console.log('seq', seq);

    map = new google.maps.Map(document.getElementById('map'), {
      center: degrees2(seq[mid]),
      zoom: 10
    });

    var line = new google.maps.Polyline({ map: map, path: seq.map(degrees2), strokeColor: COLORS[0] });

    for (var i = 0; i < seq.length; i++) {
        new google.maps.Marker({ map: map, position: degrees2(seq[i]) })
    }

  };

  function distance(lat1, lon1, lat2, lon2) {
    var c1 = cos(lat1);
    var c2 = cos(lat2);
    var s1 = sin(lat1);
    var s2 = sin(lat2);
    var h1 = sin(0.5 * (lat2 - lat1));
    var h2 = sin(0.5 * (lon2 - lon1));

    return 2 * asin(sqrt(h1 * h1 + h2 * h2 * c1 * c2));
  }

  function distance2(lat1, lon1, lat2, lon2) {
    var c1 = cos(lat1);
    var c2 = cos(lat2);
    var s1 = sin(lat1);
    var s2 = sin(lat2);

    return acos(s1 * s2 + c1 * c2 * cos(lon2 - lon1));
  }

  function interpol(lat1, lon1, lat2, lon2, k) {
    var epsilon = distance(lat1, lon1, lat2, lon2);
    console.log((epsilon * RADIUS) + ' KM');
    console.log((distance2(lat1, lon1, lat2, lon2) * RADIUS) + ' KM');

    var result = [{ lat: lat1, lng: lon1 }];

    lat1 = Math.PI/2 - lat1;
    lat2 = Math.PI/2 - lat2;

    var c1 = cos(lat1);
    var c2 = cos(lat2);
    var s1 = sin(lat1);
    var s2 = sin(lat2);

    var dlon = sin(abs(lon2 - lon1)) / sin(epsilon);

    for (i = 1; i < k; i++) {
      var fraction = i / k;
      var delta = epsilon * fraction;
    
      var cd = cos(delta);
      var sd = sin(delta);
      var beta = asin(s2 * dlon);
      var latx = acos(c1 * cd + s1 * sd * cos(beta));
      console.log(latx);

      var lont = asin(sd * s2 * dlon / sin(latx));
      var lonx = min(lon1, lon2) + lont;
      console.log(lonx, " (? ", lont);
    
      latx = Math.PI/2 - latx;
      console.log('=>', degrees(latx), degrees(lonx));

      result.push({ lat: latx, lng: lonx });
    }


    lat1 = Math.PI/2 - lat1;
    lat2 = Math.PI/2 - lat2;
    result.push({ lat: lat2, lng: lon2 });
    return result;
  }

  function interpol2(lat1, lon1, lat2, lon2, k) {
    var epsilon = distance(lat1, lon1, lat2, lon2);
    console.log((epsilon * RADIUS) + ' KM');
    console.log((distance2(lat1, lon1, lat2, lon2) * RADIUS) + ' KM');

    var result = [{ lat: lat1, lng: lon1 }];

    var c1 = cos(lat1);
    var c2 = cos(lat2);
    var s1 = sin(lat1);
    var s2 = sin(lat2);

    for (i = 1; i < k; i++) {
      var fraction = i / k;
      var a = sin((1 - fraction) * epsilon) / sin(epsilon);
      var b = sin(fraction * epsilon) / sin(epsilon);
      var x = a * c1 * cos(lon1) + b * c2 * cos(lon2);
      var y = a * c1 * sin(lon1) + b * c2 * sin(lon2);
      var z = a * s1 + b * s2

      result.push({
        lat: atan2(z, sqrt(x * x + y * y)),
        lng: atan2(y, x)
      });
    }


    result.push({ lat: lat2, lng: lon2 });
    return result;
  }

  var script = document.createElement('script');
  var tag = document.getElementsByTagName('script')[0];
  script.src = 'https://maps.googleapis.com/maps/api/js?key=' + APIKEY + '&callback=initMap'
  script.type = 'text/javascript';

  window.initMap = initMap;

  tag.parentNode.insertBefore(script, tag);

})(this, document)
