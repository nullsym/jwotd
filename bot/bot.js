// https://docs.tmijs.org/v1.2.1/Configuration.html
// https://docs.tmijs.org/v1.2.1/Commands.html
// http://momentjs.com/timezone
var tmi = require('tmi.js')

// Global vars for the WOTD
var match1 = ""
var match2 = ""
var match3 = ""
debugging = process.argv[4] === "true" ? true : false

// Create an array with the channels we want to join
var channels = []
for (let i = 5; i < process.argv.length; i++) {
    channels.push(process.argv[i])
}

// Define configuration options
var options = {
    options: { debug: debugging },
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
function findRegex(re, msg) {
    var match = re.exec(msg)
    if (match != null) {
        if (match[1]) {
            console.log(`[MATCH1] ${match[1]}`)
            match1 = match[1]
        }
        if (match[2]) {
            console.log(`[MATCH2] ${match[2]}`)
            match2 = match[2]
        }
        if (match[3]) {
            console.log(`[MATCH3] ${match[3]}`)
            match3 = match[3]
        } else
            match3 = ""

        return true;
    } else
        return false;
}

function wotdAdd(wotd, romaji, def) {
    const { spawnSync } = require('child_process'),
        populate = spawnSync('../dbadd', [wotd, romaji, def])
    console.log(`[DB] stdout:\n${populate.stdout.toString()}`);
    console.log(`[DB] stderr:\n${populate.stderr.toString()}`);
    console.log(`[DB status]: ${populate.status.toString()}`);
}

///////////////////////////////////////////
// Called every time a message comes in //
///////////////////////////////////////////
function onMessageHandler (target, context, msg, self) {
    if (context.username === "fansachiye" || context.username === "sachiyek") {
        // Add WOTD to db automatically using regexes
        if (msg.includes("word of the day")) {
            // (Group 1) Japanese WOTD
            // (Group 2) Romaji
            // (Group 3) Everything else
            // Add '?' after a quantifier to make its match non-greedy
            var re = /.+the day:[ ]?(.+?[ ]?)\[(.+?)\][ ]?(.+)/
            if(findRegex(re, msg)) {
                client.say(channels[0], 'WOTD added')
                wotdAdd(match1, match2, match3)
                return
            }
            console.log(`[ERROR] Could not match against the regex: ${msg}`)
        }

        // Add WOTD explicitely
        else if (msg.includes("!wotd add")) {
            var re = /!wotd add {{(.+)}} {{(.+)}} {{(.+)}}/
            if(findRegex(re, msg)) {
                client.say(channels[0], 'WOTD added')
                wotdAdd(match1, match2, match3)
                return
            }
            console.log(`[ERROR] Could not match against the regex: ${msg}`)
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
