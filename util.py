import math
import random

# A vector in polar coordinates
class RadVec:

    def __init__(self, theta, r):
        self.theta = theta
        self.r = r

    def toCartesian(self):
        return Vec2(self.r * math.cos(self.theta), self.r*math.sin(self.theta))
    
    def randVec(r_bound):
        return RadVec(random.random() * 2 * math.pi, 1 + random.random() * r_bound)
    
    def __str__(self):
        return f'({math.degrees(self.theta)}, {self.r})'

class Vec2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        len = self.length()
        self.x /= len
        self.y /= len

    def add(self, v2):
        if type(v2) != Vec2:
            raise TypeError("Invalid type " + str(type(v2)) + " for addition")
        
        return Vec2(self.x + v2.x, self.y + v2.y)
    
    def smul(self, s):
        return Vec2(self.x * s, self.y * s)

    def dot(self, v2):

        if type(v2) != Vec2:
            raise TypeError("Invalid type " + str(type(v2)) + " for dot product")

        return (self.x * v2.x + self.y*v2.y)
    
    def __str__(self):
        return f'({self.x}, {self.y})'
