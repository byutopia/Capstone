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
	.catch(error => console.error('Error:', error))
	.then(response => console.log('Success:', response));
	console.log(id);
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
	.catch(error => console.error('Error:', error))
	.then(response => console.log('Success:', response));
	console.log(id);
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
	.catch(error => console.error('Error:', error))
	.then(response => console.log('Success:', response));
	console.log(id);
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
	.catch(error => console.error('Error:', error))
	.then(response => console.log('Success:', response));
	console.log(id);
}
document.addEventListener("DOMContentLoaded", function() {
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	

});
