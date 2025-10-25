// 获取DOM元素
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
const colorPicker = document.getElementById('colorPicker');
const lineWidth = document.getElementById('lineWidth');
const lineWidthValue = document.getElementById('lineWidthValue');
const clearCanvas = document.getElementById('clearCanvas');
const exportCanvas = document.getElementById('exportCanvas');

// 设置画布大小
function resizeCanvas() {
    // 获取容器宽度
    const containerWidth = canvas.parentElement.clientWidth;
    // 保持16:9的宽高比
    const canvasHeight = Math.min(containerWidth * 9 / 16, 600);
    
    // 设置画布的实际大小
    canvas.width = containerWidth - 20; // 留出一些边距
    canvas.height = canvasHeight;
    
    // 清空画布
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// 初始调整画布大小
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// 绘画状态变量
let isDrawing = false;
let lastX = 0;
let lastY = 0;

// 开始绘画
function startDrawing(e) {
    isDrawing = true;
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

// 绘画中
function draw(e) {
    if (!isDrawing) return;
    
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.strokeStyle = colorPicker.value;
    ctx.lineWidth = lineWidth.value;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.stroke();
    
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

// 停止绘画
function stopDrawing() {
    isDrawing = false;
}

// 更新画笔粗细显示
function updateLineWidth() {
    lineWidthValue.textContent = `${lineWidth.value}px`;
}

// 清空画布
function handleClearCanvas() {
    if (confirm('确定要清空画板吗？')) {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
}

// 导出画布为图片
function handleExportCanvas() {
    // 创建下载链接
    const link = document.createElement('a');
    link.download = `ai-drawing-${Date.now()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
}

// 移动设备支持
function handleTouchStart(e) {
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    
    isDrawing = true;
    [lastX, lastY] = [x, y];
    e.preventDefault(); // 防止页面滚动
}

function handleTouchMove(e) {
    if (!isDrawing) return;
    
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.strokeStyle = colorPicker.value;
    ctx.lineWidth = lineWidth.value;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.stroke();
    
    [lastX, lastY] = [x, y];
    e.preventDefault(); // 防止页面滚动
}

function handleTouchEnd() {
    isDrawing = false;
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

// 初始化显示画笔粗细
updateLineWidth();