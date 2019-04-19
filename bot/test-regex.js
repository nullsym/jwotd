// Test the regular expression against a wotd.txt

const readline = require('readline');
const fs = require('fs');
const rl = readline.createInterface({
  input: fs.createReadStream('test-regex.txt'),
  crlfDelay: Infinity
});

// Find the WOTD by maching any character following 'day:'
// (Group 1) Japanese WOTD
// (Group 2) Romaji
// (Group 3) Everything else
// Add '?' after a quantifier to make its match non-greedy
let re = /.+the day:[ ]?(.+?[ ]?)\[(.+?)\][ ]?(.+)/

rl.on('line', (line) => {
    let match = re.exec(line)
    if (match != null) {
        console.log("[PASS]")
    }
    else {
        console.log(`[FAIL] ${line}`)
    }
});
