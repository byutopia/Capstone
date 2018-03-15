//$(document).ready(function() {
document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port)
    var stat = document.querySelector("div.status")
    socket.on('connect', function() {
        socket.emit('getWago');
    });
    socket.on('wagoUpdate', function(msg) {
        if (msg.lightsOn === true) {
            //$(".status").html("Lights are on!").css("background", "#407F40")
            stat.innerHTML = "<img class='light' src='/static/images/light-bulb-on.png'>"
        } else {
            //$(".status").html("Lights are off...").css("background", "#7F3F38")
            stat.innerHTML = "<img class='light' src='/static/images/light-bulb-off.png'>"
        }
    })
})
