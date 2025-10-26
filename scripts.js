// 获取DOM元素
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
const colorPicker = document.getElementById('colorPicker');
const lineWidth = document.getElementById('lineWidth');
const lineWidthValue = document.getElementById('lineWidthValue');
const clearCanvas = document.getElementById('clearCanvas');
const exportCanvas = document.getElementById('exportCanvas');

// 工具按钮
const toolButtons = document.querySelectorAll('.tool-btn');

// 绘画状态变量
let isDrawing = false;
let lastX = 0;
let lastY = 0;
let currentTool = 'pencil'; // 当前工具：pencil, eraser, circle, rectangle
let startX = 0;
let startY = 0;
let tempCanvas = document.createElement('canvas');
let tempCtx = tempCanvas.getContext('2d');

// 绘图历史记录，用于撤销功能
let drawingHistory = [];

// 初始化临时画布
function initTempCanvas() {
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    tempCtx.clearRect(0, 0, tempCanvas.width, tempCanvas.height);
}

// 设置画布大小
function resizeCanvas() {
    // 获取容器宽度
    const containerWidth = canvas.parentElement.clientWidth;
    // 保持16:9的宽高比
    const canvasHeight = Math.min(containerWidth * 9 / 16, 600);
    
    // 保存当前画布内容
    const saveCanvas = document.createElement('canvas');
    const saveCtx = saveCanvas.getContext('2d');
    saveCanvas.width = canvas.width;
    saveCanvas.height = canvas.height;
    saveCtx.drawImage(canvas, 0, 0);
    
    // 设置画布的实际大小
    canvas.width = containerWidth - 40; // 留出一些边距
    canvas.height = canvasHeight;
    
    // 确保画布的显示尺寸与实际尺寸一致
    canvas.style.width = `${canvas.width}px`;
    canvas.style.height = `${canvas.height}px`;
    
    // 清空画布
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 初始化临时画布
    initTempCanvas();
    
    // 恢复保存的内容（如果有绘图历史）
    if (drawingHistory.length > 0) {
        redrawCanvas();
    }
}

// 初始调整画布大小
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// 保存当前画布状态到历史记录
function saveToHistory() {
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    drawingHistory.push(imageData);
    // 限制历史记录数量，防止内存占用过大
    if (drawingHistory.length > 50) {
        drawingHistory.shift();
    }
}

// 撤销操作
function undoDrawing() {
    if (drawingHistory.length > 0) {
        drawingHistory.pop();
        redrawCanvas();
    }
}

// 重绘画布
function redrawCanvas() {
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    if (drawingHistory.length > 0) {
        ctx.putImageData(drawingHistory[drawingHistory.length - 1], 0, 0);
    }
}

// 开始绘画
function startDrawing(e) {
    isDrawing = true;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    [lastX, lastY] = [x, y];
    [startX, startY] = [x, y];
    
    // 保存当前状态到历史记录
    saveToHistory();
    
    // 初始化临时画布
    initTempCanvas();
    
    // 对于铅笔和橡皮擦工具，开始一个新路径
    if (currentTool === 'pencil' || currentTool === 'eraser') {
        tempCtx.beginPath();
        tempCtx.moveTo(x, y);
    }
}

