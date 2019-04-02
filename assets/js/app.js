var leaflet = require('leaflet'),
    tabs = require('./components/tabs'),
    validators = require('./components/validators');

// Overide leaflet icon path
leaflet.Icon.Default.imagePath = '/static/img/leaflet/';

/**
 * WHOIS search box
 */
if(document.querySelector(".whois-search-box") != null) {
    var form = document.querySelector(".whois-search-box form");
    var search = document.querySelector(".whois-search-box form input#whois-search-input");
    var button = document.querySelector(".whois-search-box form button#whois-search-button");

    // Add an event to search input
    search.addEventListener("input", () => {
        button.firstChild.textContent = "Search " + search.value;

        // Check if the resource is valid
        if(validators.valid_whois_resource(search.value)) button.classList.remove('.siimple-btn--disabled');
        else button.classList.remove('.siimple-btn--disabled');
    });


    // Add an event to rewrite the action URI on submit
    form.addEventListener("submit", e => {
        e.preventDefault();

        if(validators.valid_whois_resource(search.value)) {
            form.action = "/whois/" + search.value;
            form.submit();
        } else {
            // TODO: Show a error on the front.
            console.error("Ressource not valid.");
        }
    })
}

if(document.querySelector("#whois-resource-page") != null) {
    tabs("#whois-tabs"); // Setup a tabs

    // Setup the map if is available
    if(document.querySelector("#geo") != null) {
        var map = spawn_leaflet("geo-map", resource_pos);
        leaflet.marker(resource_pos).addTo(map); // Add marker
    }
}


// Generate leaflet if available
/**
 *
 * @param {*} selector
 * @param {*} setpos
 */
function spawn_leaflet(selector, setpos) {
    var map = leaflet.map(selector).setView(setpos, 9);

    leaflet.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'replaced-mapbox-access-token' // The string is replaced by Gulp on JS bundle process. DON'T EDIT THAT!
    }).addTo(map);

    return map;
}

window.browserify = { tabs, validators, spawn_leaflet };