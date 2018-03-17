// the endpoint to start watering a zone, sends id to controller from template
function zoneStart(id) {
	var url = '/rainmachine/zstart';
	var data = {id: id};

	fetch(url, {
	  method: 'POST', // or 'PUT'
	  body: JSON.stringify(data),
	  headers: new Headers({
	    'Content-Type': 'application/json'
	  })
	}).then(res => res.json())
	.catch(error => console.error('Error:', error));
}

// the endpoint to stop watering a zone, sends id to controller from template
function zoneStop(id) {
	var url = '/rainmachine/zstop';
	var data = {id: id};

	fetch(url, {
	  method: 'POST', // or 'PUT'
	  body: JSON.stringify(data),
	  headers: new Headers({
	    'Content-Type': 'application/json'
	  })
	}).then(res => res.json())
	.catch(error => console.error('Error:', error));
}

// the endpoint to start watering a program, sends id to controller from template
function programStart(id) {
	var url = '/rainmachine/pstart';
	var data = {id: id};

	fetch(url, {
	  method: 'POST', // or 'PUT'
	  body: JSON.stringify(data),
	  headers: new Headers({
	    'Content-Type': 'application/json'
	  })
	}).then(res => res.json())
	.catch(error => console.error('Error:', error));
}

// the endpoint to stop watering a program, sends id to controller from template
function programStop(id) {
	var url = '/rainmachine/pstop';
	var data = {id: id};

	fetch(url, {
	  method: 'POST', // or 'PUT'
	  body: JSON.stringify(data),
	  headers: new Headers({
	    'Content-Type': 'application/json'
	  })
	}).then(res => res.json())
	.catch(error => console.error('Error:', error));
}

// function to add and start a timer to the zone card
// the callback function emits a getData socket call,
// which should start the next queued zone
function makeTimer(duration, display, callback) {
    var timer = duration, minutes, seconds;
    var timerInt = setInterval(function() {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = "Time Left: " + minutes + ":" + seconds;

        if (--timer < 0) { 
            display.textContent = "Finished!";
            display.classList.remove("active");
            setTimeout(() => { display.textContent = "Inactive"; }, 700);
            callback();
            clearInterval(timerInt);
        }
    }, 1000);
}

document.addEventListener("DOMContentLoaded", function() {
	var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        console.log("Socket connected!");
        socket.emit('getData'); // get updated rainmachine data
    });
    socket.on('rainmachineData', function(data) {
        for (let z of data.zone.zones) { // iterate over zones
            if (z.state == 1 && z.uid != 1) { // if zone is running and isn't zone 1, make a timer
                let stat = document.querySelector("#card-"+z.uid+" .status");
                stat.classList.add("active")
                makeTimer(z.remaining, stat, () => { socket.emit('getData'); });
            } else if (z.state == 2) { // if zone is queued to run, make card reflect that
                let stat = document.querySelector("#card-"+z.uid+" .status");
                stat.classList.add("active");
                stat.textContent = "Queued";
            }
        }
    });
	socket.on('rainmachineUpdate', function(msg) { // when either start or stop is pressed
        if (msg.type === 'zone') {
            if (msg.data.status === 'started') {
                socket.emit('getData');
            } else if (msg.data.status === 'stopped') {
                socket.emit('getData');
            }
        } else if (msg.type === 'program') {
            var stat = document.querySelector("#program-"+(msg.data.programID+1)+" .state");
            if (msg.data.status === 'started') {
                stat.textContent = "Running";
            } else if (msg.data.status === 'stopped') {
                stat.textContent = "Not Running";
            }
        }
    });
});
