import numpy as np
import pygame as pg
import random
from modules.layer import Layer

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
WINDOW_OPEN = True
start_x, start_y = 20, 20
size = 20

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("MNIST Digits Prediction Using Neural Network")

network_size = [784, 10, 10]

def get_pixel_values(canvas):
    """Returns a list containing each pixel's brightness, from left to right, top to bottom."""
    values = []
    for row in canvas:
        for pixel in row:
            values.append(pixel.get_brightness())
    return values

def clear_canvas(canvas):
    for row in canvas:
        for pixel in row:
            pixel.set_brightness(0)
            pixel.update()

class Button:
    def __init__(self, x, y, w, h, color):
        self.rect = pg.rect.Rect(x, y, w, h)
        self.color = color
        self.has_been_pressed = False

    def draw(self, surface):
        pg.draw.rect(surface=surface, rect=self.rect, color=self.color)

    def was_clicked(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos):
            self.state = 1
            
            if mouse_pressed:
                self.state = 2      
                self.has_been_pressed = True
            
            elif self.has_been_pressed and not mouse_pressed:
                self.has_been_pressed = False
                return True
            return False
        else:
            self.state = 0
            return False

class Pixel:
    def __init__(self, x_pos, y_pos, size, brightness):
        self.rect = pg.rect.Rect(x_pos, y_pos, size, size)
        self.brightness = brightness
        self.color = (brightness, brightness, brightness)
        self.was_painted = False

    def get_state(self, mouse_pos, mouse_pressed):
        if not mouse_pressed:
            return

        brush_size = 625
        mouse_dist = (mouse_pos[0] - self.rect.centerx) ** 2 + (mouse_pos[1] - self.rect.centery) ** 2
        
        # If the mouse touches the pixel, it is set to white
        if self.rect.collidepoint(*mouse_pos):
            self.brightness = 255
            self.was_painted = True

        # If the pixel's center is close enough, the brightness is set accordingly to the distance from the mouse
        elif mouse_dist < brush_size:
            brightness = max(min(255, int(((brush_size - mouse_dist) / brush_size) * 255)), 0)
            self.brightness = max(self.brightness, brightness)
            self.was_painted = True

        # If the pixel is too far away and hasn't been painted yet it is set to black
        elif not self.was_painted:
            self.brightness = 0
            self.was_painted = False

        self.update()

    def update(self):
        self.color = (self.brightness, self.brightness, self.brightness)

    def draw(self, surface, mouse_pos, mouse_pressed):
        self.get_state(mouse_pos=mouse_pos, mouse_pressed=mouse_pressed)
        pg.draw.rect(surface=surface, rect=self.rect, color=self.color)

    def get_brightness(self):
        return self.brightness / 255

    def set_brightness(self, brightness:int=0):
        """Takes an int between 0 and 255 and sets it as pixels brigtness value."""
        if brightness < 0 or brightness > 255:
            return
        
        self.brightness = int(brightness)

canvas = []
for i in range(28):
    row = []
    for j in range(28):
        brightness = 0
        pixel = Pixel(start_x + size * j, start_y + size * i, size, brightness=brightness)
        row.append(pixel)
    canvas.append(row)

button = Button(600, 500, 100, 70, (0, 125, 0))

while WINDOW_OPEN:

    events = pg.event.get()

    for event in events:
        # Handle closing the window
        if event.type == pg.QUIT:
            WINDOW_OPEN = False

    mouse_pos = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed()[0]

    if button.was_clicked(mouse_pos=mouse_pos, mouse_pressed=mouse_pressed):
        clear_canvas(canvas=canvas)

    # Draw image
    pg.draw.rect(screen, (150, 150, 150), (15, 15, 570, 570), 5)
    for row in canvas:
        for pixel in row:
            pixel.draw(surface=screen, mouse_pos=mouse_pos, mouse_pressed=mouse_pressed)
    button.draw(surface=screen)

    # DEBUG
    # print(f"PIXELS: {sum(get_pixel_values(canvas=canvas)) / 784}")
    # print(f"BUTTON: {button.was_clicked(mouse_pos=mouse_pos, mouse_pressed=mouse_pressed)}")


    pg.display.flip()

pg.quit()