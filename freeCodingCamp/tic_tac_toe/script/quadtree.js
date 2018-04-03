class QuadTree {
    constructor(border, capacity) {
        this.capacity = capacity;
        this.border = border;
        this.dots = [];
        this.northwest = undefined;
        this.northeast = undefined;
        this.southwest = undefined;
        this.southeast = undefined;
        this.game = undefined;
    }

    show() {
        this.border.show();
        this.dots.forEach(dot => dot.show());
        if (this.northwest !== undefined) {
            this.northwest.show();
            this.northeast.show();
            this.southwest.show();
            this.southeast.show();
        }
    }

    branch() {
        let x = this.border.x;
        let y = this.border.y;
        let w = this.border.w;
        let h = this.border.h;

        let NW_Border = new Border(x - w / 4, y - h / 4, w / 2, h / 2);
        let NE_Border = new Border(x + w / 4, y - h / 4, w / 2, h / 2);
        let SW_Border = new Border(x - w / 4, y + h / 4, w / 2, h / 2);
        let SE_Border = new Border(x + w / 4, y + h / 4, w / 2, h / 2);

        this.northwest = new QuadTree(NW_Border, this.capacity);
        this.northeast = new QuadTree(NE_Border, this.capacity);
        this.southwest = new QuadTree(SW_Border, this.capacity);
        this.southeast = new QuadTree(SE_Border, this.capacity);

    }

    store(dot) {
        // Ignore all dots that do not belong here.
        if (!this.border.contains(dot)) {
            return false;
        }

        // If there is space, add the dot here.
        if (this.dots.length < this.capacity) {
            this.dots.push(dot);
            return true;
        }

        // Otherwise, subdivide and add it to whichever child will accept it.
        if (this.northwest === undefined) {
            this.branch();
        }
        if (this.northwest.store(dot)) {
            return true;
        }
        if (this.northeast.store(dot)) {
            return true;
        }
        if (this.southwest.store(dot)) {
            return true;
        }
        if (this.southeast.store(dot)) {
            return true;
        }

        // Otherwise, this point cannot be inserted...
        return false;
    }
    
    mount() {
        if (this.northwest !== undefined) {
            this.northwest.mount();
            this.northeast.mount();
            this.southwest.mount();
            this.southeast.mount();
        } else {
            // Set this.game as a tic-tac-toe board.
        }
    }
}