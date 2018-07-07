//////////////// PAGE SETUP \\\\\\\\\\\\\\\\\\\\\\

const H1 = getPageParameters('h1');
const M1 = getPageParameters('m1');
const S1 = getPageParameters('s1');

const H2 = getPageParameters('h2');
const M2 = getPageParameters('m2');
const S2 = getPageParameters('s2');

const ACTIVITY_TIME = setTargetTime(H1, M1, S1);
const BREAK_TIME = setTargetTime(H2, M2, S2);

const DING = new Howl({
    src: ['ding.wav'],
    onend: function() { mute = false; }
})

let msPrevious = 0;
let msAccrued = 0;
let pulseDiameter = 288;
let paused = false;
let mute = true;
let canvas;

document.getElementsByClassName('togglePlayPause')[0]
    .addEventListener('click', function(event) {
        togglePlayPause();
    });

document.getElementsByClassName('refresh')[0]
    .addEventListener('click', function(event) {
        refresh();
    });

////////////////// BEGIN P5 SKETCH \\\\\\\\\\\\\\\\\\\\\

function setup() {
    canvas = createCanvas(350, 350);
    canvas.parent('#canvasContainer');
    angleMode(DEGREES);
}

function draw() {
    let msCurrent = millis();

    if (!paused) {
        let msElapsed = msCurrent - msPrevious;
        msAccrued += msElapsed;
    }

    // Constrain elapsed time to the duration of a single lap of the Pomodoro clock.
    msAccrued = msAccrued % (ACTIVITY_TIME + BREAK_TIME);

    background(0);
    translate(width / 2, height / 2);
    rotate(270);
    noFill();

    let activityTimeLeft, breakTimeLeft;
    if (msAccrued < ACTIVITY_TIME) {
        activityTimeLeft = ACTIVITY_TIME - msAccrued;
        breakTimeLeft = BREAK_TIME;
    } else {
        activityTimeLeft = 0;
        breakTimeLeft = BREAK_TIME - (msAccrued - ACTIVITY_TIME);
    }

    if (msAccrued <= 100 && !paused && !mute) {
        DING.play();
        DING.fade(1, 0.02, 1600);
        mute = true;
    }

    showPulse();

    showArc({
        totalTime: ACTIVITY_TIME,
        timeLeft: activityTimeLeft,
        weight: 16,
        diameter: 280,
        color: {
            r: 255,
            g: 0,
            b: 0
        }
    });

    showArc({
        totalTime: BREAK_TIME,
        timeLeft: breakTimeLeft,
        weight: 8,
        diameter: 260,
        color: {
            r: 0,
            g: 255,
            b: 0
        }
    });

    // Time Text Display
    rotate(-270);
    strokeWeight(0);
    stroke(255);
    fill(255);

    textAlign(CENTER, CENTER);
    textFont('Arvo');
    textSize(40);
    text(msToTime(activityTimeLeft), 0, -10);
    textSize(20);
    text(msToTime(breakTimeLeft), 0, 30);

    msPrevious = deepCopy(msCurrent);
}


// Draws the arcs that represent the time remaining.
function showArc(config) {
    if (config === undefined) {
        throw new Error('Arc configuration is missing.')
    }
    if (config.timeLeft === 0) {
        config.color.r = 0;
        config.color.g = 0;
        config.color.b = 0;
    }

    let angle = map(config.timeLeft, 0, config.totalTime, 0, 360);
    strokeWeight(config.weight);
    stroke(config.color.r, config.color.g, config.color.b);
    arc(0, 0, config.diameter, config.diameter, 0, angle);
}

// Gentle pulse to indicate a new lap has begun.
function showPulse() {
    if (msAccrued <= 500 && !paused) {
        strokeWeight(2);
        let alpha = map(pulseDiameter, 288, 350, 255, 0);
        stroke(255, 0, 0, alpha);
        ellipse(0, 0, pulseDiameter, pulseDiameter);
        if (pulseDiameter > 350) {
            pulseDiameter = 288;
        } else {
            pulseDiameter += 1.2;
        }
    } else {
        pulseDiameter = 288;
    }
}

function togglePlayPause(forcePause = false) {
    paused = forcePause ? true : !paused;
    let button = document.getElementsByClassName('togglePlayPause');
    if (paused) {
        button[0].innerHTML = `<i class="fas fa-play"></i>`;
    } else {
        button[0].innerHTML = `<i class="fas fa-pause"></i>`;
    }
}

function refresh() {
    msAccrued = 0;
    togglePlayPause(true);
}


////////////////  UTILITY FUNCTIONS  \\\\\\\\\\\\\\\\\\

function getPageParameters(pageParameter) {
    let allParameters = window.location.search.substring(1).split("&");
    for (param of allParameters) {
        param = param.split("=");
        if (param[0] === pageParameter) {
            let num = parseInt(param[1]);
            if (typeof num === "number" && !isNaN(num)) {
                return num;
            }
        }
    }
    return 0;
}

function setTargetTime(h, m, s) {
    if (h === 0 && m === 0 && s === 0) {
        s = 10;
    }
    return ((h * 3600) + (m * 60) + s) * 1000;
}

function msToTime(duration) {
    let s = parseInt((duration / 1000) % 60);
    let m = parseInt((duration / (1000 * 60)) % 60);
    let h = parseInt((duration / (1000 * 60 * 60)) % 24);

    h = (h < 10) ? "0" + h : h;
    m = (m < 10) ? "0" + m : m;
    s = (s < 10) ? "0" + s : s;

    return h + ":" + m + ":" + s;
}

function deepCopy(data) {
    return JSON.parse(JSON.stringify(data));
}

DING.play();
console.clear();