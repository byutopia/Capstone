//$(document).ready(function() {
document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port)
    var stat = document.querySelector(".status")
    socket.on('wagoUpdate', function(msg) {
        if (msg.lightsOn === true) {
            //$(".status").html("Lights are on!").css("background", "#407F40")
            stat.innerHTML = "Lights are on!"
            stat.style.background = "#407F40"
            stat.style.color = "white"
        } else {
            //$(".status").html("Lights are off...").css("background", "#7F3F38")
            stat.innerHTML = "Lights are off..."
            stat.style.background = "#7F3F38"
            stat.style.color = "white"
        }
    })
})
