import pygame
import collections
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
ORANGE = (255, 165, 0)

# Create the screen
screen = pygame.display.set_mode((width, height + 100))
pygame.display.set_caption("Pathfinding Visualization with Maximum Flow Algorithm")

# Font
font = pygame.font.Font(None, 36)

# Create a 2D list to represent the grid
grid = [[0 for _ in range(cols)] for _ in range(rows)]

# Start and end points
start = None
end = None

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

# Function to draw the path and flow
def draw_flow_path(parent, source, sink):
    v = sink
    while v != source:
        u = parent[v]
        x1, y1 = u // cols, u % cols
        x2, y2 = v // cols, v % cols
        if (x1, y1) != start and (x1, y1) != end:
            grid[x1][y1] = 3
        if (x2, y2) != start and (x2, y2) != end:
            grid[x2][y2] = 2
        draw_grid()
        pygame.display.update()
        pygame.time.delay(50)
        v = parent[v]

# Function to highlight the shortest path
def highlight_shortest_path(parent, source, sink):
    v = sink
    while v != source:
        u = parent[v]
        x1, y1 = u // cols, u % cols
        x2, y2 = v // cols, v % cols
        if (x1, y1) != start and (x1, y1) != end:
            grid[x1][y1] = ORANGE
        if (x2, y2) != start and (x2, y2) != end:
            grid[x2][y2] = ORANGE
        draw_grid()
        pygame.display.update()
        pygame.time.delay(50)
        v = parent[v]

# Breadth-first search to find the path with available capacity
def bfs(capacity, source, sink, parent):
    visited = set()
    queue = collections.deque([source])
    visited.add(source)

    while queue:
        u = queue.popleft()

        for v in range(len(capacity)):
            if v not in visited and capacity[u][v] > 0:  # If not visited and capacity available
                queue.append(v)
                visited.add(v)
                parent[v] = u
                if v == sink:
                    draw_flow_path(parent, source, sink)
                    return True
    return False

# Edmonds-Karp function to find the maximum flow
def edmonds_karp(source, sink):
    n = len(grid) * len(grid[0])
    capacity = [[0] * n for _ in range(n)]
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == 0 or (x, y) == start or (x, y) == end:
                node = x * cols + y
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                        neighbor_node = nx * cols + ny
                        capacity[node][neighbor_node] = 1

    parent = [-1] * n
    max_flow = 0
    shortest_path = None

    while bfs(capacity, source, sink, parent):
        path_flow = float('Inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, capacity[parent[s]][s])
            s = parent[s]

        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow
        shortest_path = parent[:]

    if shortest_path:
        highlight_shortest_path(shortest_path, source, sink)

    return max_flow

# Function to visualize the pathfinding
def visualize_pathfinding():
    start_time = time.time()
    source = start[0] * cols + start[1]
    sink = end[0] * cols + end[1]
    max_flow = edmonds_karp(source, sink)
    end_time = time.time()
    time_taken = end_time - start_time
    return time_taken, max_flow

# Function to reset the grid
def reset_grid():
    global grid, start, end, pathfinding_started, pathfinding_completed, time_taken, max_flow
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    start = None
    end = None
    pathfinding_started = False
    pathfinding_completed = False
    time_taken = None
    max_flow = None

# Main loop
running = True
pathfinding_started = False
pathfinding_completed = False
start_button = None
close_button = None
time_taken = None
max_flow = None

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
            elif close_button.collidepoint(pos):
                running = False
        
        elif pygame.mouse.get_pressed()[2]:  # Right mouse button
            pos = pygame.mouse.get_pos()
            if pos[1] < height:
                x, y = pos[1] // cell_size, pos[0] // cell_size
                if (x, y) != start and (x, y) != end:
                    grid[x][y] = 0  # Remove the wall
    
    if pathfinding_started:
        time_taken, max_flow = visualize_pathfinding()
        pathfinding_started = False
        pathfinding_completed = True

    if time_taken is not None:
        text = font.render(f'Time taken: {time_taken:.2f} seconds', True, BLACK)
        screen.blit(text, (300, height + 20))
    if max_flow is not None:
        text = font.render(f'Max Flow: {max_flow}', True, BLACK)
        screen.blit(text, (300, height + 50))

    pygame.display.update()

pygame.quit()
