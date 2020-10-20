const english = document.getElementById('english');
const spanish = document.getElementById('spanish');

english.addEventListener('click', function() {
  english.style.display = 'none';
  spanish.style.display = 'block';
});

spanish.addEventListener('click', function() {
  spanish.style.display = 'none';
  english.style.display = 'block';
});

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
