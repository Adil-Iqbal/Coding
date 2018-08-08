// setTimeout(function() {
//     $('nav').addClass('navBarReady');
// }, 1500);


let mobileMode = false;

function toggleMobileMode() {
    if ($(window).width() < 500) {
        mobileMode = true;
    } else {
        mobileMode = false;
    }
}


$(document).ready(function() {
    toggleMobileMode()
    $(window).on('resize', () => {
    
        
    });



    $(document).on('click', event => {
        let classes = event.target.className.split(' ');
        if (classes.includes('navLink')) {
            $('.navLink').removeClass('active');
            $(event.target).addClass('active');
        }
    });
})