// 绘画中
function draw(e) {
    if (!isDrawing) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    // 清除临时画布
    tempCtx.clearRect(0, 0, tempCanvas.width, tempCanvas.height);
    
    // 先确保临时画布背景为白色
    tempCtx.fillStyle = '#ffffff';
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
    
    // 如果有历史记录，复制到临时画布
    if (drawingHistory.length > 0) {
        tempCtx.putImageData(drawingHistory[drawingHistory.length - 1], 0, 0);
    }
    
    switch (currentTool) {
        case 'pencil':
            // 继续之前的路径，不重新beginPath
            tempCtx.lineTo(x, y);
            tempCtx.strokeStyle = colorPicker.value;
            tempCtx.lineWidth = lineWidth.value;
            tempCtx.lineCap = 'round';
            tempCtx.lineJoin = 'round';
            tempCtx.stroke();
            break;
            
        case 'eraser':
            // 继续之前的路径，不重新beginPath
            tempCtx.lineTo(x, y);
            tempCtx.strokeStyle = '#ffffff'; // 使用白色作为橡皮擦
            tempCtx.lineWidth = parseInt(lineWidth.value) * 2; // 橡皮擦稍微粗一些
            tempCtx.lineCap = 'round';
            tempCtx.lineJoin = 'round';
            tempCtx.stroke();
            break;
            
        case 'circle':
            // 计算半径
            const radius = Math.sqrt(Math.pow(x - startX, 2) + Math.pow(y - startY, 2));
            tempCtx.beginPath();
            tempCtx.arc(startX, startY, radius, 0, Math.PI * 2);
            tempCtx.strokeStyle = colorPicker.value;
            tempCtx.lineWidth = lineWidth.value;
            tempCtx.stroke();
            break;
            
        case 'rectangle':
            const width = x - startX;
            const height = y - startY;
            tempCtx.beginPath();
            tempCtx.rect(startX, startY, width, height);
            tempCtx.strokeStyle = colorPicker.value;
            tempCtx.lineWidth = lineWidth.value;
            tempCtx.stroke();
            break;
    }
    
    // 将临时画布内容绘制到主画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(tempCanvas, 0, 0);
    
    [lastX, lastY] = [x, y];
}

// 停止绘画
function stopDrawing() {
    if (!isDrawing) return;
    isDrawing = false;
    
    // 将最终结果保存到历史记录
    const currentState = ctx.getImageData(0, 0, canvas.width, canvas.height);
    drawingHistory[drawingHistory.length - 1] = currentState;
    
    // 结束路径（对于铅笔和橡皮擦）
    if (currentTool === 'pencil' || currentTool === 'eraser') {
        tempCtx.closePath();
    }
    
    // 清除临时画布
    tempCtx.clearRect(0, 0, tempCanvas.width, tempCanvas.height);
}

// 更新画笔粗细显示
function updateLineWidth() {
    lineWidthValue.textContent = `${lineWidth.value}px`;
}

// 切换工具
function switchTool(tool) {
    currentTool = tool;
    
    // 更新按钮状态
    toolButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tool === tool) {
            btn.classList.add('active');
        }
    });
    
    // 更新鼠标指针样式
    switch (tool) {
        case 'pencil':
            canvas.style.cursor = 'crosshair';
            break;
        case 'eraser':
            canvas.style.cursor = 'url("data:image/svg+xml,%3Csvg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" fill=\"none\"%3E%3Ccircle cx=\"10\" cy=\"10\" r=\"8\" stroke=\"%23000\" stroke-width=\"1\" fill=\"white\"/%3E%3C/svg%3E") 10 10, auto';
            break;
        case 'circle':
            canvas.style.cursor = 'crosshair';
            break;
        case 'rectangle':
            canvas.style.cursor = 'crosshair';
            break;
    }
}

// 清空画布
function handleClearCanvas() {
    if (confirm('确定要清空画板吗？')) {
        // 保存清空操作到历史记录
        saveToHistory();
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // 更新历史记录的最后一项为空画布
        const emptyState = ctx.getImageData(0, 0, canvas.width, canvas.height);
        drawingHistory[drawingHistory.length - 1] = emptyState;
    }
}

