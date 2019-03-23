/**
 *
 * @param {*} root_selector
 */
function tabs(root_selector) {
    var root = document.querySelector(root_selector);
    var tabs = root.children;
    var control_div_id = root.getAttribute('tabs-control');

    if(control_div_id == null) {
        throw Error("Not have `tabs-control` attribute set.");
    }

    // Function for switching tab and block
    function switch_tab(tab, block_id) {
        if(block_id != null) {
            // Remove selected class to all tabs and add it to the specified tab
            for(var i = 0; i < tabs.length; i++) tabs[i].classList.remove("siimple-tabs-item--selected")
            tab.classList.add("siimple-tabs-item--selected");

            // Remove active class to all blocks and add it to the linked block
            var controls_blocks = document.querySelectorAll(`.tabs-controls#${control_div_id} > .tabs-block`);
            controls_blocks.forEach(block => block.classList.remove("active"));

            document.querySelector(`.tabs-block#${block_id}`).classList.add("active");
        }
    }

    // Check if a tab already have a "selected" class
    for(var i = 0; i < tabs.length; i++) {
        if(tabs[i].classList.contains("siimple-tabs-item--selected")) {
            var block_id = tabs[i].getAttribute("tab-block");
            switch_tab(tabs[i], block_id);
        }

        // Add an event for listening tab change
        tabs[i].addEventListener("click", el => {
            var block_id = el.target.getAttribute("tab-block");
            switch_tab(el.target, block_id);
        });
    }
}

/**
 *
 * @param {String} resource
 */
function valid_whois_resource(resource) {
    var asn_regex = /^AS\d{1,10}$/i;
    var ip_regex = /^((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))$/;
    var domain_regex = "";

    if(resource.match(asn_regex) || resource.match(ip_regex)) return true;
    else return false;
}


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
        if(valid_whois_resource(search.value)) button.classList.remove('.siimple-btn--disabled');
        else button.classList.remove('.siimple-btn--disabled');
    });


    // Add an event to rewrite the action URI on submit
    form.addEventListener("submit", e => {
        e.preventDefault();

        if(valid_whois_resource(search.value)) {
            form.action = "/whois/" + search.value;
            form.submit();
        } else {
            // TODO: Show a error on the front.
            console.error("Ressource not valid.");
        }
    })
}