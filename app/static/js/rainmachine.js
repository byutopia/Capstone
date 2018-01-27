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
