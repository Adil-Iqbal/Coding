// Retrieves value of URL parameter.
function getPageParameters(pageParameter) {
    let allParameters = window.location.search.substring(1).split("&");
    for (param of allParameters) {
        param = param.split("=");
        if (param[0] == pageParameter) {
            param[1] = parseInt(param[1]);
            if (typeof param[1] === "number") {
                return param[1];
            }
        }
    }
    return 0;
}

// Retrieve time from URL.
const H1 = getPageParameters('h1');
const M1 = getPageParameters('m1');
const S1 = getPageParameters('s1');

const H2 = getPageParameters('h2');
const M2 = getPageParameters('m2');
const S2 = getPageParameters('s2');

// Function that sets the time constants.
function setTargetTime(h, m, s) {
    if (h === 0 && m === 0 & s === 0) {
        s = 10;
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

// Actually set the time constants.
const ACTIVITY_TIME = setTargetTime(H1, M1, S1);
const BREAK_TIME = setTargetTime(H2, M2, S2);

// Used to create deep copy of data.
function deepCopy(data) {
	return JSON.parse(JSON.stringify(data));
}

// Begin graphic rendering using P5.js
function setup() {
    createCanvas(400, 400);
    angleMode(DEGREES)
}


function draw() {
	let elapsed = millis();

    background(0);
    translate(width / 2, height / 2);

    rotate(270);
    strokeWeight(10);
    noFill();

    // Acivity Time Ring.
    stroke(255, 0, 0);
    let activityTimeLeft = ACTIVITY_TIME.difference - elapsed;
    let a = map(activityTimeLeft, 0, ACTIVITY_TIME.difference, 0, 360);
    arc(0, 0, 300, 300, 0, a);

    // Break Time Ring.
    // strokeWeight(10);
    // noFill();
    stroke(0, 255, 0);
    let breakTimeLeft = BREAK_TIME.difference - elapsed;
    let b = map(breakTimeLeft, 0, BREAK_TIME.difference, 0, 360);
    arc(0, 0, 280, 280, 0, b);

    // Time Text Display

    rotate(-270);
    strokeWeight(0);
    stroke(255);
    fill(255);

    textAlign(CENTER, CENTER);
    textFont('Arvo');
    textSize(40);
    text(ACTIVITY_TIME.text, 0, -10);
    textSize(20);
    text(BREAK_TIME.text, 0, 30);
}

