'use strict';

// Pass token through command line
// $ TOKEN=your-token-secret npm start
if (!process.env.token) {
    console.log('Error: Specify token in environment');
    process.exit(1);
}

const FSOCIETY_URL = 'http://127.0.0.1:5000/api/v1/paragraph/';

var Botkit = require('botkit');
var os = require('os');
const request = require('superagent');

var controller = Botkit.slackbot({
    debug: false
});

var bot = controller.spawn({
    token: process.env.token
}).startRTM();


controller.hears(['hello', 'hi'], 'direct_message,direct_mention,mention', function(bot, message) {

    bot.api.reactions.add({
        timestamp: message.ts,
        channel: message.channel,
        name: 'robot_face',
    }, function(err, res) {
        if (err) {
            bot.botkit.log('Failed to add emoji reaction :(', err);
        }
    });


    controller.storage.users.get(message.user, function(err, user) {
        if (user && user.name) {
            bot.reply(message, 'Hello ' + user.name + '!!');
        } else {
            bot.reply(message, 'Hello.');
        }
    });
});

// Command format: generate [query sentence] from [twitter/reddit/reuters]
controller.hears(['generate'], 'direct_message,direct_mention,mention', function(bot, message) {

    console.log(message);

    let raw = message.text.replace('generate', '').trim();
    const from = raw.indexOf('from');
    const query = raw.substring(0, from != -1 ? from : raw.length);
    const source = raw.substring(from + 'from'.length + 1, raw.length);

    if (query.length > 0) {
      // bot.reply(message, 'I can look from: ' + source + '. Your query is: ' + query);
      request
      .post(FSOCIETY_URL + source)
      .send('query=' + query)
      .send('paragraph_count=' + 4)
      .end((err, res) => {
        if (err) {
          console.log('Err', err);
          bot.reply(message, 'Sorry, my brain messed up.'); 
        }
        else {
          console.log('Res', res.body);
          let lorem = '';
          let counter = 0;
          res.body.data.forEach((d) => {
            lorem += d + '\n\n';
            counter++;

            if (counter === res.body.data.length) {
              bot.reply(message, lorem); 
            }
          });
        }
      });
    }
    else {
     bot.reply(message, 'Sorry, I can\'t think properly now.'); 
    }
});
