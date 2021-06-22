import pygame
import numpy as np
import random

pygame.init()

FPS = 60
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = window.get_size()
clock = pygame.time.Clock()
N, SPACE, RADIUS, VISION, MAXSPEED = 100, 2, 12, 5, 10
WRAP, LIMIT_SPEED, SEEK_MOUSE, PAUSED = True, True, False, False


class boid:
    def __init__(self, pos, vel, id):
        self.pos = np.array(pos, dtype='float64')
        self.vel = np.array(vel, dtype='float64')
        self.id = id

    def update(self, boids, cursor_pos=[]):
        if SEEK_MOUSE:
            self.vel += self.behave(boids) + \
                        self.seek(cursor_pos)
        else:
            self.vel += self.behave(boids)
        if LIMIT_SPEED:
            self.limit_speed()
        self.pos += self.vel
        if WRAP:
            self.wrap()
        else:
            self.collide()

    def behave(self, boids):
        tc = np.array([0, 0], dtype='float64')  # Cohesion vector
        ts = np.array([0, 0], dtype='float64')  # Seperation vector
        ta = np.array([0, 0], dtype='float64')  # Alignment vector
        c = 0
        for boid in boids:
            if boid.id == self.id:
                continue
            dist = ((boid.pos[0] - self.pos[0]) ** 2 +
                    (boid.pos[1] - self.pos[1]) ** 2) ** 0.5
            if dist < SPACE * RADIUS:
                ts = ts - (boid.pos - self.pos)
            if dist < VISION * RADIUS:
                tc += boid.pos
                ta += boid.vel
                c += 1
        if c > 0:
            tc = (tc / c - self.pos) / N
            ta = (ta / c - self.vel)
        else:
            tc = 0
            ta = 0
        ts = ts / (RADIUS)
        return tc + ts + ta

    def limit_speed(self):
        speed = (self.vel[0] ** 2 + self.vel[1] ** 2) ** 0.5
        if speed > MAXSPEED:
            self.vel = self.vel / speed * MAXSPEED

    def seek(self, place):
        return (place - self.pos) / N

    def wrap(self):
        if self.pos[0] < 0:
            self.pos[0] = WIDTH
        if self.pos[0] > WIDTH:
            self.pos[0] = 0

        if self.pos[1] < 0:
            self.pos[1] = HEIGHT
        if self.pos[1] > HEIGHT:
            self.pos[1] = 0

    def collide(self):
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.vel[0] = -self.vel[0]
        if self.pos[0] > WIDTH:
            self.pos[0] = WIDTH
            self.vel[0] = -self.vel[0]

        if self.pos[1] < 0:
            self.pos[1] = 0
            self.vel[1] = -self.vel[1]
        if self.pos[1] > HEIGHT:
            self.pos[1] = HEIGHT
            self.vel[1] = -self.vel[1]

    def draw(self):
        pygame.draw.polygon(window, (255, 255, 255), self.get_pts())

    def get_pts(self):
        if not self.vel.all():
            angle = 0
        else:
            angle = np.arccos(self.vel[0] / (self.vel[0] ** 2 + self.vel[1] ** 2) ** 0.5)
        if self.vel[1] < 0:
            angle *= -1
        p1 = self.pos[0] + RADIUS * \
             np.cos(angle), self.pos[1] + RADIUS * np.sin(angle)
        p2 = rotate_point(self.pos[0], self.pos[1], 2 * np.pi / 3, p1)
        p3 = rotate_point(self.pos[0], self.pos[1], -2 * np.pi / 3, p1)
        return (self.pos, p2, p1, p3)


def rotate_point(cx, cy, angle, pt):
    p = list(pt)
    s = np.sin(angle)
    c = np.cos(angle)

    p[0] -= cx
    p[1] -= cy

    xnew = p[0] * c - p[1] * s
    ynew = p[0] * s + p[1] * c

    # Cool "Feature"
    # xnew = p[0] * c - p[0] * s
    # ynew = p[1] * s + p[1] * c

    p[0] = xnew + cx
    p[1] = ynew + cy
    return p


def main():
    pygame.mouse.set_visible(False)
    boids = []
    for i in range(N):
        pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
        vel = (random.randrange(-1, 2) * random.random(),
               random.randrange(-1, 2) * random.random())
        boids.append(boid(pos, vel, i))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    global WRAP
                    WRAP = not WRAP
                if event.key == pygame.K_l:
                    global LIMIT_SPEED
                    LIMIT_SPEED = not LIMIT_SPEED
                if event.key == pygame.K_s:
                    global SEEK_MOUSE
                    SEEK_MOUSE = not SEEK_MOUSE
                if event.key == pygame.K_p:
                    global PAUSED
                    PAUSED = not PAUSED
                global RADIUS
                if event.key == pygame.K_EQUALS and RADIUS < 30:
                    RADIUS = RADIUS + 1
                if event.key == pygame.K_MINUS and RADIUS > 2:
                    RADIUS = RADIUS - 1

        if not PAUSED:
            window.fill((0, 0, 0))
            if SEEK_MOUSE: pygame.draw.circle(window, (255, 0, 0), pygame.mouse.get_pos(), 5)
            if not WRAP: pygame.draw.rect(window, (0, 0, 255), (0, 0, WIDTH - 1, HEIGHT - 1), 2)
            for b in boids:
                if SEEK_MOUSE:
                    b.update(boids, pygame.mouse.get_pos())
                else:
                    b.update(boids)
                b.draw()
            pygame.display.update()
        clock.tick(FPS)


main()