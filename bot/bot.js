// https://docs.tmijs.org/v1.2.1/Configuration.html
// https://docs.tmijs.org/v1.2.1/Commands.html
// http://momentjs.com/timezone
var tmi = require('tmi.js')
var moment = require('moment-timezone')

// Create an array with the channels we want to join
var channels = []
for (let i = 4; i < process.argv.length; i++) {
    channels.push(process.argv[i])
}

// Define configuration options
var options = {
  options: { debug: true },
  // options: { debug: false },
  connection: { reconnect: true },
  identity: {
    username: process.argv[2],
    password: process.argv[3]
  },
  channels: channels
}

// Create a client with our options:
var client = new tmi.client(options)

///////////////////////////////////////////////
// Events as per                             //
// https://docs.tmijs.org/v1.2.1/Events.html //
///////////////////////////////////////////////
client.on('message', onMessageHandler)
client.on('connected', onConnectedHandler)
client.on('disconnected', onDisconnectedHandler)

// Connect to Twitch:
client.connect()

//////////////////////
// Helper Functions //
//////////////////////
function PacificTime() {
  var today = new Date()
  var format = 'YYYY-MM-DD'
  return moment(today, format).tz('America/Los_Angeles').format(format)
}

function add_wotd(date, wotd, def) {
  console.log(`[WOTD] Date: ${date}`)

  const { spawnSync } = require('child_process'),
    populate = spawnSync('../dbdriver', ['--add', date, wotd, def])

  console.log(`[DB] stderr: ${populate.stderr.toString()}`);
  console.log(`[DB] stdout: ${populate.stdout.toString()}`);
}

///////////////////////////////////////////
// Called every time a message comes in //
///////////////////////////////////////////
function onMessageHandler (target, context, msg, self) {
  if (context.username === "fansachiye" || context.username === "sachiyek") {
    // Add WOTD to db automatically using regexes
    if (msg.includes("word of the day")) {
      // (Group 1) WOTD (Group 2) Definition
      // Find the WOTD by maching any character following 'day:'
      // until a closing ] is found.
      // Find the defintion by following the WOTD until
      // a ". @" or a '." @' is found
      var re = /.+the day:[ ]?(.+][ ]?)(.+\."?)[ ]?@.+/
      var match = re.exec(msg)
      if (match != null) {
        add_wotd(PacificTime(), match[1], match[2])
      } else {
        console.log(`[ERROR] Could not match against the regex`)
        console.log(`[ERROR] ${msg}`)
      }
    }
    // WOTD Commands
    else if (msg.includes("!wotd add")) {
        console.log('wotd add called')
        //TODO: Finish me
    }
    else if (msg.includes("!wotd del")) {
        console.log('wotd del called')
        //TODO: Finish me
    }
  }
  else return
}

// Called every time the bot connects to Twitch chat
function onConnectedHandler (addr, port) {
  console.log(`* Connected to ${addr}:${port}`)
}

// Called every time the bot disconnects from Twitch
function onDisconnectedHandler (reason) {
  console.log(`* Disconnected: ${reason}`)
  process.exit(1);
}
