# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 17:51:28 2020

@author: noahc
"""
import numpy as np
import math


class Node:
    def __init__(self, coordinates):
        self.coordinates = np.array(coordinates)


class Edge:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop


class Wireframe:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_nodes(self, nodelist):
        for node in nodelist:
            if isinstance(node, Node):
                self.nodes.append(node)
            else:
                self.nodes.append(Node(node))

    def add_edges(self, edgelist):
        for edge in edgelist:
            if isinstance(edge, Edge):
                self.edges.append(edge)

    def print_nodes(self):
        print('\n --- Nodes --- ')
        for i, node in enumerate(self.nodes):
            print('{}: ({}, {}, {})'.format(i, *node.coordinates))

    def print_edges(self):
        print('\n --- Edges --- ')
        for i, edge in enumerate(self.edges):
            print('\n{}: ({}, {}, {})'.format(i, *edge.start.coordinates))
            print('to ({}, {}, {})'.format(*edge.stop.coordinates))

    def find_center(self):
        return np.average(np.array([i.coordinates for i in self.nodes]),
                          axis=0)

    def rotate_z(self, radians):
        point = self.find_center()
        for node in self.nodes:
            x = node.coordinates[0] - point[0]
            y = node.coordinates[1] - point[1]
            r = math.hypot(y, x)
            theta = math.atan2(y, x) + radians
            node.coordinates[0] = point[0] + r * math.cos(theta)
            node.coordinates[1] = point[1] + r * math.sin(theta)

    def rotate_x(self, radians):
        point = self.find_center()
        for node in self.nodes:
            z = node.coordinates[2] - point[2]
            y = node.coordinates[1] - point[1]
            r = math.hypot(y, z)
            theta = math.atan2(y, z) + radians
            node.coordinates[2] = point[2] + r * math.cos(theta)
            node.coordinates[1] = point[1] + r * math.sin(theta)

    def rotate_y(self, radians):
        point = self.find_center()
        for node in self.nodes:
            x = node.coordinates[0] - point[0]
            z = node.coordinates[2] - point[2]
            r = math.hypot(z, x)
            theta = math.atan2(x, z) + radians
            node.coordinates[0] = point[0] + r * math.sin(theta)
            node.coordinates[2] = point[2] + r * math.cos(theta)

    def translate(self, dx=0, dy=0, dz=0):
        for node in self.nodes:
            node.coordinates += np.array([dx, dy, dz])

    def scale(self, factor):
        center = self.find_center()
        for node in self.nodes:
            node.coordinates = center + factor * (node.coordinates - center)


def make_cube(side_length):
    """ Returns a wireframe object in the shape of a cube.
    """
    def hypote(a, b):
        a = np.array(a)
        b = np.array(b)
        return np.sqrt(np.sum((a - b) ** 2, axis=0))

    cube_nodes = [(x, y, z) for x in (0, side_length) for y in (0, side_length)
                  for z in (0, side_length)]
    cube = Wireframe()
    cube.add_nodes(cube_nodes)
    edge_list = []
    for i, node in enumerate(cube.nodes):
        for node2 in cube.nodes[i+1:]:
            current_distance = hypote(node.coordinates, node2.coordinates)
            if current_distance == side_length:
                edge_list.append(Edge(node, node2))
    cube.add_edges(edge_list)
    return cube


def make_custom():
    nodes = input("How many nodes?")
    node_list = []
    for i, node in enumerate(range(int(nodes))):
        node_list.append(Node(np.array([
            input("Node {} x : ".format(i+1)),
            input("Node {} y : ".format(i+1)),
            input("Node {} z : ".format(i+1))
        ])))
    custom = Wireframe()
    custom.add_nodes(node_list)
    return custom
