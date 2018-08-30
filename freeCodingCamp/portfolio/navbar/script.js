let mobileMode = false;
let mobileMenuPosition = false;

function toggleMobileMode() {
    if ($(window).width() < 500) {
        mobileMode = true;
    } else {
        mobileMode = false;
    }
}

function toggleNavBehavior() {
    if (mobileMode) {
        $('nav').removeClass('navBarReady');
    } else {
        setTimeout(() => {
            $('nav').addClass('navBarReady');
        }, 1500)
    }
}

function dropMobileMenu() {
    $('#toggleNav').html('<i class="fas fa-times toggleNav"></i>');
    $('nav').addClass('navBarReady');
    $('#overlay').css('display', 'block');
    mobileMenuPosition = true;
}

function liftMobileMenu() {
    $('#toggleNav').html('<i class="fas fa-bars toggleNav"></i>');
    $('nav').removeClass('navBarReady');
    $('#overlay').css('display', 'none');
    mobileMenuPosition = false;
}

$(document).ready(function() {
    toggleMobileMode()
    toggleNavBehavior()
    $(window).on('resize', () => {
        toggleMobileMode()
        toggleNavBehavior()
    });

    $(document).on('click', event => {
        let id = event.target.id
        let classes = event.target.className.split(' ');
        // Mobile Only
        if (mobileMode && (id === 'toggleNav' || classes.includes('toggleNav'))) {
            if (mobileMenuPosition) {
                liftMobileMenu();
            } else {
                dropMobileMenu();
            }
        }
        // Nav Links
        if (classes.includes('navLink')) {
            $('.navLink').removeClass('active');
            $(event.target).addClass('active');
        }
    });
})