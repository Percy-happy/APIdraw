# Drawing Board

A versatile drawing board application that supports both manual drawing and API-controlled drawing functionality.

## Features

### Manual Drawing
- Draw on canvas using mouse or touch
- Adjust brush color and thickness
- Clear canvas function
- Export canvas content as PNG image

### API Drawing Control
- Execute drawing commands through the API input area
- Support for drawing lines, circles, rectangles, and text
- Control brush color and thickness via commands
- Export and clear functionality through API

## How to Use

### Manual Drawing
1. Open the application in a web browser
2. Select your desired brush color from the color picker
3. Adjust the brush thickness using the slider
4. Draw on the canvas area using mouse or touch
5. Use the "Clear" button to reset the canvas
6. Use the "Export" button to save your drawing as a PNG image

### API Drawing
1. Open the API command input area
2. Enter drawing commands in the specified format
3. Click the "Execute" button to run the command
4. Use the "API Export" button to export via API

## API Command Format

### Drawing Commands

#### Draw a Line
```
draw(line, x1, y1, x2, y2, color, width)
```
- `x1, y1`: Starting coordinates
- `x2, y2`: Ending coordinates
- `color`: Brush color (optional, defaults to current color)
- `width`: Brush width (optional, defaults to current width)

#### Draw a Circle
```
draw(circle, x, y, radius, color, width)
```
- `x, y`: Center coordinates
- `radius`: Circle radius
- `color`: Brush color (optional, defaults to current color)
- `width`: Brush width (optional, defaults to current width)

#### Draw a Rectangle
```
draw(rectangle, x, y, width, height, color, thickness)
```
- `x, y`: Top-left corner coordinates
- `width`: Rectangle width
- `height`: Rectangle height
- `color`: Brush color (optional, defaults to current color)
- `thickness`: Border thickness (optional, defaults to current width)

#### Draw Text
```
draw(text, x, y, text_content, color, font_size)
```
- `x, y`: Text position coordinates
- `text_content`: The text to display
- `color`: Text color (optional, defaults to current color)
- `font_size`: Font size (optional, defaults to 20)

### Utility Commands

#### Set Color
```
set(color, color_value)
```
- `color_value`: Color value (e.g., '#FF0000' or 'red')

#### Set Line Width
```
set(width, width_value)
```
- `width_value`: Line width in pixels

#### Export Canvas
```
export()
```

#### Clear Canvas
```
clear()
```

## JavaScript API

You can also control the drawing board programmatically through JavaScript:

```javascript
// Draw a line
window.DrawingAPI.drawLine(10, 10, 100, 100, '#FF0000', 5);

// Draw a circle
window.DrawingAPI.drawCircle(150, 150, 50, '#00FF00', 3);

// Draw a rectangle
window.DrawingAPI.drawRectangle(200, 200, 100, 80, '#0000FF', 2);

// Draw text
window.DrawingAPI.drawText(50, 50, 'Hello World', '#FF00FF', 24);

// Set color
window.DrawingAPI.setColor('#000000');

// Set line width
window.DrawingAPI.setLineWidth(4);

// Clear canvas
window.DrawingAPI.clear();

// Export canvas
window.DrawingAPI.export();
```

## Technical Implementation

### Web Version
- HTML5 Canvas API for drawing
- Pure JavaScript for all functionality
- CSS3 for interface styling
- Support for both mouse and touch events

### Python Version
- Uses PIL/Pillow library for image processing
- Supports local drawing and remote control of web drawing board
- Provides the same API interface as the web version

## Python API Usage Guide

### Install Dependencies

Before using the Python API, install the necessary dependencies:

```bash
pip install pillow requests
```

### Basic Usage

```python
from draw_api import DrawingAPI

# Create a local mode API instance
api = DrawingAPI(width=800, height=600)

# Draw shapes
api.draw_line(10, 10, 100, 100, color='#ff0000', width=5)
api.draw_circle(150, 150, 50, color='#00ff00', width=3)
api.draw_rectangle(200, 200, 100, 80, color='#0000ff', width=2)
api.draw_text(50, 50, 'Hello World', color='#ff00ff', font_size=24)

# Save image
api.export('my_drawing.png')

# Display image
api.show()
```

### Remote Mode

```python
# Connect to web drawing board (requires web version running)
api = DrawingAPI(mode='remote', url='http://localhost:8000')

# Draw shapes on remote board
api.draw_circle(300, 300, 40)
api.set_color('#ff9900')
api.draw_line(100, 100, 400, 400)
```

### Command String Execution

```python
# Execute command string
result = api.execute_command("draw(circle, 300, 300, 40)")
print(result)
```

### All API Methods

- `draw_line(x1, y1, x2, y2, color=None, width=None)` - Draw a line
- `draw_circle(x, y, radius, color=None, width=None)` - Draw a circle
- `draw_rectangle(x, y, width_rect, height_rect, color=None, width=None)` - Draw a rectangle
- `draw_text(x, y, text, color=None, font_size=20)` - Draw text
- `export(filename=None)` - Export canvas content
- `clear()` - Clear canvas
- `set_color(color)` - Set brush color
- `set_line_width(width)` - Set brush width
- `execute_command(command)` - Execute command string
- `show()` - Display current canvas (local mode only)

### Notes

- Remote mode requires the web drawing board to have corresponding API endpoints to receive commands
- Local mode uses PIL/Pillow library for image processing
- Default canvas size is 800x600 pixels, can be customized during initialization

## Compatibility

- Web version supports all modern browsers (Chrome, Firefox, Safari, Edge)
- Touch support for mobile devices
- Python API supports Python 3.6+

## Installation and Running

1. Clone or download the repository
2. Open the `index.html` file in a web browser, or
3. Run a local web server in the project directory:
   ```bash
   python3 -m http.server 8000
   ```
4. Visit http://localhost:8000 in your browser

## License

Free to use and modify for personal and educational purposes.