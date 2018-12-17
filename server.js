console.log('Server-side code running');

const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const { exec } = require('child_process');




const app = express();

// serve files from the public directory
app.use(express.static(__dirname))

app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies;

// start the express web server listening on 8080
app.listen(8080, () => {
	console.log('listening on 8080');
});

// serve the homepage
app.get('/', (req, res) => {
	res.sendFile(__dirname + '/index.html');
});

app.post('/connection', (req, res) => {
	var email = req.body.email;
	var pwd = req.body.password;
	exec('python3 dataminer.py '+email+' '+pwd, (error, stdout, stderr) => {
		if (error) {
			res.sendStatus(400);
			return;
		}
		fs.readFile(stdout.split('\n')[0]+'.json', 'utf8', function (err, data) {
			if (err) throw err;
			obj = JSON.parse(data);
			res.json(data);
		});
	});
});

