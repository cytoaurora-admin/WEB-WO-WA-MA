document.addEventListener("DOMContentLoaded", function () {
    var woResult = document.getElementById("wo_result")
    var woExport = document.getElementById("wo_export")

    woResult.addEventListener("change", function () {
        woExport.value = this.value
    })
})
