$(document).ready(function() {
    $("li.menu").each(function() {
        const path = window.location.href;
        const elementPath = this.firstElementChild.href;
        if (elementPath === path) {
            $(this).addClass("active grey");
        } else {
            $(this).removeClass("active grey");
        }
    });
});
