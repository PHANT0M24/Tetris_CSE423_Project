import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

# Define colors
colors = [
    (0.0, 0.0, 0.0),  # Black (empty space)
    (0.47, 0.15, 0.7),  # Purple
    (0.39, 0.7, 0.7),  # Cyan
    (0.31, 0.13, 0.09),  # Brown
    (0.31, 0.52, 0.09),  # Green
    (0.7, 0.13, 0.09),  # Red
    (0.7, 0.13, 0.48),  # Magenta
]

# Define Tetris blocks (tetrominoes)
class Figure:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # Square shape
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # T-shape
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # Z-shape
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # L-shape
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # S-shape
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # J-shape
        [[1, 2, 5, 6]],  # Line shape
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

# Midpoint Circle Drawing Algorithm
def midpoint_circle(center_x, center_y, radius):
    points = []
    x = radius
    y = 0
    p = 1 - radius  # Initial decision parameter

    # Plot points for a circle using symmetry
    while x >= y:
        points.append((center_x + x, center_y + y))
        points.append((center_x - x, center_y + y))
        points.append((center_x + x, center_y - y))
        points.append((center_x - x, center_y - y))
        points.append((center_x + y, center_y + x))
        points.append((center_x - y, center_y + x))
        points.append((center_x + y, center_y - x))
        points.append((center_x - y, center_y - x))

        y += 1
        if p <= 0:
            p = p + 2 * y + 1
        else:
            x -= 1
            p = p + 2 * (y - x) + 1

    return points

