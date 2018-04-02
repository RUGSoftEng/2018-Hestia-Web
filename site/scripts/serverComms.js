/**
 * @fileOverview
 * @name serverComms.js
 * The file contains all the javascript needed to communicate with the Flask and
 * the remote Hestia controller. It needs refactoring and rearchitecturing.
 */

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



/**
 * Gets a device with a particular deviceId from a server. This uses promises as
 * the request is asynchronous. If the promise is not fulfilled it rejects the
 * promise and errors.
 * @param {} server
 * @param {} deviceId
 * @returns {} promised device
 */
function getDevice(server, deviceId) {
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

window.onload = function() {
    sendRequest(globalServer(), "/devices/", "GET", populateDevices);
};