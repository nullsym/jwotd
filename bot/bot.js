// https://docs.tmijs.org/v1.2.1/Configuration.html
// https://docs.tmijs.org/v1.2.1/Commands.html
// http://momentjs.com/timezone
const tmi = require('tmi.js')

// Global vars for the WOTD
let match1 = ""
let match2 = ""
let match3 = ""

// Define configuration options
const debugboolean = process.env.TWITCH_DEBUG === "true" ? true : false
const options = {
    options: { debug: debugboolean },
    connection: { reconnect: true, secure: true },
    identity: {
        username: process.env.TWITCH_USER,
        password: process.env.TWITCH_PASSWD
    },
    channels: [process.env.TWITCH_CHANNEL]
}

// Create a client with our options
const client = new tmi.client(options)

//////////////////////
// Helper Functions //
//////////////////////
function findRegex(re, msg) {
    let match = re.exec(msg)
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

// Called every time a message comes in
// https://docs.tmijs.org/v1.4.2/Events.html#chat
function onMessageHandler (channel, userobj, message, self) {
    // Allow only the streammer to add a WOTD
    if (userobj.username === channel.replace("#", "")) {

        // Add WOTD to db automatically using regular expressions
        if (message.includes("word of the day")) {
            // (Group 1) Japanese WOTD
            // (Group 2) Romaji
            // (Group 3) Everything else
            // Add '?' after a quantifier to make its match non-greedy
            let re = /.+the day:[ ]?(.+?[ ]?)\[(.+?)\][ ]?(.+)/
            if(findRegex(re, message)) {
                client.say(channel, 'WOTD added')
                wotdAdd(match1, match2, match3)
                return
            }
            console.log(`[ERROR] Could not match against the regex: ${message}`)
        }

        // Add WOTD explicitely
        else if (message.includes("!wotd add")) {
            let re = /!wotd add {{(.+)}} {{(.+)}} {{(.+)}}/
            if(findRegex(re, message)) {
                client.say(channel, 'WOTD added')
                wotdAdd(match1, match2, match3)
                return
            }
            console.log(`[ERROR] Could not match against the regex: ${message}`)
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

///////////////////////////////////////////////
// Events as per                             //
// https://docs.tmijs.org/v1.2.1/Events.html //
///////////////////////////////////////////////
client.on('message', onMessageHandler)
client.on('connected', onConnectedHandler)
client.on('disconnected', onDisconnectedHandler)

// Connect to Twitch:
client.connect()