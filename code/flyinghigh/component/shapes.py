from __future__ import division

from itertools import chain
from math import cos, pi, sin, sqrt
from random import randint

from ..geometry.vec3 import Vec3, Origin, XAxis, YAxis, ZAxis


class Geometry(object):
    '''
    Defines a 3d object as a list of vertices, and a list of faces.
    Each face is a list of indices into the vertex array, forming a
    coplanar convex ring defining the face's boundary.
    '''
    def __init__(self, vertices, faces):
        if not isinstance(vertices[0], Vec3):
            vertices = [Vec3(*v) for v in vertices]
        self.vertices = vertices
        self.faces = faces


class Shape(object):

    def __init__(self, vertices, faces, color):
        self.geometry = Geometry(vertices, faces)
        self.color = color

    @property
    def vertices(self):
        return self.geometry.vertices

    @property
    def faces(self):
        return self.geometry.faces

    @property
    def colors(self):
        return [self.color for _ in xrange(len(self.vertices))]


class CompositeShape(object):

    def __init__(self):
        self.children = []
        self._vertices = None
        self._colors = None
        self._faces = None

    def add(self, child, offset=None):
        if offset is None:
            offset = Origin
        self.children.append((child, offset))

    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = [
                vert + offset
                for shape, offset in self.children
                for vert in shape.vertices]
        return self._vertices

    @property
    def faces(self):
        if self._faces is None:
            newfaces = []
            index_offset = 0
            for shape, _ in self.children:
                for face in shape.faces:
                    newface = []
                    for index in face:
                        newface.append(index + index_offset)
                    newfaces.append(newface)
                index_offset += len(shape.vertices)
            self._faces = newfaces
        return self._faces

    @property
    def colors(self):
        if self._colors is None:
            self._colors = list(
                chain.from_iterable(shape.colors for shape, _ in self.children))
        return self._colors


def Rectangle(width, height, color):
    vertices = [
        (-width/2, -height/2),
        (+width/2, -height/2),
        (+width/2, +height/2),
        (-width/2, +height/2),
    ]
    face = [0, 1, 2, 3]
    return Shape(vertices, [face], color)


def Circle(radius, color):
    NUM_POINTS = 32
    verts = []
    for n in xrange(0, NUM_POINTS):
        a = n * 2 * pi / NUM_POINTS
        verts.append( (radius * cos(a), radius * sin(a)) )
    face = [n for n in xrange(0, NUM_POINTS)]
    return Shape(verts, [face], color)


def Cube(edge, color):
    e2 = edge/2
    verts = [
        (-e2, -e2, -e2),
        (-e2, -e2, +e2),
        (-e2, +e2, -e2),
        (-e2, +e2, +e2),
        (+e2, -e2, -e2),
        (+e2, -e2, +e2),
        (+e2, +e2, -e2),
        (+e2, +e2, +e2),
    ]
    faces = [
        [0, 1, 3, 2], # left
        [4, 6, 7, 5], # right
        [7, 3, 1, 5], # front
        [0, 2, 6, 4], # back
        [3, 7, 6, 2], # top
        [1, 0, 4, 5], # bottom
    ]
    return Shape(verts, faces, color)


def RgbCubeCluster(edge, cluster_edge, cube_count):
    shape = CompositeShape()
    for i in xrange(cube_count):
        r = randint(1, cluster_edge-1)
        g = randint(1, cluster_edge-1)
        b = randint(1, cluster_edge-1)
        color = (
            int(r / cluster_edge * 255),
            int(g / cluster_edge * 255),
            int(b / cluster_edge * 255),
            255)
        pos = [
            r - cluster_edge / 2,
            g - cluster_edge / 2,
            b - cluster_edge / 2,
        ]
        shape.add(Cube(edge, color), Vec3(*pos))
    return shape


def CubeLattice(edge, cluster_edge, freq):
    shape = CompositeShape()
    black = (0, 0, 0, 255)
    for i in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
        for j in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
            shape.add(Cube(edge, black), Vec3(i, j, -cluster_edge/2))
            shape.add(Cube(edge, black), Vec3(i, j, +cluster_edge/2))
            shape.add(Cube(edge, black), Vec3(i, -cluster_edge/2, j))
            shape.add(Cube(edge, black), Vec3(i, +cluster_edge/2, j))
            shape.add(Cube(edge, black), Vec3(-cluster_edge/2, i, j))
            shape.add(Cube(edge, black), Vec3(+cluster_edge/2, i, j))
    return shape


def CubeCross():
    shape = CompositeShape()
    center_color = (150, 150, 150, 255)
    shape.add(Cube(2, center_color))

    outer_color = (170, 170, 170, 255)
    shape.add(Cube(1, outer_color), XAxis)
    shape.add(Cube(1, outer_color), YAxis)
    shape.add(Cube(1, outer_color), ZAxis)
    shape.add(Cube(1, outer_color), -XAxis)
    shape.add(Cube(1, outer_color), -YAxis)
    shape.add(Cube(1, outer_color), -ZAxis)
    return shape


def Tetrahedron(edge, color):
    size = edge / sqrt(2)/2
    return Shape(
        vertices=[
            (+size, +size, +size),
            (-size, -size, +size),
            (-size, +size, -size),
            (+size, -size, -size), 
        ],
        faces=[ [0, 2, 1], [1, 3, 0], [2, 3, 1], [0, 3, 2] ],
        color=color,
    )


