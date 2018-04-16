/*jshint esversion: 6 */
console.clear();

function pairwise(arr, arg) {
    let usedIndicies = [];

    for (let i = 0; i < arr.length; i++) {
        for (let j = 0; j < arr.length; j++) {

            if (arr[i] + arr[j] === arg && i !== j) {
                if (!usedIndicies.includes(i) && !usedIndicies.includes(j)) {
                    usedIndicies.push(i);
                    usedIndicies.push(j);
                }
            }
        }
    }

    if (usedIndicies.length !== 0) {
        return usedIndicies.reduce((a, b) => a + b);
    } else {
        return 0;
    }
}

let x = pairwise([], 100);
console.log(x);