class Dot {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    show() {
        strokeWeight(4);
        stroke(64, 224, 208);
        point(this.x, this.y);
    }
}