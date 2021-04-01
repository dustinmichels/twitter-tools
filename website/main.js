/*
 * Based on: https://leafletjs.com/examples/choropleth/
 */

var map = L.map("map").setView([30, 10], 2);

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

function getColor(d) {
  return d > 1000
    ? "#800026"
    : d > 500
    ? "#BD0026"
    : d > 100
    ? "#E31A1C"
    : d > 50
    ? "#FC4E2A"
    : d > 30
    ? "#FD8D3C"
    : d > 10
    ? "#FEB24C"
    : d > 1
    ? "#FED976"
    : "#636363";
}

function style(feature) {
  return {
    fillColor: getColor(feature.properties.count),
    weight: 2,
    opacity: 1,
    color: "white",
    dashArray: "3",
    fillOpacity: 0.7,
  };
}

// ------ POPUP -----
var info = L.control();

info.onAdd = function (map) {
  this._div = L.DomUtil.create("div", "info"); // create a div with a class "info"
  this.update();
  return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
  this._div.innerHTML =
    "<h4>Friend Count</h4>" +
    (props
      ? "<b>" + props.name + "</b><br />" + props.count + " people"
      : "Hover over a country");
};

info.addTo(map);

// ----- INTERACTION -----

var geojson;

function highlightFeature(e) {
  var layer = e.target;

  layer.setStyle({
    weight: 5,
    color: "#666",
    dashArray: "",
    fillOpacity: 0.7,
  });

  if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
    layer.bringToFront();
  }

  info.update(layer.feature.properties);
}

function resetHighlight(e) {
  geojson.resetStyle(e.target);
  info.update();
}

function zoomToFeature(e) {
  map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click: zoomToFeature,
  });
}

// ----- INIT MAP -----

geojson = L.geoJson(geoData, {
  style: style,
  onEachFeature: onEachFeature,
}).addTo(map);
