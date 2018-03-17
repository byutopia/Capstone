document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port) // make websocket connection
    var stat = document.querySelector("div.status")
    socket.on('connect', function() {
        socket.emit('getWago'); // get updated data
    });
    socket.on('wagoUpdate', function(msg) { // make UI match Wago state
        if (msg.lightsOn === true) {
            stat.innerHTML = "<img class='light' src='/static/images/light-bulb-on.png'>"
        } else {
            stat.innerHTML = "<img class='light' src='/static/images/light-bulb-off.png'>"
        }
    })
})
