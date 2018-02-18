//Express application object, uses it to get a Router object and 
//then adds a couple of routes to it using the get() method. Last of all exports the Router object.
// check for explantion:  https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs/routes

var express = require('express'),
	router = express.Router();



router.get('/', function(req, res, next) {//HTTP Request object,HTTP response, next() middelware  chain 
	res.render('index');
});

module.exports = router;