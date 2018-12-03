// https://docs.tmijs.org/v1.2.1/Configuration.html
// https://docs.tmijs.org/v1.2.1/Commands.html
// http://momentjs.com/timezone
var tmi = require('tmi.js')
var moment = require('moment-timezone')


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
function PacificTime() {
    var today = new Date()
    var format = 'YYYY-MM-DD'
    return moment(today, format).tz('America/Los_Angeles').format(format)
}

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

function wotdAdd(date, wotd, def) {
    const { spawnSync } = require('child_process'),
        populate = spawnSync('../dbdriver', ['--add', date, wotd, def])

    console.log(`[DB] stderr: ${populate.stderr.toString()}`);
    console.log(`[DB] stdout: ${populate.stdout.toString()}`);
}

function wotdDel(date) {
    const { spawnSync } = require('child_process'),
        populate = spawnSync('../dbdriver', ['--delete', date])

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
            var re = /.+the day:[ ]?(.+][ ]?)(.+\."?)[ ]?/
            if(findRegex(re, msg)) {
                client.say(channels[0], 'Word of the day added')
                if (!debugging) wotdAdd(PacificTime(), match1, match2)
                return
            }
            console.log(`[ERROR] Could not match against the regex: ${msg}`)
        }

        // Add WOTD explicitely
        else if (msg.includes("!wotd add")) {
            // Assume current date
            var re = /!wotd add {{(.+)}} {{(.+)}}/
            if(findRegex(re, msg)) {
                client.say(channels[0], 'Word of the day added')
                if (!debugging) wotdAdd(PacificTime(), match1, match2)
                return
            }
            // If are given a date
            var re = /!wotd add (\d{4}-\d{2}-\d{2}) {{(.+)}} {{(.+)}}/
            if(findRegex(re, msg)) {
                client.say(channels[0], `Word of the day added [${match1}]`)
                if (!debugging) wotdAdd(match1, match2, match3)
                return
            }
            console.log(`[ERROR] Could not match against the regex: ${msg}`)
        }

        // Delete WOTD explicitely
        else if (msg.includes("!wotd del")) {
            var re = /!wotd del (\d{4}-\d{2}-\d{2})/
            // If we are given a date
            if(findRegex(re, msg)) {
                client.say(channels[0], 'Word of the day deleted')
                if (!debugging) wotdDel(match1)
                return
            }
            // When we are not given a date assume current date
            else {
                client.say(channels[0], 'Word of the day deleted')
                if (!debugging) wotdDel(PacificTime())
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
