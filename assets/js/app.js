var leaflet = require('leaflet'),
    tabs = require('./components/tabs'),
    validators = require('./components/validators');

// Overide leaflet icon path
leaflet.Icon.Default.imagePath = '/static/img/leaflet/';

/**
 * Operation modal
 */
if(document.querySelector("#operation-create-btn") != null) {
    let btn = document.querySelector("#operation-create-btn");
    let modal = document.querySelector("#operation-modal");
    let modal_body = document.querySelector("#operation-modal .siimple-modal-body");
    let form = document.querySelector('form#operation-create-form');
    let close_btn = document.querySelector("#operation-modal #operation-modal-close");
    let cancel_btn = document.querySelector("#operation-modal #operation-modal-cancel");
    let queues_list = document.querySelector("#operation-create-queues-list");

    let close_modal = () => {
        modal.style.display = "none";
        form.reset();
    }

    // Show the modal
    btn.addEventListener("click", () => modal.style.display = "");

    close_btn.addEventListener("click", () => close_modal());
    cancel_btn.addEventListener("click", () => close_modal());

    // Retrieve available queues
    fetch(new URL(location.origin + "/api/v1/management/backend/queues")).then(resp => {
        if(resp.status != 200) {
            var tip = document.createElement("div");
            tip.classList.add(...["siimple-tip", "siimple-tip--warning", "siimple-tip--exclamation"]);
            tip.textContent = `Unable to retrieve the list of queues. Please retry more later.`;
            queues_list.appendChild(tip);
        } else {
            resp.json().then(payload => {
                // Build each checkbox in good form.
                payload.forEach(queue => {
                    let div = document.createElement("div");
                    div.classList.add("queue");

                    let label = document.createElement("label");
                    label.classList.add("siimple-label");
                    label.textContent = queue.name;


                    let checkbox_div = document.createElement("div");
                    checkbox_div.classList.add("siimple-checkbox");

                    let checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    checkbox.name = "queues";
                    checkbox.value = queue.queue;
                    checkbox.id = `operation-queue--${queue.queue}`;

                    let checkbox_label = document.createElement("label");
                    checkbox_label.setAttribute("for", checkbox.id);

                    if(queue.broadcast == false) {
                        label.textContent = `${queue.name} (not broadcast)`;
                        checkbox_div.classList.add("siimple-checkbox--warning");
                    }

                    checkbox_div.appendChild(checkbox);
                    checkbox_div.appendChild(checkbox_label);
                    div.appendChild(label);
                    div.appendChild(checkbox_div);
                    queues_list.appendChild(div);
                });
            });
        }
    });

    // Send the form
    form.addEventListener("submit", e => {
        e.preventDefault();

        let form_data = new FormData(form);
        let json_data = {
          queues: []
        };

        // Put all the form informations into JSON serialable
        form_data.forEach(function(value, key) {
            if(key == "queues") json_data.queues.push(value);
            else json_data[key] = value;
        });

        fetch(new URL(location.origin + "/api/v1/operations"), {
            method: "POST",
            body: JSON.stringify(json_data),
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        }).then(resp => {
            resp.json().then(payload => {
                if(resp.status >= 500 && resp.status < 599) {
                    let tip = document.createElement("div");
                    tip.classList.add(...["siimple-tip", "siimple-tip--error", "siimple-tip--exclamation"]);
                    tip.textContent = "Internal server error. Unable to create the operation.";
                    modal_body.prepend(tip);

                    // Destroy the tip after 5 seconds
                    setTimeout(() => tip.remove(), 5000);
                } else if(resp.status >= 400 && resp.status <= 499) {
                    let tip = document.createElement("div");
                    tip.classList.add(...["siimple-tip", "siimple-tip--warning", "siimple-tip--exclamation"]);
                    tip.textContent = "Some informations are not provided or not correct.";
                    modal_body.prepend(tip);

                    // Destroy the tip after 5 seconds
                    setTimeout(() => tip.remove(), 5000);
                } else {
                    if(Object.keys(payload).indexOf("operation_id") != -1) {
                        window.location.href = `${location.origin}/operations/${payload.operation_id}`;
                    }
                }
            });

        });
    });
}

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
        if(validators.valid_whois_resource(search.value)) button.classList.remove('siimple-btn--disabled');
        else button.classList.add('siimple-btn--disabled');
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


