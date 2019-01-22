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
// Add '?' after a on a quantifier to make its match non-greedy
var re = /.+the day:[ ]?(.+?[ ]?)\[(.+?)\][ ]?(.+)/

rl.on('line', (line) => {
    var match = re.exec(line)
    if (match != null) {
        console.log("[PASS]")
        // console.log(`Word: ${line}`)
        // console.log(`Match[1]: ${match[1]}`)
        // console.log(`Match[2]: ${match[2]}`)
        // console.log(`Match[3]: ${match[3]}\n`)
    }
    else {
        console.log("[FAIL]")
    }
});
