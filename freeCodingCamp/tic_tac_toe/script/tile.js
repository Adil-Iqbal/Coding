class Tile {
    constructor(index, parent, x, y) {
        this.index = index;
        this.parent = parent;
        this.x = x;
        this.y = y;
        this.state = empty;
        this.w = this.parent.w / 3;
        this.h = this.parent.h / 3;
        this.bounds = {
            posX: this.x + (this.w / 2),
            negX: this.x - (this.w / 2),
            posY: this.y + (this.h / 2),
            negY: this.y - (this.h / 2)
        };
        this.humanSymbol = "X";
        this.compSymbol = "O";
    }

    clicked() {
        if (mouseX < this.bounds.posX && mouseX > this.bounds.negX && mouseY < this.bounds.posY && mouseY > this.bounds.negY) {
            if (this.state == empty && this.parent.turn == human) {
                this.state = human;
                this.parent.switchTurn();
            }
        }
    };

    show(col) {
        fill(255);
        noStroke();
        rect(this.x, this.y, this.parent.w / 3, this.parent.h / 3);

        push();
        fill(col.r, col.g, col.b);
        translate(this.x - this.parent.w / 8, this.y + this.parent.h / 8);
        textSize(this.parent.w / 3);
        if (this.state == human) {
            text(this.humanSymbol, 0, 0);
        } else if (this.state == computer) {
            text(this.compSymbol, 0, 0);
        }
        pop();
    };

    setSymbol() {
        if (this.parent.swapSymbols) {
            this.humanSymbol = "O";
            this.compSymbol = "X";
        }
    };
}