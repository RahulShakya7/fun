import pygame
import numpy as np
from numba import jit

pygame.init()

WIDTH, HEIGHT = 200, 200
size = 2
window = pygame.display.set_mode((WIDTH * size, HEIGHT * size))
clock = pygame.time.Clock()
fps = 144

f = 0.055
k = 0.062
dA = 1
dB = 0.5

grid = np.empty(shape=(WIDTH, HEIGHT, 2))
grid[0:][0:] = [1, 0]
grid[0][0] = [1, 0]

for y in range(HEIGHT // 2 - 10, HEIGHT // 2 + 11):
    for x in range(WIDTH // 2 - 10, WIDTH // 2 + 11):
        grid[y][x] = [0, 1]


@jit(nopython="True")
def update(grid):
    a = np.empty(shape=(WIDTH, HEIGHT, 2))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if y == 0 or x == 0 or y == HEIGHT - 1 or x == WIDTH - 1:
                a[y][x][0] = grid[y][x][0]
                a[y][x][1] = grid[y][x][1]
            else:
                a[y][x][0] = grid[y][x][0] + (
                            dA * laplace(x, y, 0, grid) - grid[y][x][0] * grid[y][x][1] ** 2 + f * (1 - grid[y][x][0]))
                a[y][x][1] = grid[y][x][1] + (
                            dB * laplace(x, y, 1, grid) + grid[y][x][0] * grid[y][x][1] ** 2 - (k + f) * grid[y][x][1])
    return a


@jit(nopython="True")
def laplace(x, y, p, grid):
    val = 0
    val += grid[y][x][p] * -1
    val += grid[y - 1][x][p] * 0.2
    val += grid[y + 1][x][p] * 0.2
    val += grid[y][x - 1][p] * 0.2
    val += grid[y][x + 1][p] * 0.2
    val += grid[y - 1][x - 1][p] * 0.05
    val += grid[y + 1][x + 1][p] * 0.05
    val += grid[y + 1][x - 1][p] * 0.05
    val += grid[y - 1][x + 1][p] * 0.05
    return val


def main():
    global grid
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for y in range(HEIGHT):
            for x in range(WIDTH):
                # pygame.draw.rect(window, (int(max(0, min(grid[y][x][0] * 255, 255))), 0, int(max(0, min(grid[y][x][1] * 255, 255)))), (x * size, y * size, size, size))
                pygame.draw.rect(window, (grid[y][x][0] * 255, 0, grid[y][x][1] * 255),
                                 (x * size, y * size, size, size))
        grid = update(grid)

        pygame.display.update()
        # clock.tick(fps)


main()