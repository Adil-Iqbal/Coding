let data = [];
let a, b, c, d;

let canvas;
let lrSlider, lrP;
let polyP, lossP;
let clearB, randomizeB;
let polyS, optimizerS;

let learningRate = 0.02;
let optimizer = tf.train.sgd(learningRate);

class Dot {
    constructor(x_, y_, invertMapping = false) {
        if (invertMapping) {
            this.p5 = {
                x: map(x_, -1, 1, 0, width),
                y: map(y_, -1, 1, height, 0)
            };
            this.tf = {
                x: x_,
                y: y_
            }
        } else {
            this.p5 = {
                x: x_,
                y: y_
            };
            this.tf = {
                x: map(x_, 0, width, -1, 1),
                y: map(y_, 0, height, 1, -1)
            }
        }
    }
}

function loadData(a_ = 0, b_ = 0, c_ = 0, d_ = 0) {
    function f(x) {
        return (a_ * x ** 3) + (b_ * x ** 2) + (c_ * x) + d_;
    }

    data = [];
    for (let x = -1; x < 1.1; x += 0.1) {
        let dot = new Dot(x, f(x), invertMapping = true);
        data.push(dot);
    }

}

function loadPoly() {
    let a = 0;
    let b = 0;
    let c = 0;
    let d = 0;
    switch (polyS.value()) {
        case 'None':
            data = [];
            return;
        case 'Cubic (Simple)':
            a = 1;
            break;
        case 'Cubic (Random)':
            a = random(-1, 1);
            b = random(-1, 1);
            c = random(-1, 1);
            d = random(-1, 1);
            break;
        case 'Quadratic (Simple)':
            b = 1.8;
            d = -0.8;
            break;
        case 'Quadratic (Random)':
            b = random(-1, 1);
            c = random(-1, 1);
            d = random(-1, 1);
            break;
        case 'Linear (Simple)':
            c = 1;
            break;
        case 'Linear (Random)':
            c = random(-1, 1);
            d = random(-1, 1);
            break;
        case 'Constant (Simple)':
            break;
        case 'Constant (Random)':
            d = random(-1, 1);
            break;
        default:
            break;
    }

    loadData(a, b, c, d);
}

function setOptimizer(learningRate) {
    switch (optimizerS.value()) {
        case 'SGD':
            optimizer = tf.train.sgd(learningRate);
            break;
        case 'Adam':
            optimizer = tf.train.adam(learningRate);
            break;
        case 'Momentum':
            optimizer = tf.train.momentum(learningRate, 1);
            break;
        case 'Adaptive Gradient':
            optimizer = tf.train.adagrad(learningRate);
            break;
    }
}

function randomizeCurve() {
    a = tf.scalar(random(-1, 1)).variable();
    b = tf.scalar(random(-1, 1)).variable();
    c = tf.scalar(random(-1, 1)).variable();
    d = tf.scalar(random(-1, 1)).variable();
}

function setup() {
    canvas = createCanvas(340, 340);
    canvas.parent('#canvasContainer');

    lrSlider = createSlider(0, 0.5, 0.15, 0.001);
    lrSlider.parent('#lrSlider');

    lrP = createP(`Learning Rate: ${learningRate}`);
    lrP.parent('#lrP');

    polyP = createP('');
    polyP.parent('#polynomial');

    lossP = createP('Click on canvas to add data points.');
    lossP.parent('#loss');

    clearB = createButton('Clear Data');
    clearB.mousePressed(() => { data = [] });
    clearB.parent('#clearButton');

    randomizeB = createButton('Randomize Curve');
    randomizeB.mousePressed(randomizeCurve);
    randomizeB.parent('#randomizeCurve');

    polyS = createSelect();
    polyS.changed(loadPoly);
    polyS.option('None');
    polyS.option('Constant (Simple)');
    polyS.option('Linear (Simple)');
    polyS.option('Quadratic (Simple)');
    polyS.option('Cubic (Simple)');
    polyS.option('Constant (Random)');
    polyS.option('Linear (Random)');
    polyS.option('Quadratic (Random)');
    polyS.option('Cubic (Random)');
    polyS.parent('#polyDataset');

    optimizerS = createSelect();
    optimizerS.option('SGD');
    optimizerS.option('Adam');
    optimizerS.option('Momentum');
    optimizerS.option('Adaptive Gradient');
    optimizerS.parent('#optimizer');

    randomizeCurve();
}

function mousePressed() {
    if (mouseX < width && mouseX > 0 && mouseY < height && mouseY > 0) {
        let dot = new Dot(mouseX, mouseY);
        data.push(dot);
    }
}

function draw() {
    learningRate = lrSlider.value();
    setOptimizer(learningRate);

    lrP.html(`Learning Rate: ${learningRate}`);

    let aText = a.dataSync()[0].toFixed(3);
    let bText = b.dataSync()[0].toFixed(3);
    let cText = c.dataSync()[0].toFixed(3);
    let dText = d.dataSync()[0].toFixed(3);

    polyP.html(`<h3><b>y</b> = ${aText}<b>x<sup>3</sup></b> + ${bText}<b>x<sup>2</sup></b> + ${cText}<b>x</b> + ${dText}</h3>`);

    background(0);
    stroke(255);

    if (data.length > 0) {
        optimizer.minimize(() => {
            // Convert data to seperate X and Y tensors.	
            const X = tf.tensor1d(data.map(dot => dot.tf.x));
            const Y = tf.tensor1d(data.map(dot => dot.tf.y));
            let loss_ = loss(predict(X), Y);
            let lossText = loss_.dataSync()[0] * 100;
            lossP.html(`Loss &asymp; ${lossText.toFixed(4)}%`);

            return loss_;
        })
    } else {
        stroke(0);
        // text()
    }

    // Draw data points.
    strokeWeight(4);
    for (dot of data) {
        point(dot.p5.x, dot.p5.y);
    }

    // Draw predictive line.
    tf.tidy(() => {
        let xs = [];
        for (let x = -1; x < 1.05; x += 0.05) {
            xs.push(x);
        }
        let ys = predict(tf.tensor1d(xs)).dataSync();
        let curve = [];
        for (let i = 0; i < xs.length; i++) {
            curve.push(new Dot(xs[i], ys[i], invertMapping = true));
        }

        stroke(64, 224, 208);
        strokeWeight(2);
        noFill();
        beginShape();
        for (dot of curve) {
            vertex(dot.p5.x, dot.p5.y);
        }
        endShape();
    });

    if (data.length === 0) {
    	stroke(255);
    	strokeWeight(1);
    	text('Click here to add data points!', width/2 - 80, height/2);
    }
}

function loss(prediction, label) {
    // Mean squared error
    return prediction.sub(label).square().mean();
}

function predict(x) {
    // y = ax^3 + bx^2 + cx + d
    return a.mul(x.pow(tf.scalar(3))).add(b.mul(x.square())).add(c.mul(x)).add(d);
}