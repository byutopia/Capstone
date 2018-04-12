// the endpoint to start watering a zone, sends id to controller from template
function zoneStart(id) {
	var url = '/rainmachine/zstart';
	var data = {id: id};

	fetch(url, {
	  method: 'POST',
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
	  method: 'POST',
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
	  method: 'POST',
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
	  method: 'POST',
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
    return timerInt;
}

document.addEventListener("DOMContentLoaded", function() {
    var timers = {}
	var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        console.log("Socket connected!");
        socket.emit('getData'); // get updated rainmachine data
    });
    socket.on('rainmachineData', function(data) {
        for (let z of data.zone.zones) { // iterate over zones
            let stat = document.querySelector("#card-"+z.uid+" .status");
            if (z.state == 1) { // if zone is running and isn't zone 1, make a timer
                if (!timers["card-"+z.uid] || timers["card-"+z.uid] == 0) {
                    stat.classList.add("active")
                    timers["card-"+z.uid] = makeTimer(z.remaining, stat, () => { 
                        timers["card-"+z.uid] = 0;
                        socket.emit('getData'); 
                    });
                }
            } else if (z.state == 2) { // if zone is queued to run, make card reflect that
                stat.classList.add("active");
                stat.textContent = "Queued";
            } else if (z.state == 0) { // if zone is inactive
                if (stat.classList.contains("active")) {
                    if (timers["card-"+z.uid] > 0) {
                        clearInterval(timers["card-"+z.uid])
                        timers["card-"+z.uid] = 0;
                        stat.classList.remove("active");
                        stat.textContent = "Inactive";
                    }
                }
            }
        }
    });
	socket.on('rainmachineUpdate', function(msg) { // when either start or stop is pressed
        if (msg.type === 'zone') {
            if (msg.data.status === 'started') {
                socket.emit('getData')
                setTimeout(() => { socket.emit('getData') }, 3000);
            } else if (msg.data.status === 'stopped') {
                socket.emit('getData')
                setTimeout(() => { socket.emit('getData') }, 3000);
            }
        } else if (msg.type === 'program') {
            var stat = document.querySelector("#program-"+(msg.data.programID)+" .state");
            if (msg.data.status === 'started') {
                stat.textContent = "Running";
            } else if (msg.data.status === 'stopped') {
                stat.textContent = "Not Running";
            }
        }
    });
});

