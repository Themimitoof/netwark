var leaflet = require('leaflet'),
    tabs = require('./components/tabs'),
    validators = require('./components/validators');

// Overide leaflet icon path
leaflet.Icon.Default.imagePath = '/static/img/leaflet/';

/**
 * WHOIS search box
 */
if(document.querySelector(".search-box#whois-search-box") != null) {
    var form = document.querySelector(".search-box form");
    var search = document.querySelector(".search-box form input#whois-search-input");
    var button = document.querySelector(".search-box form button#whois-search-button");

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
            window.location.href = "/tools/whois/" + search.value;
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

if(document.querySelector(".search-box#macoui-search-box") != null) {
    tabs("#macoui-tabs"); // Setup a tabs

    document.querySelectorAll("form").forEach(form => {
        var inputs = form.getElementsByTagName("input");

        // Add event to submit trigger
        form.addEventListener("submit", e => {
            e.preventDefault();

            var url = new URL(location.origin + "/api/v1/mac-oui");

            // Forge a URI with params if the form is "find-form" or put the resource in
            // PATHINFO if the form is "precise-form"
            if(form.id == "find-form") {
                var params = [];

                for(var i=0; i < inputs.length; i++) {
                    var el = inputs[i];

                    if(el.value != "")
                        params.push([el.getAttribute("name"), el.value]);
                }

                url.search = new URLSearchParams(params);
            } else if(form.id == "precise-form") {
                url.pathname = `${url.pathname}/${encodeURIComponent(inputs[0].value)}`;
            }

            fetch(url).then(resp => {
                var result_div = document.querySelector(".mac-oui-return");
                var result_body = document.querySelector(".mac-oui-return .siimple-card-body");

                // Show if the result div is not visible and add a loader
                result_div.classList.add("active");
                result_body.innerHTML = `<div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>`;

                resp.json().then(json => {
                    if(Array.isArray(json)) {
                        if(json.length == 0) {
                            var tip = document.createElement("div");
                            tip.classList.add(...["siimple-tip", "siimple-tip--warning"]);
                            tip.textContent = `No entry found in the database.`;
                            result_body.appendChild(tip);
                        } else {
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
                        }
                    } else {
                        var tip = document.createElement("div");

                        if(Object.keys(json).length == 0) {
                            tip.classList.add(...["siimple-tip", "siimple-tip--warning"]);
                            tip.textContent = `No entry found in the database.`;
                        } else {
                            var list = document.createElement("ul");
                            list.classList.add("no-style");

                            var node = document.createElement("li");
                            node.innerText = `Assignment: ${json.assignment}`;
                            list.appendChild(node);

                            node = document.createElement("li");
                            node.innerText = `Organization: ${json.orgname}`;
                            list.appendChild(node);

                            node = document.createElement("li");
                            node.innerText = `Organization address: ${json.orgaddr}`;
                            list.appendChild(node);

                            tip.appendChild(list);
                        }

                        result_body.appendChild(tip);
                    }

                    // Show the result div with the new results
                    document.querySelector(".lds-ellipsis").remove();
                });

            }).catch(err => {
                console.error(err);

                var result_div = document.querySelector(".mac-oui-return");
                var result_body = document.querySelector(".mac-oui-return .siimple-card-body");
                result_body.innerHTML = "";

                var tip = document.createElement("div");
                tip.classList.add(...["siimple-tip", "siimple-tip--error"]);
                tip.textContent = "Unable to retrieve the result of the request. Something go wrong with the API..."
                result_body.append(tip);

                result_div.classList.add("active");
            });
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