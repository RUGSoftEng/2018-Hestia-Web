/**
 * @fileOverview
 * @name domInteraction.js
 * This file contains functions to interact with the webpage to dynamically load devices.
 */

var SELECTED_DEVICE = null;
var SELECTED_SERVER = null;

/**
 * Removes all children from a node. Used in the gui.
 * @param {} node
 */
function removeChildren(node) {
    if (node) {
        while (node.firstChild) {
            node.removeChild(node.firstChild);
        }
    }
}

/**
 * Sets all children of a node to have a particular class.
 * @param {} node
 * @param {} className
 */
function setAllChildrenToClass(node, className) {
    var children = node.children;
    for (var i = 0; i < children.length; i++){
        children[i].className = className;
    }
}

/**
 * Finds a device by its id in an array. Returns null if it is not found.
 * @param {} id
 * @param {} array
 * @returns {} json object
 */
function getDeviceById(id, array) {
    for (var i = 0; i < array.length; i++) {
        if (array[i].deviceId == id) {
            return array[i];
        }
    }
    return null;
}

/**
 * Wrapper to update the re-populated the device list based on a promised json
 * object from the server.
 */
function updateDeviceList() {
    var devices = getServerDevices(SELECTED_SERVER.address);
    devices.then(result => {
            console.log("Got devices from server: ");
            console.log(result);
            populateDevices(result);
        })
        .catch(err => {
            console.log(err);
        });
}

function updateServerList() {
    getUserServers(firebase, firebase.auth().currentUser).then(servers =>{
        populateServers(servers);
    });
}

function populateServers(servers){
    var serversListElem = document.getElementById("serverNamesList");
    removeChildren(serversListElem);

    for (var name in servers){
        var elem = document.createElement("li");
        elem.className = "device_row";
        elem.id = name;
        console.log("Found server with name: " + name);
        elem.onclick = function(){
            setAllChildrenToClass(serversListElem, "device_row");
            this.className = "device_row active";

            var server = servers[this.id];
            SELECTED_SERVER = server;
            SELECTED_DEVICE = null;

            updateDeviceList();
        };
        elem.appendChild(document.createTextNode(name));
        serversListElem.appendChild(elem);
    }

    if (SELECTED_SERVER == null){
        if (serversListElem.firstChild != null){
            serversListElem.firstChild.click();
        }
    } else {
        document.getElementById(SELECTED_SERVER).click();
    }
}

/**
 * Generates the html to view all of the devices in data.
 * @param {} data
 */
function populateDevices(data){
    var namesListElem = document.getElementById("deviceNamesList");
    removeChildren(namesListElem);

    //Insert placeholder in temporary payload input to add devices
    var inputPlaceholder = '{\n "plugin_name": "light",\n "collection": "mock",\n "required_info": {\n   "ip": "123",\n   "port": "456",\n   "name": "not_a_kitchen_light"\n  }\n}';
    document.getElementById("payload_input").value = inputPlaceholder;

    data.forEach(function(device) {
        var elem = document.createElement("li");
        elem.className = "device_row";
        elem.id = device.deviceId;
        elem.onclick = function() {
            setAllChildrenToClass(namesListElem, "device_row");
            elem.className = "device_row active";

            var dev = getDeviceById(elem.id, data);
            SELECTED_DEVICE = dev.deviceId;

            viewDeviceActivators(dev.name, dev.deviceId, dev.activators);
        };

        elem.appendChild(document.createTextNode(device.name));
        namesListElem.appendChild(elem);
    });

    if (SELECTED_DEVICE == null){
        if (namesListElem.firstChild != null){
            namesListElem.firstChild.click();
        }
    } else {
        document.getElementById(SELECTED_DEVICE).click();
    }
}

/**
 * Generates the html to view a device with a particular deviceName and for its
 * associated activators. deviceId is passed so that we may interact with the
 * activators and know their device. This will be refactored.
 * @param {} deviceName
 * @param {} deviceId
 * @param {} activators
 */
function viewDeviceActivators(deviceName, deviceId, activators) {
    var activatorsElem = document.getElementById("activatorsList");
    var activatorsTitle = document.getElementById("activatorsTitle");
    activatorsTitle.firstChild.innerHTML = deviceName;
    removeChildren(activatorsElem);
    for (var i = 0; i < activators.length; i++) {
        var activator = activators[i];
        var elem = document.createElement("div");
        elem.className = "device_control_row";
        elem.appendChild(document.createTextNode(activator.name));
        switch (activator.type) {
            case "bool":
                var label = document.createElement("label");
                label.className = "switch";
                var input = document.createElement("input");
                input.type = "checkbox";
                input.name = deviceId;
                input.onclick = onToggleInteracted;
                input.id = activator.activatorId;
                input.checked = activator.state;
                label.appendChild(input);
                var span = document.createElement("span");
                span.className = "switchSlider round";
                label.append(span);
                elem.appendChild(label);
                break;
            case "float":
                var slideContainer = document.createElement("div");
                slideContainer.className = "slidecontainer";
                var input = document.createElement("input");
                input.type = "range";
                input.min = 0;
                input.max = 100;
                input.step = 10;
                input.name = deviceId;
                input.value = activator.state * 100; // TODO Based on object
                input.className = "slider";
                input.id = activator.activatorId;
                input.onchange = onSliderInteracted;
                slideContainer.appendChild(input);
                elem.appendChild(slideContainer);
                break;
            default:
                console.log("Unknown activator type: " + activator.type);
        }
        activatorsElem.appendChild(elem);
    }
}