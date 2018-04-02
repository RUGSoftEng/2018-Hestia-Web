<<<<<<< HEAD:site/static/scripts/functions.js
//The most recent json object received by the client.
var LAST_DATA_RECEIVED = null;
var SELECTED_DEVICE = null;

function globalServer() {
    return document.getElementById("serverAddress").value;
}

//Sends an asynchronous request to the webserver, intended to reach a local controller.
function sendRequest(serverAddress, endpoint, method, callback, payload={}){
    var data = {
        query: serverAddress + endpoint,
        method: method,
        payload: payload
    };
    console.log("Sending request:");
    console.log(data);
    $.ajax({
        url: "/request.php",
        type: "post",
        cache: false,
        data: data,
        dataType: "json",
        success: callback
    });
}

//Updates a device activator using an abstracted call to send a request.
function updateDeviceActivator(serverAddress, deviceId, activatorId, newState){
    console.log("Sending request to: "+serverAddress);
    console.log("endpoint: "+"/devices/" + deviceId + "/activators/" + activatorId);
    sendRequest(serverAddress,
        "/devices/" + deviceId + "/activators/" + activatorId,
        "POST",
        function(response){
            console.log("Response from updating device activator.");
            console.log(response);
        });
}

// promises a device
function getDevice(server, deviceId){
=======
/**
 * @fileOverview
 * @name functions.js
 * The file contains all the javascript needed to communicate with the Flask and
 * the remote Hestia controller. It needs refactoring and rearchitecturing.
 */

/**
 * Gets a device with a particular deviceId from a server. This uses promises as
 * the request is asynchronous. If the promise is not fulfilled it rejects the
 * promise and errors.
 * @param {} server
 * @param {} deviceId
 * @returns {} promised device
 */
function getDevice(server, deviceId) {
>>>>>>> feature/sprint2:flask/templates/static/scripts/functions.js
    console.log("getDevice() is called");

    return new Promise(function(resolve, reject) {
        var request = new XMLHttpRequest();
        var url = "/request";

        request.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                result = this.responseText;
                obj = JSON.parse(result);

                if (obj) {
                    resolve(obj);
                } else {
                    let error = new Error('Could not fetch device');
                    reject(error);
                    return;
                }
            }
        };

        var data = {
            "query": server + "/devices/" + deviceId,
            "method": "GET"
        };

        request.open("POST", url, true);
        request.setRequestHeader("Content-type", "application/json");
        request.send(JSON.stringify(data));
    });
}


/**
 * This function sends a request to a server to change the state of the
 * activator with activatorId for the device with deviceId.
 * @param {} server
 * @param {} deviceId
 * @param {} activatorId
 * @param {} state
 */
function changeActivator(server, deviceId, activatorId, state) {
    var request = new XMLHttpRequest();
    var url = "/request";

    var data = {
        "query": server + "/devices/" + deviceId + "/activators/" + activatorId,
        "method": "POST",
        "payload": {
            "state": state
        }
    };

    console.log(data);

    request.open("POST", url, true);
    request.setRequestHeader("Content-type", "application/json");
    request.send(JSON.stringify(data));
}


/**
 * This is an alias for the dimmers. How we choose to define these functions in
 * the future (e.g. an alias, a direct call, or something else) is subject to
 * change.
 * @param {} server
 * @param {} deviceId
 * @param {} activatorId
 * @param {} payload
 */
function dimmer(server, deviceId, activatorId, payload) {
    changeActivator(server, deviceId, activatorId, payload);
}


/**
 * This is an alias for the toggle switches. How we choose to define these functions in
 * the future (e.g. an alias, a direct call, or something else) is subject to
 * change.
 * @param {} server
 * @param {} deviceId
 * @param {} activatorId
 * @param {} payload
 */
function toggle(server, deviceId, activatorId, payload) {
    changeActivator(server, deviceId, activatorId, payload);
}


<<<<<<< HEAD:site/static/scripts/functions.js
//Removes all children from an element.
function removeChildren(node){
    while(node.firstChild){
        node.removeChild(node.firstChild);
    }
}

