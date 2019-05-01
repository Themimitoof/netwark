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

if(document.querySelector(".search-box") != null) {
    tabs("#macoui-tabs"); // Setup a tabs

    document.querySelectorAll("form").forEach(form => {
        var inputs = form.getElementsByTagName("input");


        form.addEventListener("submit", e => {
            e.preventDefault();

            console.log("Hello buddy")

            var url = new URL(location.origin + "/api/v1/mac-oui");

            if(form.id == "find-form") {
                var params = [];

                inputs.forEach(el => {
                    if(el.value != "")
                        params.push[el.getAttribute("name"), el.value];
                });

                url.search = new URLSearchParams(params);
            }

            fetch(url).then(resp => {
                resp.json().then(json => {
                    var result_div = document.querySelector(".mac-oui-return");
                    var result_body = document.querySelector(".mac-oui-return .siimple-card-body");

                    // Hide the result div and cleanup the actual content
                    result_div.classList.remove("active");
                    result_body.innerHTML = "";

                    if(Array.isArray(json)) {
                        json.forEach(el => {
                            var tip = document.createElement("div");
                            tip.classList.add(...["siimple-tip", "siimple-tip--primary"]);
                            var list = document.createElement("ul");
                            list.classList.add("no-style");

                            var node = document.createElement("li");
                            node.innerText = `Assignment: ${el.assignment}`;
                            list.appendChild(node);

                            node = document.createElement("li");
                            node.innerText = `Organization: ${el.orgname}`;
                            list.appendChild(node);

                            node = document.createElement("li");
                            node.innerText = `Organization address: ${el.orgaddr}`;
                            list.appendChild(node);

                            tip.appendChild(list);
                            result_body.appendChild(tip);
                        });
                    } else {
                        var tip = document.createElement("div");
                        tip.classList.add(...["siimple-tip", "siimple-tip--primary"]);
                        var list = document.createElement("ul");
                        list.classList.add("no-style");

                        var node = document.createElement("li");
                        node.innerText = `Assignment: ${el.assignment}`;
                        list.appendChild(node);

                        node = document.createElement("li");
                        node.innerText = `Organization: ${el.orgname}`;
                        list.appendChild(node);

                        node = document.createElement("li");
                        node.innerText = `Organization address: ${el.orgaddr}`;
                        list.appendChild(node);

                        tip.appendChild(list);
                        result_body.appendChild(tip);
                    }

                    // Show the result div with the new results
                    result_div.classList.add("active");
                });

            }).catch(err => console.error(err));
        });
    });
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