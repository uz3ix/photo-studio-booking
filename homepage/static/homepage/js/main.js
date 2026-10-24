"use strict";
const backToTop = document.getElementById("back-to-top");
if (backToTop) {
  backToTop.hidden = false;
  backToTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "auto" }));
}