/**
 * Mac OUI Vendor page
 */
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


/**
 * IP Calc page
 */
if(document.querySelector("#ipcalc-form") != null) {
    var input = document.querySelector("input[name=resource]");
    var errors = document.querySelector("#ipcalc-errors");

    input.addEventListener("input", () => {
        if(input.value == "") input.classList.remove("siimple-input--danger");
        else {
            if(validators.validate_ipv4(input.value, true) || validators.validate_ipv6(input.value, true)) {
                input.classList.remove("siimple-input--danger");
                errors.innerHTML = "";

                var url = new URL(`${location.origin}/api/v1/ip-calc/${input.value}`);
                fetch(url).then(resp => {
                    resp.json().then(json => {
                        if(resp.status == 200) {
                            // Fill netmask input for IPv4 with a CIDR < 31
                            if(Object.keys(json).includes("netmask")) {
                                document.querySelector("#netmask-addr").classList.remove("hidden");
                                document.querySelector("#netmask-addr input").value = json.netmask;
                            } else {
                                document.querySelector("#netmask-addr").classList.add("hidden");
                                document.querySelector("#netmask-addr input").value = "";
                            }

                            // Fill broadcast input for IPv4 with a CIDR < 31
                            if(Object.keys(json).includes("broadcast")) {
                                document.querySelector("#broadcast-addr").classList.remove("hidden");
                                document.querySelector("#broadcast-addr input").value = json.broadcast;
                            } else {
                                document.querySelector("#broadcast-addr").classList.add("hidden");
                                document.querySelector("#broadcast-addr input").value = "";
                            }

                            // Fill first_ip input for all subnets with more than 2 ips
                            if(Object.keys(json).includes("first_ip")) {
                                document.querySelector("#first-ip").classList.remove("hidden");
                                document.querySelector("#first-ip input").value = json.first_ip;
                            } else {
                                document.querySelector("#first-ip").classList.add("hidden");
                                document.querySelector("#first-ip input").value = "";
                            }

                            // Fill last_ip input for all subnets with more than 2 ips
                            if(Object.keys(json).includes("last_ip")) {
                                document.querySelector("#last-ip").classList.remove("hidden");
                                document.querySelector("#last-ip input").value = json.last_ip;
                            } else {
                                document.querySelector("#last-ip").classList.add("hidden");
                                document.querySelector("#last-ip input").value = "";
                            }

                            // Fill other inputs
                            document.querySelector("#network-addr input").value = json.network;
                            document.querySelector("#cidr input").value = json.cidr;
                            document.querySelector("#usable-ips input").value = json.usable_ips;
                        } else {
                            input.classList.add("siimple-input--danger");

                            json.errors.forEach(err => {
                                var tip = document.createElement("div");
                                tip.classList.add(...["siimple-tip", "siimple-tip--error"]);
                                tip.textContent = err.description;
                                errors.appendChild(tip);
                            });
                        }
                    });
                });
            } else {
                input.classList.add("siimple-input--danger");
            }
        }
    });
}

/**
 * Operation page
 */
if(document.querySelector(".operations-infos-bar") != null) {
    let infobar = document.querySelector(".operations-infos-bar");
    let oper_status = infobar.getAttribute("operation-status");

    switch(oper_status) {
        case "pending":
            infobar.setAttribute("class", "operations-infos-bar");
            infobar.classList.add(...["siimple--bg-light", "siimple--color-dark"]);
            break;

        case "progress":
            infobar.setAttribute("class", "operations-infos-bar");
            infobar.classList.add(...["siimple--bg-primary", "siimple--color-light"]);

            // Set a timeout for refreshing the page every 10 seconds
            setTimeout(() => location.reload(), 10000);
            break;

        case "timeout":
            infobar.setAttribute("class", "operations-infos-bar");
            infobar.classList.add(...["siimple--bg-warning", "siimple--color-dark"]);
            break;

        case "error":
            infobar.setAttribute("class", "operations-infos-bar");
            infobar.classList.add(...["siimple--bg-error", "siimple--color-light"]);
            break;

        case "done":
            infobar.setAttribute("class", "operations-infos-bar");
            infobar.classList.add(...["siimple--bg-success", "siimple--color-light"]);
            break;

        default:
            infobar.setAttribute("class", "operations-infos-bar");
            infobar.classList.add(...["siimple--bg-light", "siimple--color-dark"]);
            break;
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