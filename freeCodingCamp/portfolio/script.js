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
    let wait = 1000;
    move("python", 95);
    setTimeout(move("javascript", 84), wait);
    setTimeout(move("javascript", 84), wait);
    setTimeout(move("jquery", 64), wait);
    setTimeout(move("sass", 76), wait);
    setTimeout(move("css", 70), wait);
    setTimeout(move("html", 66), wait);
    // setTimeout(, wait);
}

// jQuery
$(document).ready(function() {

    // Download the resume.
    $(".resume").click(function() {
        alert("Resume download goes here!")
    });

    // Smooth scrolling.
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();

        var target = this.hash;
        var $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top
        }, 900, 'swing', function() {
            window.location.hash = target;
        });
    });

    // Trigger skill bar animation.

    let load_bars = true;
    $(window).on('resize scroll', function() {
        if ($('#skill_bars').visible() && load_bars) {
            updateBars();
            load_bars = false;
        }
    });
});
