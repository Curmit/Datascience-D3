//https://www.youtube.com/watch?v=-lEEEi-0Fqc
//https://github.com/matthewmueller/x-ray

var Xray = require('x-ray'),
	x = new Xray();

x('http://www.reddit.com', '#siteTable .thing', [{
	name: 'a.title',
	likes: '.score.likes',
	comments: '.comments'
}])
.paginate('.nextprev a@href') 
.limit(2)
.write('./scripts/flare.json');