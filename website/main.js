var mapboxAccessToken =
  "pk.eyJ1IjoiZHVzdGlubWljaGVscyIsImEiOiJja2s4YzgwYnUwbTVuMnBvMHBrYmNsNGo1In0.fiSyjORBCNSbGbTHPKuM3A";
var map = L.map("map").setView([37.8, -96], 4);

L.tileLayer(
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=" +
    mapboxAccessToken,
  {
    id: "mapbox/light-v9",
    attribution: "This",
    tileSize: 512,
    zoomOffset: -1,
  }
).addTo(map);

L.geoJson(geoData).addTo(map);