// 导出画布为图片
function handleExportCanvas() {
    // 创建下载链接
    const link = document.createElement('a');
    link.download = `drawing-${Date.now()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
}

// 移动设备支持 - 适配各种工具
function handleTouchStart(e) {
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    
    isDrawing = true;
    [lastX, lastY] = [x, y];
    [startX, startY] = [x, y];
    
    // 保存当前状态到历史记录
    saveToHistory();
    
    // 初始化临时画布
    initTempCanvas();
    
    // 对于铅笔和橡皮擦工具，开始一个新路径
    if (currentTool === 'pencil' || currentTool === 'eraser') {
        tempCtx.beginPath();
        tempCtx.moveTo(x, y);
    }
    
    e.preventDefault(); // 防止页面滚动
}

function handleTouchMove(e) {
    if (!isDrawing) return;
    
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    
    // 清除临时画布
    tempCtx.clearRect(0, 0, tempCanvas.width, tempCanvas.height);
    
    // 先确保临时画布背景为白色
    tempCtx.fillStyle = '#ffffff';
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
    
    // 如果有历史记录，复制到临时画布
    if (drawingHistory.length > 0) {
        tempCtx.putImageData(drawingHistory[drawingHistory.length - 1], 0, 0);
    }
    
    switch (currentTool) {
        case 'pencil':
            // 继续之前的路径，不重新beginPath
            tempCtx.lineTo(x, y);
            tempCtx.strokeStyle = colorPicker.value;
            tempCtx.lineWidth = lineWidth.value;
            tempCtx.lineCap = 'round';
            tempCtx.lineJoin = 'round';
            tempCtx.stroke();
            break;
            
        case 'eraser':
            // 继续之前的路径，不重新beginPath
            tempCtx.lineTo(x, y);
            tempCtx.strokeStyle = '#ffffff';
            tempCtx.lineWidth = parseInt(lineWidth.value) * 2;
            tempCtx.lineCap = 'round';
            tempCtx.lineJoin = 'round';
            tempCtx.stroke();
            break;
            
        case 'circle':
            const radius = Math.sqrt(Math.pow(x - startX, 2) + Math.pow(y - startY, 2));
            tempCtx.beginPath();
            tempCtx.arc(startX, startY, radius, 0, Math.PI * 2);
            tempCtx.strokeStyle = colorPicker.value;
            tempCtx.lineWidth = lineWidth.value;
            tempCtx.stroke();
            break;
            
        case 'rectangle':
            const width = x - startX;
            const height = y - startY;
            tempCtx.beginPath();
            tempCtx.rect(startX, startY, width, height);
            tempCtx.strokeStyle = colorPicker.value;
            tempCtx.lineWidth = lineWidth.value;
            tempCtx.stroke();
            break;
    }
    
    // 将临时画布内容绘制到主画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(tempCanvas, 0, 0);
    
    [lastX, lastY] = [x, y];
    e.preventDefault(); // 防止页面滚动
}

function handleTouchEnd() {
    if (!isDrawing) return;
    isDrawing = false;
    
    // 将最终结果保存到历史记录
    const currentState = ctx.getImageData(0, 0, canvas.width, canvas.height);
    drawingHistory[drawingHistory.length - 1] = currentState;
    
    // 结束路径（对于铅笔和橡皮擦）
    if (currentTool === 'pencil' || currentTool === 'eraser') {
        tempCtx.closePath();
    }
    
    // 清除临时画布
    tempCtx.clearRect(0, 0, tempCanvas.width, tempCanvas.height);
}

// 添加事件监听器
// 鼠标事件
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

// 触摸事件（移动设备支持）
canvas.addEventListener('touchstart', handleTouchStart);
canvas.addEventListener('touchmove', handleTouchMove);
canvas.addEventListener('touchend', handleTouchEnd);

// 工具栏事件
lineWidth.addEventListener('input', updateLineWidth);
clearCanvas.addEventListener('click', handleClearCanvas);
exportCanvas.addEventListener('click', handleExportCanvas);

// 工具按钮事件
toolButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        if (btn.dataset.tool === 'undo') {
            undoDrawing();
        } else {
            switchTool(btn.dataset.tool);
        }
    });
});

// 初始化显示画笔粗细
updateLineWidth();

// 初始化画布状态
ctx.fillStyle = '#ffffff';
ctx.fillRect(0, 0, canvas.width, canvas.height);
saveToHistory(); // 保存初始空白状态