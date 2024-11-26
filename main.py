import pygame
import numpy as np
import math
from util import *

SIZE = (900, 700)

#Gradient descent process
class GDProcess:

    def __init__(self):
        self.learning_rate = 0.02

    def grad(self, segments, p_x, p_y):

        # First, calculate u and v to help our gradient calculation:
        sum_u = 0
        sum_v = 0
        for segment in segments:
            sum_u += (segment.r * math.cos(segment.theta))
            sum_v += (segment.r * math.sin(segment.theta))
        u = (p_x - sum_u)
        v = (p_y - sum_v)

        # Now calculate the partial derivatives for the gradient vector:
        grad = np.zeros(len(segments))
        for (i, segment) in enumerate(segments):
            grad[i] = (2 * segment.r * math.sin(segment.theta) * u) - (2 * segment.r * math.cos(segment.theta) * v)

        return grad
    
    def descend(self, iterations, params, target):
        steps = 0

        # Copy params: don't wanna do this in-place
        params = [RadVec(x.theta, x.r) for x in params]
        while steps < iterations:
            # Perform one gradient descent
            grad = -self.learning_rate * self.grad(params, target[0], target[1])
            
            for (i, vec) in enumerate(params):
                vec.theta += grad[i]

            steps += 1
        
        return params


class App:

    class EasingTask:

        def __init__(self):
            self.easing = False
            self.t = 0

        def startTask(self, start, end, time):
            self.start = [RadVec(x.theta, x.r) for x in start]
            self.modify = start # The array to be easing over
            self.end = end
            self.easing = True
            self.time = time

        def endTask(self):
            self.easing = False
            self.t = 0
            self.start = None
            self.end = None

        def tick(self):
            self.t += 1

            for (i, vec) in enumerate(self.modify):
                dist = self.end[i].theta - self.start[i].theta
                vec.theta = self.start[i].theta + (dist * (math.sin((self.t / self.time * math.pi) / 2)))

            if (self.t > self.time):
                self.endTask()

    def __init__(self):
        self.SCALE = 50
        self.arm = [RadVec.randVec(1) for _ in range(3)]
        self.point = (1, 1)

        self.easing_task = self.EasingTask()

    def tick(self):
        if (self.easing_task.easing):
            self.easing_task.tick()


    # Begin gradient descent
    def onKey(self, unicode):
        gdp = GDProcess()
        params = gdp.descend(1000, self.arm, self.point)

        self.easing_task = self.EasingTask()
        self.easing_task.startTask(self.arm, params, 60)

    # Update point pos based on click pos
    def onClick(self, pos):
        origin_x = SIZE[0] // 2
        origin_y = SIZE[1] // 2
        self.point = ((origin_x - pos[0]) / -self.SCALE, (origin_y - pos[1]) / self.SCALE)

    def draw(self, screen):
        screen.fill("white")

        origin_x = SIZE[0] // 2
        origin_y = SIZE[1] // 2
        start = (origin_x, origin_y)
        # Draw each section of the arm
        for seg in self.arm:
            seg_cart = seg.toCartesian().smul(self.SCALE)
            end = (start[0] + seg_cart.x, start[1] - seg_cart.y)

            pygame.draw.line(screen, (0, 0, 0), start, end, 3)
            pygame.draw.circle(screen, (0,0,0), start, 12)
            pygame.draw.circle(screen, (255,255,255), start, 10)

            start = end

        # Draw desired point
        point_screen = (origin_x + self.point[0] * self.SCALE, origin_y - self.point[1] * self.SCALE)
        pygame.draw.circle(screen, (255, 0, 0), point_screen, 11, 2)

    
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)

    pygame.display.set_caption("IK")

    running = True
    clock = pygame.time.Clock()

    app = App()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key = event.unicode
                app.onKey(key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                app.onClick(event.pos)

        app.tick()
        app.draw(screen)

        pygame.display.flip()



if __name__ == "__main__":
    main()