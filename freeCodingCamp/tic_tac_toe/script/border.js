class Border {
    constructor(x, y, w, h) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
    }

    contains(dot) {
        return (dot.x <= this.x + this.w / 2 &&
            dot.x > this.x - this.w / 2 &&
            dot.y <= this.y + this.h / 2 &&
            dot.y > this.y - this.h / 2);
    }

    show() {
        rectMode(CENTER);
        strokeWeight(1);
        stroke(255, 255, 255, Math.floor(255 / 2));
        noFill();
        rect(this.x, this.y, this.w, this.h);
    }
}
