window.onload = function () {
    var nubTube = document.getElementById("nub_tube")
    nubTube.addEventListener("change", function () {
        var n = parseInt(nubTube.value)
        if (!isNaN(n)) {
            var container = document.getElementById("tube_container")
            container.innerHTML = "" // 清空容器
            for (var i = 1; i <= n; i++) {
                var div = document.createElement("div")
                div.innerHTML = `
                <br />
                <div class="form-inline">
                    <label for="quota${i}">管${i} 可實驗次數：30 / 種類：</label>
                    <select id="tube_type${i}" name="tube_type${i}" class="form-control" required>
                        <option value="">請選擇</option>
                        <option value="yellow">黃頭管</option>
                        <option value="camouflage">迷彩管</option>
                        <option value="200ul_tube">200µL Tube</option>
                    </select>
                </div>    
            `
                container.appendChild(div)
            }
        }
    })
}
