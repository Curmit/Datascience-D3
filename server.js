// importing labaries,my files and starting the server in app 
var express = require('express'),
	fs = require('fs'),
	path = require('path'),
	request = require('request'),
	routes = require('./routes/index'),
	app = express();


// app.use??
// makes path variables

app.use('/node', express.static(__dirname + '/node_modules/'));
app.use('/scripts', express.static(__dirname + '/scripts'));
app.use('/stylesheets', express.static(__dirname + '/stylesheets'));

app.set('view engine', 'jade');
app.use('/', routes);

app.listen('8081');

console.log('Server running on port 8081');
exports = module.exports = app;
view raw