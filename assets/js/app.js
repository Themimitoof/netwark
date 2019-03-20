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