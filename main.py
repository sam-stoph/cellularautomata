import numpy as np
import pygame

#Brian's Brain states
OFF, ON, DYING = 0, 1, 2

print ("\nWelcome to the Brian's Brain Simulation! \n\nHere are the controls: \n-Mouse-click: turns cell on/off \n-Space: Start/stop the simulation \n-R: randomize the grid with ON/OFF/DYING cells \n-C: Set all the cells to OFF \n\n Have fun! \n")

class Grid:
    def __init__(self, size=130, cell_size=7):
        pygame.init()
        self.size = size
        self.cell_size = cell_size
        self.grid = np.zeros((size, size), dtype=int)
        self.screen_size = size * cell_size
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("Brian's Brain")
        self.running = False

    def update_grid(self):
        #make a new grid and replace it with the old to avoid using updated values when considering states
        new_grid = np.copy(self.grid)
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x, y] == OFF:
                    neighbors = self.count_neighbors(x, y)
                    if neighbors == 2:
                        new_grid[x, y] = ON
                elif self.grid[x, y] == ON:
                    new_grid[x, y] = DYING
                elif self.grid[x, y] == DYING:
                    new_grid[x, y] = OFF
        self.grid = new_grid

    def count_neighbors(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if self.grid[(x + dx) % self.size, (y + dy) % self.size] == ON:
                    count += 1
        return count

    def draw_grid(self):
        colors = {OFF: (255, 255, 255), ON: (0, 255, 0), DYING: (255, 0, 0)}
        self.screen.fill(colors[OFF])
        for x in range(self.size):
            for y in range(self.size):
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                color = colors[self.grid[x, y]]
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
        pygame.display.flip()

    def toggle_cell(self, pos):
        x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
        self.grid[x, y] = ON if self.grid[x, y] == OFF else OFF

    def randomize_grid(self):
        self.grid = np.random.choice([OFF, ON, DYING], size=(self.size, self.size))

    def clear_grid(self):
        self.grid = np.zeros((self.size, self.size), dtype=int)

    def run(self):
        clock = pygame.time.Clock()
        running_simulation = True
        while running_simulation:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_simulation = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.toggle_cell(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = not self.running
                    elif event.key == pygame.K_r:
                        self.randomize_grid()
                    elif event.key == pygame.K_c:
                        self.clear_grid()

            if self.running:
                self.update_grid()

            self.draw_grid()

        pygame.quit()

if __name__ == '__main__':
    grid = Grid()
    grid.run()
