let data = [];
let m, b;

const learningRate = 0.01;
const optimizer = tf.train.sgd(learningRate, );

class Dot {
    constructor(x_, y_) {
        this.p5 = {
            x: x_,
            y: y_
        };
        this.tf = {
            x: map(x_, 0, width, 0, 1),
            y: map(y_, 0, height, 1, 0) //inverted.
        }
    }
}

function setup() {
    createCanvas(400, 400);
    m = tf.scalar(random(1)).variable();
    b = tf.scalar(random(1)).variable();
}

function mousePressed() {
    let dot = new Dot(mouseX, mouseY);
    data.push(dot);
}

function draw() {
    background(0);
    stroke(255);

    if (data.length > 0) {
        optimizer.minimize(() => {
            
                // Convert data to seperate X and Y tensors.	
                const X = tf.tensor1d(data.map(dot => dot.tf.x));
                const Y = tf.tensor1d(data.map(dot => dot.tf.y));
                return loss(predict(X), Y);
           
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
        const LINE_X = [0, 1];
        const LINE_Y = predict(tf.tensor1d(LINE_X));
        const LINE_Y_DATA = LINE_Y.dataSync();

        let x1 = map(LINE_X[0], 0, 1, 0, width);
        let x2 = map(LINE_X[1], 0, 1, 0, width);
        let y1 = map(LINE_Y_DATA[0], 0, 1, height, 0);
        let y2 = map(LINE_Y_DATA[1], 0, 1, height, 0);

        line(x1, y1, x2, y2);
    });
}

function loss(prediction, label) {
    // Mean squared error
    return prediction.sub(label).square().mean();
}

function predict(input) {
    // y = mx + b
    return input.mul(m).add(b);
}