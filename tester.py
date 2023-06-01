from tkinter import *
import math

WIDTH = 400
HEIGHT = 400
CANVAS_MID_X = WIDTH/2
CANVAS_MID_Y = HEIGHT/2
SIDE = WIDTH/4

root = Tk()
canvas = Canvas(root, bg="black", height=HEIGHT, width=WIDTH)
canvas.pack()

vertices = [
    [CANVAS_MID_X - SIDE/10, CANVAS_MID_Y - SIDE/2],
    [CANVAS_MID_X + SIDE/10, CANVAS_MID_Y - SIDE/2],
    [CANVAS_MID_X + SIDE/10, CANVAS_MID_Y + SIDE/2],
    [CANVAS_MID_X - SIDE/10, CANVAS_MID_Y + SIDE/2],
]

def rotate(points, angle, center):
    angle = math.radians(angle)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    cx, cy = center
    new_points = []
    for x_old, y_old in points:
        x_old -= cx
        y_old -= cy
        x_new = x_old * cos_val - y_old * sin_val
        y_new = x_old * sin_val + y_old * cos_val
        new_points.append([x_new + cx, y_new + cy])
    return new_points

def draw_square(points, color="red"):
    canvas.create_polygon(points, fill=color)

def test():
    old_vertices = [[150, 150], [250, 150], [250, 250], [150, 250]]
    print ("vertices: ", vertices, "should be: ", old_vertices)
    print (vertices == old_vertices)

draw_square(vertices, "blue")

center = (CANVAS_MID_X, CANVAS_MID_Y)
new_square = rotate(vertices, 30, center)
test()
draw_square(new_square)

mainloop()
