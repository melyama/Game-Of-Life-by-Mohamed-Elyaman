import pygame

class Box:

    def __init__(self, width, hieght, position):
        self.hieght = hieght
        self.width = width
        self.position = position

    def to_alive(self):
        print(" ")