//Gets a device object by id from some data.
function getDeviceById(id){
    for (var i = 0; i < LAST_DATA_RECEIVED.length; i++){
        if (LAST_DATA_RECEIVED[i].deviceId == id){
            return LAST_DATA_RECEIVED[i];
=======

/**
 * Gets all devices for a given server. This uses promises as the request is
 * asynchronous. If the promise is not fulfilled it rejects the promise and
 * errors.
 * @param {} server
 * @returns {} promised json object
 */
function getServerDevices(server) {
    return new Promise(function(resolve, reject) {
        var request = new XMLHttpRequest();
        var url = "/request";

        request.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                result = this.responseText;
                obj = JSON.parse(result);

                if (obj) {
                    resolve(obj);
                } else {
                    let error = new Error('Could not fetch device');
                    reject(error);
                    return;
                }
            }
        };

        var data = {
            "query": server + "/devices/",
            "method": "GET"
        };

        request.open("POST", url, true);
        request.setRequestHeader("Content-type", "application/json");
        request.send(JSON.stringify(data));
    });
}


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
 * Finds a device by its id in an array. Returns null if it is not found.
 * @param {} id
 * @param {} array
 * @returns {} json object
 */
function getDeviceById(id, array) {
    for (var i = 0; i < array.length; i++) {
        if (array[i].deviceId == id) {
            return array[i];
>>>>>>> feature/sprint2:flask/templates/static/scripts/functions.js
        }
    }
    return null;
}

<<<<<<< HEAD:site/static/scripts/functions.js
//Populates the list of devices from some data received from the server.
//  data is a list of devices as received from the server.
function populateDevices(data){
    LAST_DATA_RECEIVED = data;
=======
/**
 * Generates the html to view all of the devices in data.
 * @param {} data
 */
function populateDevices(data) {
>>>>>>> feature/sprint2:flask/templates/static/scripts/functions.js
    var namesListElem = document.getElementById("deviceNamesList");
    removeChildren(namesListElem);

    //Insert placeholder in temporary payload input to add devices
    var inputPlaceholder = '{\n "plugin_name": "light",\n "collection": "mock",\n "required_info": {\n   "ip": "123",\n   "port": "456",\n   "name": "not_a_kitchen_light"\n  }\n}';
    document.getElementById("payload_input").value = inputPlaceholder;

    console.log(data);
    data.forEach(function(device) {
        var elem = document.createElement("li");
        elem.className = "device_row";
        elem.id = device.deviceId;
        elem.onclick = function() {
            var children = namesListElem.children;
            for (var i = 0; i < children.length; i++) {
                children[i].className = "device_row";
            }
            elem.className = "device_row active";

            var dev = getDeviceById(elem.id, data);
            SELECTED_DEVICE = dev.deviceId;

            viewDeviceActivators(dev.name, dev.deviceId, dev.activators);
        };

        elem.appendChild(document.createTextNode(device.name));
        namesListElem.appendChild(elem);
    });

    namesListElem.firstChild.click();
    SELECTED_DEVICE = namesListElem.firstChild.id;
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

/**
 * Is a wrapper for the function our toggles calls. We currently have only one
 * type of toggle so the name is bad.
 */
function onToggleInteracted() {
    toggle(document.getElementById("serverAddress").value, this.name, this.id, this.checked);
}

/**
 * Is a wrapper for the function our sliders calls. We currently have only one
 * type of slider so the name is bad.
 */
function onSliderInteracted() {
    dimmer(document.getElementById("serverAddress").value, this.name, this.id, this.value / 100);
}

<<<<<<< HEAD:site/static/scripts/functions.js
//When the user changes a slider's value.
function onSliderInteracted(){
    console.log("User changed slider: " + this.id + ", Current state: " + this.value);
    updateDeviceActivator(globalServer(), SELECTED_DEVICE, this.id, 0.1);
}

window.onload = function() {
    sendRequest(globalServer(), "/devices/", "GET", populateDevices);
};
=======
/**
 * Is a wrapper for the function our button calls. We currently have only one
 * functionality for the buttons so the name is bad.
 */
function onClickInteracted() {
    postDevice(document.getElementById("serverAddress").value, document.getElementById("payload_input").value);
}

/**
 * Wrapper to update the re-populated the device list based on a promised json
 * object from the server.
 */
function updateDeviceList() {
    var devices = getServerDevices(document.getElementById("serverAddress").value);
    devices.then(result => {
            populateDevices(result);
        })
        .catch(err => {
            console.log(err);
        });
}

/**
 * Sends the request to add new device described by payload to the server.
 * @param {} server
 * @param {} payload
 */
function postDevice(server, payload) {
    var request = new XMLHttpRequest();
    var url = "/request";

    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            result = this.responseText;
            obj = JSON.parse(result);
        }
    };

    var data = {
        "query": server + "/devices/",
        "method": "POST"
    };

    console.log(data);

    if (payload) {
        // Payload is not empty
        data.payload = JSON.parse(payload);
    }

    request.open("POST", url, true);
    request.setRequestHeader("Content-type", "application/json");
    request.send(JSON.stringify(data));
}
>>>>>>> feature/sprint2:flask/templates/static/scripts/functions.js
