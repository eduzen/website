document.addEventListener("DOMContentLoaded", function() {
  let dropdown = document.querySelector(".absolute.right-0.z-20.mt-2");
  let button = document.querySelector("button.language-dropdown");

  document.addEventListener("click", function(event) {
      // Check if the dropdown and button exist and if the clicked element is not the dropdown or the button
      if (dropdown && button && !dropdown.contains(event.target) && !button.contains(event.target) && dropdown.style.display !== "none") {
          dropdown.style.display = "none";
      }
  });

  const mobileButton = document.getElementById("mobile-menu-button");
  const mobileMenu = document.getElementById("mobile-menu");

  if (mobileButton && mobileMenu) {
      mobileButton.addEventListener("click", function() {
          mobileMenu.style.display = mobileMenu.style.display === "none" ? "block" : "none";
      });
  }
});
