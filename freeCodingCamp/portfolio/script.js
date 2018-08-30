

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
