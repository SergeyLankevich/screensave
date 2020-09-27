import pygame
import random
import math

SCREEN_SIZE = (1280, 720)


class Vector:
    def __init__(self, x, y):
            self.x = x
            self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, factor):
        if isinstance(factor, Vector):
            return self.x * factor.x + self.y * factor.y
        return Vector(self.x * factor, self.y * factor)

    def len(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def int_pair(self):
        return (int(self.x), int(self.y))


class Line:
    def __init__(self):
        self.points = []
        self.velocities = []

    def add_point(self, point, speed):
        self.points.append(point)
        self.velocities.append(speed)

    def set_points(self):
        for i in range(len(self.points)):
            self.points[i] += self.velocities[i]
            if self.points[i].x > SCREEN_SIZE[0] or self.points[i].x < 0:
                self.velocities[i] = Vector(- self.velocities[i].x, self.velocities[i].y)
            if self.points[i].y > SCREEN_SIZE[1] or self.points[i].y < 0:
                self.velocities[i] = Vector(self.velocities[i].x, -self.velocities[i].y)

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for point in points:
            pygame.draw.circle(gameDisplay, color, point.int_pair(), width)


class Joint(Line):
    def __init__(self, count):
        super().__init__()
        self.count = count

    def add_point(self, point, speed):
        super().add_point(point, speed)
        self.get_joint()

    def set_points(self):
        super().set_points()
        self.get_joint()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.count
        result = []
        for i in range(self.count):
            result.append(self.get_point(base_points, i * alpha))
        return result

    def get_joint(self):
        if len(self.points) < 3:
            return []
        result = []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            pnt.append((self.points[i] + self.points[i + 1]) * 0.5)
            pnt.append(self.points[i + 1])
            pnt.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            result.extend(self.get_points(pnt))
        return result

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, points[p_n].int_pair(), points[p_n + 1].int_pair(), width)


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])
    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("MyScreenSaver")
    steps = 35
    working = True
    Line = Line()
    joint = Joint(steps)
    show_help = False
    pause = True
    hue = 0
    color = pygame.Color(0)
    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    Line = Line()
                    joint = Joint(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                Line.add_point(Vector(event.pos[0], event.pos[1]), Vector(random.random() * 2, random.random() * 2))
                joint.add_point(Vector(event.pos[0], event.pos[1]), Vector(random.random() * 2, random.random() * 2))
        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        Line.draw_points(Line.points)
        joint.draw_points(joint.get_joint(), 3, color)
        if not pause:
            Line.set_points()
            joint.set_points()
        if show_help:
            draw_help()
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
    exit(0)