class Tetris:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        self.state = "start"
        self.figure = None
        self.score = 0
        self.last_score_time = time.time()
        self.upcoming_figures = []
        self.paused = False  # Add paused attribute

    def new_figure(self):
        # Checking if there are upcoming figures; if not, generate them
        if not self.upcoming_figures:
            self.upcoming_figures = [Figure(3, 0) for _ in range(3)]

        # Poping the next figure from the upcoming figures list
        self.figure = self.upcoming_figures.pop(0)

        # After using a figure, add a new one to the list
        self.upcoming_figures.append(Figure(3, 0))

    def intersects(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    x, y = j + self.figure.x, i + self.figure.y
                    if x < 0 or x >= self.width or y >= self.height or self.field[y][x] > 0:
                        return True
        return False

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[self.figure.y + i][self.figure.x + j] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "Game Over"

    def break_lines(self):
        lines = 0
        for i in range(self.height - 1, -1, -1):
            if 0 not in self.field[i]:
                lines += 1
                del self.field[i]
                self.field.insert(0, [0 for _ in range(self.width)])
        self.score += lines ** 2

    def go_down(self):
        if not self.paused and self.state == "start":  # Check if not paused
            self.figure.y += 1
            if self.intersects():
                self.figure.y -= 1
                self.freeze()

    def go_side(self, dx):
        if not self.paused and self.state == "start":  # Check if not paused
            self.figure.x += dx
            if self.intersects():
                self.figure.x -= dx

    def rotate(self):
        if not self.paused and self.state == "start":  # Check if not paused
            old_rotation = self.figure.rotation
            self.figure.rotate()
            if self.intersects():
                self.figure.rotation = old_rotation

    def toggle_pause(self):
        if self.state == "start":  # Only allow pausing in the "start" state
            self.paused = not self.paused

    def reset_game(self):
        self.__init__(self.height, self.width)  # Reinitialize the game
        self.new_figure()


# Draw a single block cell with a rounded corner style
def draw_cell(x, y, color):
    glColor3f(*color)
    radius = 10
    for dx in range(4):
        for dy in range(4):
            if dx != 2 or dy != 2:
                points = midpoint_circle(x * 30 + 15 , y * 30 + 15, radius)  # Smaller radius for each cell
                glBegin(GL_POLYGON)  # Draw a filled polygon
                for px, py in points:
                    glVertex2i(px, py)
                glEnd()
def draw_button(x, y, width, height, label, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2i(x, y)
    glVertex2i(x + width, y)
    glVertex2i(x + width, y + height)
    glVertex2i(x, y + height)
    glEnd()

    glColor3f(1, 1, 1)
    glRasterPos2i(x + 10, y + height // 2 - 5)
    for char in label:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

# Function to display the game state
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor4f(0.62, 0.0, 1, 1.0)  # Golden color with full opacity
    glLineWidth(5)  # Setting border line width
    glBegin(GL_LINE_LOOP)
    glVertex2i(2, 30)  # Top-left corner
    glVertex2i(game.width * 30, 30)  # Top-right corner
    glVertex2i(game.width * 30, game.height * 30)  # Bottom-right corner
    glVertex2i(2, game.height * 30)  # Bottom-left corner
    glEnd()

    glColor4f(0.5, 0.5, 0.5, 0.5)  # Light gray with 50% opacity
    glLineWidth(2)  # Set grid line width
    glBegin(GL_LINES)
    for x in range(1, game.width):
        glVertex2i(x * 30, 30)
        glVertex2i(x * 30, game.height * 30)
    for y in range(1, game.height):
        glVertex2i(2, y * 30 + 30)
        glVertex2i(game.width * 30, y * 30 + 30)
    glEnd()

    # Draw the game grid and the falling figure
    for y in range(game.height):
        for x in range(game.width):
            if game.field[y][x] > 0:
                draw_cell(x, y, colors[game.field[y][x]])

    if game.figure:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.figure.image():
                    draw_cell(game.figure.x + j, game.figure.y + i, colors[game.figure.color])

    # Score display with blinking effect
    glColor3f(1.0, 1.0, 1.0)  # White color for the score
    current_time = time.time()
    score_text = "Score"
    if int(current_time * 2) % 2 == 0:  # Blinking effect
        glRasterPos2i(game.width * 30 + 50, 30)  # Position score label
        for char in score_text:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    score_display = f"{game.score}"
    glRasterPos2i(game.width * 30 + 50, 60)  # Position score value
    for char in score_display:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    # Buttons
    draw_button(800, 100, 100, 30, "Pause", (0, 0.7, 0))
    draw_button(800, 150, 100, 30, "Restart", (0.7, 0.7, 0))
    draw_button(800, 200, 100, 30, "Quit", (0.7, 0, 0))

    # Display upcoming cells on the right side below buttons
    glColor3f(1.0, 1.0, 1.0)  # White color for text
    glRasterPos2i(800, 250)  # Position the text "Upcoming Cell"
    for char in "Upcoming Cell":
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    # Draw the upcoming cells below the text "Upcoming Cell"
    for i, upcoming_figure in enumerate(game.upcoming_figures):
        for j in range(4):
            for k in range(4):
                if j * 4 + k in upcoming_figure.image():
                    # Draw the upcoming cells offset from the right side of the main grid
                    draw_cell(27 + k, 9 + i * 4 + j, colors[upcoming_figure.color])

    glutSwapBuffers()

def reset_game():
    game.score = 0
    game.state = "start"
    game.field = [[0 for _ in range(game.width)] for _ in range(game.height)]
    game.new_figure()

def quit_game():
    exit(0)

def keyboard(key, x, y):
    if game.state == "start":
        if key == b'a':  # Move left
            game.go_side(-1)
        elif key == b'd':  # Move right
            game.go_side(1)
        elif key == b's':  # Move down
            game.go_down()
        elif key == b'w' or key == 101:  # Rotate (also support up arrow key)
            game.rotate()
    if key == b'q':  # Quit the game
        exit(0)


def mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 800 <= x <= 900:
            if 100 <= y <= 130:  # Pause button
                game.toggle_pause()
            elif 150 <= y <= 180:  # Restart button
                game.reset_game()
            elif 200 <= y <= 230:  # Quit button
                glutLeaveMainLoop()


# Timer function to control game speed
def update(value):
    if game.state == "start" and not game.paused:  # Skip updates if the game is paused
        game.go_down()
    glutPostRedisplay()  # Redraw the screen
    glutTimerFunc(500, update, 0)  # Call update every 500 ms


# Main function to initialize the game
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1280, 720)  # 1280x720 resolution
    glutCreateWindow(b"Tetris")  # Create the window
    glOrtho(0, 1280, 720, 0, -1, 1)  # 2D orthogonal projection for the new window size
    glutDisplayFunc(display)  # Set display callback
    glutKeyboardFunc(keyboard)  # Set keyboard input callback
    glutMouseFunc(mouse_click)
    glutTimerFunc(200, update, 0)  # Set the timer callback
    game.new_figure()  # Generate the first figure
    glutMainLoop()  # Start the main loop

# Run the game
game = Tetris(20, 25)
main()
