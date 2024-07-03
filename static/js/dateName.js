function exportReport() {
    let date1 = document.getElementById("date1").value
    let date2 = document.getElementById("date2").value
    let reportName = `${date1}_${date2}_report`
    exportTableToCSV(reportName)
}
