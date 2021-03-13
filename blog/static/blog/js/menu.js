const english = "<i class='flag-icon flag-icon-us'> </i>";
const spanish = "<i class='flag-icon flag-icon-es'> </i>";

$(document).ready(function() {
    const path = window.location.pathname;
    const lenguage = $("#lenguage");

    lenguage.empty();
    if (path.includes("/es")) {
      lenguage.attr("href", "/en/");
      lenguage.append(english);
    } else if (path.includes("/en")) {
      lenguage.attr("href", "/es/");
      lenguage.append(spanish);
    } else {
      lenguage.attr("href", "/en/");
      lenguage.append(english);
    }

    $("li.menu").each(function() {
        const elementPath = $(this.firstElementChild);
        if (elementPath.attr("href") === path) {
          $(this).addClass("active grey");
        } else {
          $(this).removeClass("active grey");
        }
    });

});
