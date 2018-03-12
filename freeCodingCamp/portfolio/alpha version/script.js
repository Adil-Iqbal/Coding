// javascript

function move(bar_id, skill) {
    let elem = document.getElementById(bar_id);
    let width = 1;
    let id = setInterval(frame, 10);

    function frame() {
        if (width >= skill) {
            clearInterval(id);
        } else {
            width += 2;
            elem.style.width = width + '%';
        }
    }
}

function updateBars() {
    move("python", 95);
    move("javascript", 84);
    move("javascript", 84);
    move("jquery", 64);
    move("sass", 76);
    move("css", 70);
    move("html", 66);
}

// jQuery
$(document).ready(function() {

    // Download the resume.
    $(".resume").click(function() {
        alert("Resume download goes here!")
    });

    let load_bars = true;
    $('#fullpage').fullpage({
        // Fill skill bars.
        afterLoad: function(index) {
            if ((index == 'technical_skills') && load_bars) {
                updateBars();
                load_bars = false;
            }
        },
        verticalCentered: true,
        controlArrows: false
    });
});
