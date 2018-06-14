/*
1. Figure out time metric.
2. Figure out arc display (map to mouse at first);  
*/
const TIME = setTargetTime();
console.log(TIME);

function setup() {
    createCanvas(400, 400);
    angleMode(DEGREES)
}


function draw() {
    background(0);
    translate(width / 2, height / 2);


    rotate(270);
    strokeWeight(10);
    noFill();

    // Acivity Time Ring.
    stroke(255, 0, 0);
    let a = map(mouseX, 0, width, 360, 0);
    arc(0, 0, 300, 300, 0, a);

    // Break Time Ring.
    // strokeWeight(10);
    // noFill();
    stroke(0, 255, 0);
    let b = map(mouseY, 0, width, 0, 360);
    arc(0, 0, 280, 280, 0, b);

    // Time Text Display

    rotate(-270);
    strokeWeight(0);
    stroke(255);
    fill(255);

    textAlign(CENTER, CENTER);
    textFont('Arvo');
    textSize(40);
    text(TIME.text, 0, 0);


}


function setTargetTime(h = 0, m = 0, s = 0) {
    if (h === 0 && m === 0 & s === 0) {
        s = 15;
    }
    while (s >= 60) {
        s = s - 60;
        m++;
    }
    while (m >= 60) {
        m = m - 60;
        h++;
    }
    if (h > 99) {
        h = 99;
    }

    function textify(n) {
        n = n.toString();
        if (n.length === 1) {
            n = `0${n}`;
        }
        return n;
    }

    let now = Date.now();
    let diff = (s * 1000) + (m * 60000) + (h * 360000);
    return {
    	hours: h,
    	minutes: m,
    	seconds: s,
        text: `${textify(h)}:${textify(m)}:${textify(s)}`,
        now: now,
        difference: diff,
        target: now + diff
    }
}