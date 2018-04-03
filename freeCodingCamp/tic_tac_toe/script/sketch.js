// const human = -1;
// const empty = 0;
// const computer = 1;
// let mounted = false;
// let games = [];
// let winConditions = [
//     [0, 1, 2],
//     [3, 4, 5],
//     [6, 7, 8],
//     [0, 3, 6],
//     [1, 4, 7],
//     [2, 5, 8],
//     [0, 4, 8],
//     [2, 4, 6]
// ]

let w = 800;
let h = 800;

let canvasBorder = new Border(w / 2, h / 2, w, h);
let mozaic = new QuadTree(canvasBorder, 2);

function setup() {
    createCanvas(w, h);
    for (i = 0; i < 50; i++) {
        let x = randomGaussian(w/2, w/10);
        let y = randomGaussian(h/2, h/10);
        let dot = new Dot(x, y);
        mozaic.store(dot);
    }
    background(0);
    mozaic.show();
}

// function draw() {
//     if (mounted) {
//         games.forEach(game => game.show());
//     }
// }

// function mousePressed() {
//     if (!mounted) {
//         mozaic.mount();
//         mounted = true;
//     } else {
//         games.forEach(game => game.clicked());
//     }
// }









/*
var games = [];
var human = -1;
var empty = 0;
var computer = 1;
var winConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


function setup() {
    console.clear()
    console.log("Chances to Blunder:")
    createCanvas(830, 220);
    noLoop();
    rectMode(CENTER);
    for (var i = 0; i <= 3; i++) {
        var size = floor(random(25, 200));
        var x = ((size * 1.167) / 2) + 10
        if (i > 0) {
            x += games[i - 1].bounds.posX
        }
        games[i] = new Board(i, x, 110, size);
        games[i].initialize();
        blunder = games[i].blunder * 100
        console.log((i + 1) + '.) ' + blunder.toFixed(2) + "%")
    }
    redraw();
}


function draw() {
    for (var i = 0; i < games.length; i++) {
        games[i].show()
    }
}


function mousePressed() {
    for (var i = 0; i < games.length; i++) {
        games[i].clicked()
    }
}
*/