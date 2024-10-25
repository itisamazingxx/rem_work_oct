$(document).ready(function() {
    // 点击按钮触发文件上传input
    $('#btn-upload').on('click', function(event) {
        event.preventDefault(); 
        $('#fileInput').click();
    });

    // 当选择文件时自动上传
    $('#fileInput').on('change', function() {
        let file = this.files[0];
        if (file) {
            // 创建FormData对象，添加文件
            let formData = new FormData();
            formData.append('file', file);

            // Ajax请求
            $.ajax({
                url: '/upload_file', // 上传的Flask路由
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function(response) {
                    alert('success upload file');
                    location.reload();
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    alert('fail upload file');
                }
            });
        }
        // 重置文件输入框
        $('#fileInput').val('');
    });

    function updateTable(data) {
        const tableBody = $('#table-body'); // 假设你有一个表格体的ID为table-body
        tableBody.empty(); // 清空现有数据
    
        // 遍历返回的数据并添加到表格中
        data.forEach((item, index) => {
            tableBody.append(`
                <tr>
                    <td>${index + 1}</td> <!-- 使用 index 来显示行号 -->
                    <td>${item.Earner_Name}</td>
                    <td>${item.Earner_ID}</td>
                    <td>${item.Agent_Name}</td>
                    <td>${item.Agent_ID}</td>
                    <td>${item.Commission_Amount}</td>
                    <td>${item.Commission_Period}</td>
                    <td>${item.Carrier_Name}</td>
                    <td>${item.Enrollment_Type}</td>
                    <td>${item.Plan_Name}</td>
                    <td>${item.Member_Name}</td>
                    <td>${item.Member_ID}</td>
                    <td>${item.Effective_Date}</td>
                    <td>${item.Cycle_Year}</td>
                    <td>${item.Earner_Type}</td>
                </tr>
            `);
        });
    }

    // search
    $('#btn-search').on('click', function(event) {
        event.preventDefault(); // 阻止默认表单提交
        let searchKeyword = $('#search-input').val();
        let selectedOption = $('#select-opt').val();
        if (!searchKeyword || selectedOption === '0'){
            alert('please input keyword or select option');
            return;
        }
        $.ajax({
            url: '/1',
            method: 'POST',
            data: {
                option: selectedOption,
                keyword: searchKeyword
            },
            success: function(response) {
                updateTable(response.table_data)
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert('fail search file');
            }
        })
    });

    // export file
    $('#btn-export').on('click', function(event) {
        event.preventDefault();
        $.ajax({
            url: '/export_file',
            type: 'GET',
            success: function(response) {
                alert('success export file');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert('fail export file');
            }
        })
    });

    // find top
    function updateTable2(data) {
        const tableBody = $('#table-body2'); // 假设你有一个表格体的ID为table-body
        tableBody.empty(); // 清空现有数据
    
        // 遍历返回的数据并添加到表格中
        data.forEach((item, index) => {
            const totalCommission = item.total_commission.toFixed(2);
            tableBody.append(`
                <tr>
                    <td>${index + 1}</td> 
                    <td>${item.Name}</td>
                    <td>${totalCommission}</td>
                </tr>
            `);
        });
    }

    $('#btn-find-top').on('click', function(event) {
        event.preventDefault();
        let selectedOption = $('#select-opt2').val();
        if (selectedOption === '0'){
            alert('please select option');
            return;
        }
        $.ajax({
            url: '/analysis',
            method: 'POST',
            data: {
                option: selectedOption
            },
            success: function(response) {
                updateTable2(response.table_data)
            }
        })
    })
});
