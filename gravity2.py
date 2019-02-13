import random as r
import math
import graphics


g = 6.6 * 10 ** -11
timestep = 1 / 30
framestep = 1 / 30
bodies = 20
seconds = 10000000000000
nframes = int(seconds / framestep)
height = 600
width = 1000
size = 2
scale = 100
velo = 50000
mass = 1000
sbmass = 10 ** 24


def safe_div(x, y):
    if y == 0:
        return 0
    return x/y


class Special_Body:                         # Class creates a Special Body
    def __init__(self):
        self.xval = width * scale / 2
        self.yval = height * scale / 2
        self.massval = sbmass
        self.sizeval = 50


class Particle:                             # Particle class creates a particle
    def __init__(self, index):
        self.index = index
        self.x = r.randint(0, width * scale)
        self.dx = r.randint(-velo, velo)
        self.ddx = None
        self.y = r.randint(0, height * scale)
        self.dy = r.randint(-velo, velo)
        self.ddy = None
        self.mass = r.randint(mass, mass * 5)
        self.size = self.mass / mass * size

# Updates ddx and ddy for one frame
    def update_a(self, space, special_bodies):
        self.ddx = 0
        self.ddy = 0

        Special_Bodyx = special_bodies[0][0]
        Special_Bodyy = special_bodies[0][1]
        Special_Bodymass = special_bodies[0][2]
        distancex = - Special_Bodyx + self.x
        distancey = - Special_Bodyy + self.y
        distance = math.sqrt(distancex ** 2 + distancey ** 2)
        if distance >= self.size:
            force = - safe_div(
                (g * Special_Bodymass * self.mass), distance ** 2)
            self.ddx += (force * distancex / distance) / self.mass
            self.ddy += (force * distancey / distance) / self.mass
        else:
            force = - safe_div((
                g * sbody.massval * self.mass), (self.size * 10) ** 2)
            self.ddx += safe_div(force * distancex, distance) / self.mass
            self.ddy += safe_div(force * distancey, distance) / self.mass

        for pair in space:
            particle = pair[0]
            if particle.index is not self.index:        # Forces from particles
                distancex = - particle.x + self.x
                distancey = - particle.y + self.y
                distance = math.sqrt(distancex ** 2 + distancey ** 2)
                if distance >= self.size:
                    force = - safe_div(
                        (g * particle.mass * self.mass), distance ** 2)
                    self.ddx += safe_div(force * distancex, distance)\
                        / self.mass
                    self.ddy += safe_div(force * distancey, distance)\
                        / self.mass
                else:
                    force = - safe_div((
                        g * particle.mass * self.mass), (self.size * 10) ** 2)
                    self.ddx += (force * distancex / distance) / self.mass
                    self.ddy += (force * distancey / distance) / self.mass

    def update_v(self):                     # Updates dx and dy for one frame
        self.dx += self.ddx * timestep
        self.dy += self.ddy * timestep

    def update_r(self, fig):                # Updates x and y for one frame
        dx = self.dx
        dy = self.dy
        self.x += dx * timestep
        self.y += dy * timestep


space = []                        # Holds Particle objects and graphics objects

# Appends one list of a particle and its matching graphics object to space
for body in range(bodies):
    pair = []
    particle = Particle(body)
    x = particle.x / scale
    y = particle.y / scale
    point = graphics.Point(x, y)
    circle = graphics.Circle(point, particle.size)
    pair.append(particle)
    pair.append(circle)
    space.append(pair)


special_bodies = []             # Holds Special Body object and graphics object

sbody = Special_Body()
stats = [sbody.xval, sbody.yval, sbody.massval]
special_bodies.append(stats)
sbody_image = graphics.Circle(
    graphics.Point(sbody.xval / scale, sbody.yval / scale), sbody.sizeval)
special_bodies.append(sbody_image)


# Graphics function
def main():
    win = graphics.GraphWin("Gravity", width, height, autoflush=False)

    sbody_image.draw(win)      # Draws Special Body
    sbody_image.setFill("blue")

    for pair in space:      # Initializes the space, draws all particles
        particle = pair[0]
        particle_circle = pair[1]
        particle_circle.draw(win)
        particle_circle.setFill("black")

    for frame in range(nframes):        # Instructions for frame refresh
        for pair in space:
            particle = pair[0]
            circle = pair[1]
            dx = particle.dx * timestep / scale
            dy = particle.dy * timestep / scale
            circle.move(dx, dy)
            particle.update_a(space, special_bodies)
            particle.update_v()
            particle.update_r(win)
        graphics.update(1 / framestep)


main()
