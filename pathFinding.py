import pygame
import heapq
import time

# Initialize Pygame
pygame.init()

# Screen dimensions and grid parameters
width, height = 800, 800
rows, cols = 50, 50
cell_size = width // cols

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
CYAN = (0, 255, 255)

# Create the screen
screen = pygame.display.set_mode((width, height + 100))
pygame.display.set_caption("Pathfinding Visualization with Dijkstra's Algorithm")

# Font
font = pygame.font.Font(None, 36)

# Create a 2D list to represent the grid
grid = [[0 for _ in range(cols)] for _ in range(rows)]

# Start and end points
start = None
end = None

# Priority queue for Dijkstra's algorithm
pq = []

# Function to draw the grid
def draw_grid():
    for row in range(rows):
        for col in range(cols):
            color = WHITE
            if grid[row][col] == 1:
                color = BLACK
            elif (row, col) == start:
                color = GREEN
            elif (row, col) == end:
                color = RED
            elif grid[row][col] == 2:
                color = BLUE
            elif grid[row][col] == 3:
                color = CYAN
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, GRAY, (col * cell_size, row * cell_size, cell_size, cell_size), 1)

# Function to draw the UI
def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, height, width, 100))
    if pathfinding_completed:
        button_text = 'Reset'
    else:
        button_text = 'Play'
    start_button = pygame.Rect(10, height + 10, 100, 40)
    close_button = pygame.Rect(120, height + 10, 150, 40)
    pygame.draw.rect(screen, YELLOW, start_button)
    pygame.draw.rect(screen, RED, close_button)
    screen.blit(font.render(button_text, True, BLACK), (30, height + 20))
    screen.blit(font.render('Close Window', True, BLACK), (130, height + 20))
    return start_button, close_button

# Function to visualize the pathfinding
def visualize_pathfinding():
    start_time = time.time()
    path_found = False
    came_from = {}

    while pq:
        current_cost, current_node = heapq.heappop(pq)
        current_x, current_y = current_node
        
        if (current_x, current_y) == end:
            path_found = True
            break
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_x, next_y = current_x + dx, current_y + dy
            if 0 <= next_x < rows and 0 <= next_y < cols and grid[next_x][next_y] == 0:
                heapq.heappush(pq, (current_cost + 1, (next_x, next_y)))
                grid[next_x][next_y] = 2
                came_from[(next_x, next_y)] = (current_x, current_y)
                if (next_x, next_y) != start and (next_x, next_y) != end:
                    pygame.draw.rect(screen, BLUE, (next_y * cell_size, next_x * cell_size, cell_size, cell_size))
                    pygame.draw.rect(screen, GRAY, (next_y * cell_size, next_x * cell_size, cell_size, cell_size), 1)
                pygame.display.update()
                pygame.time.delay(10)

    end_time = time.time()
    time_taken = end_time - start_time
    
    if path_found:
        current = end
        while current != start:
            x, y = current
            if current != end:
                grid[x][y] = 3
            current = came_from[current]
            pygame.display.update()
            pygame.time.delay(50)
    
    return time_taken

# Function to reset the grid
def reset_grid():
    global grid, start, end, pq, pathfinding_started, pathfinding_completed, time_taken
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    start = None
    end = None
    pq = []
    pathfinding_started = False
    pathfinding_completed = False
    time_taken = None

# Main loop
running = True
pathfinding_started = False
pathfinding_completed = False
start_button = None
close_button = None
time_taken = None

while running:
    screen.fill(WHITE)
    draw_grid()
    start_button, close_button = draw_ui()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif pygame.mouse.get_pressed()[0]:  # Left mouse button
            pos = pygame.mouse.get_pos()
            if pos[1] < height:
                x, y = pos[1] // cell_size, pos[0] // cell_size
                if not start:
                    start = (x, y)
                elif not end and (x, y) != start:
                    end = (x, y)
                elif (x, y) != start and (x, y) != end:
                    grid[x][y] = 1  # Mark the cell as a wall
            elif start_button.collidepoint(pos):
                if pathfinding_completed:
                    reset_grid()
                elif start and end:
                    pathfinding_started = True
                    heapq.heappush(pq, (0, start))
            elif close_button.collidepoint(pos):
                running = False
        
        elif pygame.mouse.get_pressed()[2]:  # Right mouse button
            pos = pygame.mouse.get_pos()
            if pos[1] < height:
                x, y = pos[1] // cell_size, pos[0] // cell_size
                if (x, y) != start and (x, y) != end:
                    grid[x][y] = 0  # Remove the wall
    
    if pathfinding_started:
        time_taken = visualize_pathfinding()
        pathfinding_started = False
        pathfinding_completed = True

    if time_taken is not None:
        text = font.render(f'Time taken: {time_taken:.2f} seconds', True, BLACK)
        screen.blit(text, (300, height + 20))

    pygame.display.update()

pygame.quit()
