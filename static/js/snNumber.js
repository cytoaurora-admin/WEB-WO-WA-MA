window.onload = function () {
    var snSelector = document.getElementById("serial_number")
    for (var i = 1; i <= 2; i++) {
        var option = document.createElement("option")
        option.value = i
        option.text = i
        snSelector.appendChild(option)
    }

    snSelector.addEventListener("change", function () {
        var n = parseInt(snSelector.value)
        var detectionCode = document.getElementById("detection_code").value // 從模板中獲取detection_code的值
        var detectionCodeArray = detectionCode.match(/.{1,2}/g) // 將detection_code每兩個字符分割成一個陣列
        var detectionCodeCount = detectionCodeArray.length // 計算陣列的長度
        if (!isNaN(n)) {
            n = n * detectionCodeCount // 將n乘以detectionCodeCount
            var container = document.getElementById("machine_container")
            container.innerHTML = "" // 清空容器
            for (var i = 1; i <= n; i++) {
                var div = document.createElement("div")
                div.innerHTML = `
                <br />
                <div class="row">
                    <div class="col-md-4">
                            <label for="machine${i}">序號${i} 機台：</label>
                            <select id="machine${i}" name="machine${i}" class="form-control">
                                <option value=""></option>
                                <option value="CR2-011">CR2-011</option>
                                <option value="CR2-012">CR2-012</option>
                                <option value="CR2-013">CR2-013</option>
                                <option value="CR2-014">CR2-014</option>
                                <option value="CR2-015">CR2-015</option>
                                <option value="CR5-004">CR5-004</option>                           
                                <option value="CR5-005">CR5-005</option>
                                <option value="CR5-006">CR5-006</option>
                            </select>
                    </div>
                    <div class="col-md-8">
                        <label>檢驗說明：</label>
                        <input id="comment${i}" name="comment${i}" class="form-control" type="text">
                    </div>
                </div>
            `
                container.appendChild(div)
            }
        }
    })
}
