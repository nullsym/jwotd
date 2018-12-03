// Test the regular expression against a wotd.txt

const readline = require('readline');
const fs = require('fs');
const rl = readline.createInterface({
  input: fs.createReadStream('test-regex.txt'),
  crlfDelay: Infinity
});

// (Group 1) WOTD (Group 2) Definition
// Find the WOTD by maching any character following 'day:'
// until a closing ] is found.
// Find the defintion by following the WOTD until
// a ". @" or a '." @' is found
// var re = /.+the day:[ ]?(.+][ ]?)(.+\."?)[ ]?@.+/
var re = /.+the day:[ ]?(.+][ ]?)(.+\."?)[ ]?/

rl.on('line', (line) => {
    var match = re.exec(line)
    if (match != null) {
        console.log("[PASS]")
        // console.log(`Match[1]: ${match[1]}`)
        // console.log(`Match[2]: ${match[2]}\n`)
    }
    else {
        console.log("[FAIL]")
    }
});
