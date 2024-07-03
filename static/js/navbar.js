document.addEventListener("DOMContentLoaded", function () {
    var currentUrl = window.location.pathname
    var navLinks = document.querySelectorAll(".navbar-nav .nav-item a")

    navLinks.forEach(function (link) {
        var linkUrl = link.getAttribute("href")
        if (currentUrl === linkUrl) {
            link.classList.add("active")
            link.parentElement.classList.add("active")
        }
    })
})
