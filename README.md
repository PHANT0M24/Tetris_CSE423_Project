# OpenGL Points Renderer

A Python-based OpenGL project that exclusively uses **GL_POINTS** for rendering. This project demonstrates the power and flexibility of OpenGL for creating visually stunning point-based graphics, bypassing external libraries like `pygame` for simplicity and focusing purely on OpenGL.

## Features

- **GL_POINTS Rendering**: Leverages the GL_POINTS primitive to create point-based visualizations.
- **Customizable Shader Programs**: Integrates vertex and fragment shaders to control the rendering pipeline.
- **Dynamic Animations**: Supports interactive or procedural animations using point clouds.
- **Lightweight and Minimal Dependencies**: Built using Python's OpenGL bindings (`PyOpenGL`) for direct interaction with the OpenGL API.

## Requirements

Ensure the following dependencies are installed:

- Python 3.8+
- [PyOpenGL](https://pypi.org/project/PyOpenGL/)
- [Numpy](https://pypi.org/project/numpy/) (for efficient data handling)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/opengl-points-renderer.git
   cd opengl-points-renderer
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script to start the OpenGL application:
```bash
python main.py
```

### Key Commands
- **ESC**: Exit the application
- **Arrow Keys**: Adjust viewing angles or point positions
- **Mouse Scroll**: Zoom in/out

## Code Overview

### 1. **Initialization**
The program initializes an OpenGL context using `GLUT` for window management and event handling.

### 2. **Shaders**
- **Vertex Shader**: Controls the positioning of points in 3D space.
- **Fragment Shader**: Applies color or texture to the points.

### 3. **Point Data**
Point data is dynamically generated or loaded from an external source (e.g., `.txt`, `.csv`, or procedural functions).

### 4. **Rendering Loop**
A render loop updates the point positions (if animated) and redraws the frame at a fixed interval.

---

**Author**: Mohammad Khairul Ananm   
**GitHub**: [PHANT0M24](https://github.com/PHANT0M24)
---
**Co-Author**: Mst. Ishrat Jahan Rintu   
**GitHub**: [Ishrat2413](https://github.com/Ishrat2413)
---
**Co-Author**: SM Najmul Alam   
**GitHub**: [Najmul193](https://github.com/Najmul193)   
---
