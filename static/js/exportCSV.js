function downloadCSV(csv, filename) {
    var csvFile
    var downloadLink

    // 添加 UTF-8 BOM
    var BOM = "\uFEFF"
    csv = BOM + csv

    // CSV 文件
    csvFile = new Blob([csv], { type: "text/csv;charset=utf-8;" })

    // 下載链接
    downloadLink = document.createElement("a")

    // 文件名稱
    downloadLink.download = filename

    // 創建一個鏈接到文件
    downloadLink.href = window.URL.createObjectURL(csvFile)

    // 隱藏下載鏈接
    downloadLink.style.display = "none"

    // 將下載鏈接添加到網頁
    document.body.appendChild(downloadLink)

    // 點擊下載鏈接
    downloadLink.click()
}

function exportTableToCSV(filename = "data.csv") {
    var csv = []
    var rows = document.getElementById("result").querySelectorAll("tr")

    // 遍历表格的每一行，提取数据并添加到CSV数组中
    for (var i = 0; i < rows.length; i++) {
        var row = []
        var cols = rows[i].querySelectorAll("td, th")

        for (var j = 0; j < cols.length; j++) {
            // 將所有的逗號 (',') 轉換為全形逗號 ('，')
            var text = cols[j].innerText.replace(/,/g, "，")
            row.push(text)
        }

        csv.push(row.join(","))
    }

    // 调用downloadCSV函数以下载CSV文件
    downloadCSV(csv.join("\n"), filename)
}
