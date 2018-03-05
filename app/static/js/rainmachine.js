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
	//.then(response => console.log('Success:', response));
	//console.log(id);
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
	//.then(response => console.log('Success:', response));
	//console.log(id);
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
	//.then(response => console.log('Success:', response));
	//console.log(id);
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
	//.then(response => console.log('Success:', response));
	//console.log(id);
}
function makeTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function() {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = "Time Left: " + minutes + ":" + seconds;

        if (--timer < 0) { display.textContent = "Finished!"; }
    }, 1000);
}

document.addEventListener("DOMContentLoaded", function() {
	var socket = io.connect('http://' + document.domain + ':' + location.port, { path: '/rainmachine'});
    socket.on('rainmachineData', function(data) {
        console.log(data);
    });
	socket.on('rainmachineUpdate', function(msg) {
        if (msg.type === 'zone') {
            var stat = document.querySelector("#card-"+msg.data.zoneID+" .status");
            if (msg.data.status === 'started') {
                //stat.innerHTML = "Time Left: " + (msg.data.time / 60) + " min.";
                makeTimer(msg.data.time, stat);
                stat.style.opacity = 1;
            } else if (msg.data.status === 'stopped') {
                stat.innerHTML = "Inactive";
                stat.style.opacity = 0.4;
            }
        } else if (msg.type === 'program') {
            var stat = document.querySelector("#program-"+msg.data.programID+" .state");
            if (msg.data.status === 'started') {
                stat.innerHTML = "Running";
            } else if (msg.data.status === 'stopped') {
                stat.innerHTML = "Not Running";
            }
        }
    });
});
