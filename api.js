// 画板 JavaScript API
// 提供与Python API相同的功能接口
const apiCommandInput = document.getElementById('apiCommand');
const executeApiCommandBtn = document.getElementById('executeApiCommand');

// 复用scripts.js中已声明的变量: canvas, ctx, colorPicker, lineWidth

// 执行API命令
function executeApiCommand() {
    const command = apiCommandInput.value.trim();
    if (!command) {
        alert('请输入有效的API命令');
        return;
    }
    
    try {
        // 解析命令
        parseAndExecuteCommand(command);
        // 清空输入框
        apiCommandInput.value = '';
    } catch (error) {
        alert('命令执行出错: ' + error.message);
        console.error('API命令执行错误:', error);
    }
}

// 解析并执行命令
function parseAndExecuteCommand(command) {
    // 检查是否是draw命令
    if (command.startsWith('draw(') && command.endsWith(')')) {
        // 提取命令内容
        const content = command.substring(5, command.length - 1);
        
        // 解析参数
        const params = parseParams(content);
        
        if (params.length === 0) {
            throw new Error('无效的命令格式');
        }
        
        // 获取图形类型
        const shapeType = params[0].toLowerCase();
        
        // 根据图形类型执行相应的绘制函数
        switch (shapeType) {
            case 'line':
                drawLine(params.slice(1));
                break;
            case 'circle':
                drawCircle(params.slice(1));
                break;
            case 'rect':
                drawRectangle(params.slice(1));
                break;
            case 'text':
                drawText(params.slice(1));
                break;
            default:
                throw new Error('不支持的图形类型: ' + shapeType);
        }
    } else if (command.startsWith('export()')) {
        // 导出画布
        handleExportViaApi();
    } else {
        throw new Error('未知命令: ' + command);
    }
}

// 解析参数字符串
function parseParams(content) {
    const params = [];
    let currentParam = '';
    let inQuotes = false;
    let quoteChar = null;
    let bracketCount = 0;
    
    for (let i = 0; i < content.length; i++) {
        const char = content[i];
        
        // 处理引号
        if ((char === '"' || char === '\'') && content[i-1] !== '\\') {
            if (!inQuotes) {
                inQuotes = true;
                quoteChar = char;
            } else if (char === quoteChar) {
                inQuotes = false;
            }
            currentParam += char;
        } else if (char === ',' && !inQuotes && bracketCount === 0) {
            // 遇到逗号且不在引号内，并且括号平衡，结束当前参数
            params.push(cleanParam(currentParam));
            currentParam = '';
        } else {
            // 其他字符直接添加
            currentParam += char;
        }
    }
    
    // 添加最后一个参数
    if (currentParam.trim()) {
        params.push(cleanParam(currentParam));
    }
    
    return params;
}

// 清理参数值
function cleanParam(param) {
    param = param.trim();
    
    // 如果是字符串，去掉引号
    if ((param.startsWith('"') && param.endsWith('"')) || 
        (param.startsWith('\'') && param.endsWith('\''))) {
        return param.substring(1, param.length - 1);
    }
    
    // 如果是数字，转换为数字类型
    if (!isNaN(param) && isFinite(param)) {
        return parseFloat(param);
    }
    
    return param;
}

// 绘制直线
function drawLine(params) {
    if (params.length !== 4) {
        throw new Error('绘制直线需要4个参数: x1, y1, x2, y2');
    }
    
    const [x1, y1, x2, y2] = params;
    
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.strokeStyle = colorPicker.value;
    ctx.lineWidth = lineWidth.value;
    ctx.lineCap = 'round';
    ctx.stroke();
}

// 绘制圆形
function drawCircle(params) {
    if (params.length !== 3) {
        throw new Error('绘制圆形需要3个参数: x, y, radius');
    }
    
    const [x, y, radius] = params;
    
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.strokeStyle = colorPicker.value;
    ctx.lineWidth = lineWidth.value;
    ctx.stroke();
}

// 绘制矩形
function drawRectangle(params) {
    if (params.length !== 4) {
        throw new Error('绘制矩形需要4个参数: x, y, width, height');
    }
    
    const [x, y, width, height] = params;
    
    ctx.beginPath();
    ctx.rect(x, y, width, height);
    ctx.strokeStyle = colorPicker.value;
    ctx.lineWidth = lineWidth.value;
    ctx.stroke();
}

// 绘制文本
function drawText(params) {
    if (params.length !== 3) {
        throw new Error('绘制文本需要3个参数: x, y, text');
    }
    
    const [x, y, text] = params;
    
    ctx.font = '20px Arial';
    ctx.fillStyle = colorPicker.value;
    ctx.fillText(text, x, y);
}

// 通过API导出画布
function handleExportViaApi() {
    // 创建下载链接
    const link = document.createElement('a');
    link.download = `drawing-${Date.now()}.png`;
    const canvasElement = document.getElementById('drawingCanvas');
    link.href = canvasElement.toDataURL('image/png');
    link.click();
}

// 公开的API方法，供外部调用
window.DrawingAPI = {
    // 绘制直线
    drawLine: function(x1, y1, x2, y2, color = null, width = null) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = color || colorPicker.value;
        ctx.lineWidth = width || lineWidth.value;
        ctx.lineCap = 'round';
        ctx.stroke();
        return true;
    },
    
    // 绘制圆形
    drawCircle: function(x, y, radius, color = null, width = null) {
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.strokeStyle = color || colorPicker.value;
        ctx.lineWidth = width || lineWidth.value;
        ctx.stroke();
        return true;
    },
    
    // 绘制矩形
    drawRectangle: function(x, y, width, height, color = null, lineWidth = null) {
        ctx.beginPath();
        ctx.rect(x, y, width, height);
        ctx.strokeStyle = color || colorPicker.value;
        ctx.lineWidth = lineWidth || window.lineWidth.value;
        ctx.stroke();
        return true;
    },
    
    // 绘制文本
    drawText: function(x, y, text, color = null, fontSize = 20) {
        ctx.font = `${fontSize}px Arial`;
        ctx.fillStyle = color || colorPicker.value;
        ctx.fillText(text, x, y);
        return true;
    },
    
    // 导出画布
    export: function() {
        handleExportViaApi();
        const canvasElement = document.getElementById('drawingCanvas');
        return canvasElement.toDataURL('image/png');
    },
    
    // 清空画布
    clear: function() {
        const canvasElement = document.getElementById('drawingCanvas');
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvasElement.width, canvasElement.height);
        return true;
    },
    
    // 设置画笔颜色
    setColor: function(color) {
        colorPicker.value = color;
        return true;
    },
    
    // 设置画笔粗细
    setLineWidth: function(width) {
        lineWidth.value = width;
        document.getElementById('lineWidthValue').textContent = `${width}px`;
        return true;
    },
    
    // 执行命令字符串
    executeCommand: function(command) {
        try {
            parseAndExecuteCommand(command);
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
};

// 添加执行按钮事件监听
executeApiCommandBtn.addEventListener('click', executeApiCommand);

// 添加回车键执行命令
apiCommandInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        executeApiCommand();
    }
});