from pygame.math import Vector2
import pygame

stiffness_k = 15
dump_k = .5
gravity = 9.81
mass = 0.1
scale = 1000

points = []
line_color = (255, 255, 255)
point_color = (127, 127, 127)
line_width = 2
point_radius = 5


def load_points(filename):
    try:
        file = open(filename, 'r')
        n, stop = map(int, file.readline().split())
        for i in range(n):
            stop_point = False
            if i < stop:
                stop_point = True
            coords = tuple(map(int, file.readline().split()))
            points.append(Point(coords, mass, stop_point))
        for i in range(n):
            connections = tuple(map(int, file.readline().split()))
            for j in connections:
                points[i].set_connection(j)
    except FileExistsError:
        print('Файла не существует')


def cloth_update(deltatime, target):
    for point in points:
        if point != target:
            point.force_calculate()

    for point in points:
        if point != target:
            point.move(deltatime)


def draw(surface: pygame.Surface):
    n = len(points)
    used = [False] * n
    for i in range(n):
        for j in points[i].connections.keys():
            if not used[j]:
                pygame.draw.aaline(surface,
                                 line_color,
                                 points[i].position * scale,
                                 points[j].position * scale,
                                 line_width)
        pygame.draw.circle(surface,
                           point_color,
                           points[i].position * scale,
                           point_radius)
        used[i] = True


def set_points_to_default():
    for point in points:
        point.position.update(point.start_position / scale)
        point.velocity.update(0, 0)


def find_point(pos, search_radius):
    for point in points:
        if (point.position * scale).distance_to(pos) < search_radius:
            return point
    return None


def create_point(pos, stop_point=False):
    points.append(Point(pos, mass, stop_point))


class Point:
    def __init__(self, start_pos, mass, stop_point=False):
        self.mass = mass
        self.start_position = Vector2(start_pos)
        self.position = Vector2(start_pos) / scale
        self.velocity = Vector2(0, 0)
        self.stop_point = stop_point

        self.connections = {}
        self.total_force = Vector2(0, 0)

    def set_connection(self, other_id):
        self.connections[other_id] = (points[other_id].position - self.position).length()

    def update_connection(self, other_id):
        self.set_connection(other_id)
        points[other_id].set_connection(points.index(self))

    def force_calculate(self):
        if not self.stop_point:
            self.total_force.update(0, 0)
            for other in self.connections.keys():
                force = ((points[other].position - self.position).length() - self.connections[other]) * stiffness_k + \
                        (points[other].position - self.position).normalize()*(points[other].velocity - self.velocity) * dump_k
                self.total_force += (points[other].position - self.position).normalize() * force
            self.total_force += Vector2(0, 1) * self.mass * gravity

    def move(self, deltatime):
        if not self.stop_point:
            self.velocity += self.total_force / self.mass * deltatime
            self.position += self.velocity * deltatime

    def set_position(self, pos, update_start_pos):
        self.position = Vector2(pos) / scale
        if update_start_pos:
            self.start_position.update(pos)
            for i, other_id in enumerate(self.connections):
                self.update_connection(other_id)
