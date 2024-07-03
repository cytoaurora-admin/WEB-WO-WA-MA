document.addEventListener("DOMContentLoaded", function () {
    // 選擇所有的checkbox
    var checkboxes = document.querySelectorAll(".btn-check")

    // 為每個checkbox添加事件監聽器
    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            var values = []

            // 遍歷所有的checkbox，並將選中的checkbox的值添加到陣列中
            checkboxes.forEach(function (c) {
                if (c.checked) {
                    // 將每個值分解成兩位數字的陣列
                    for (var i = 0; i < c.value.length; i += 2) {
                        values.push(c.value.substring(i, i + 2))
                    }
                }
            })

            // 使用Set來移除重複的部分
            var uniqueValues = Array.from(new Set(values))

            // 將陣列排序並連接成一個字串
            var detection_code = uniqueValues.sort().join("")

            // 將字串賦值給detection_code的欄位
            document.getElementById("detection_code").value = detection_code
        })
    })
})
