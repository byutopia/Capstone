function start(id) {
	var url = '/rainmachine/start';
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


function stop(id) {
	var url = '/rainmachine/stop';
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