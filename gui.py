import pyglet
from pyglet.gl import glBegin, GL_LINES, glEnd, glVertex2f, glLineWidth
import backtracking
import ac3
import time

input_file = open('input copy.txt', 'r')
lines = input_file.readlines()
lines.insert(0, "800000000003600000070090200050007000000045700000100030001000068008500010090000400")

window = pyglet.window.Window(caption='Sudoku Solver')
icon = pyglet.resource.image('icon.png')
window.set_icon(icon)

w_one_fourth = window.width // 4
h_one_third = window.height // 3

start_button_texture = pyglet.resource.image('image.png')
start_button_sprite = pyglet.sprite.Sprite(start_button_texture,
                                           x=w_one_fourth * 3,
                                           y=h_one_third * 0.25,
                                           )

reset_button_texture = pyglet.resource.image('image.png')
reset_button_sprite = pyglet.sprite.Sprite(reset_button_texture,
                                           x=w_one_fourth * 3,
                                           y=h_one_third * 1.05,
                                           )

sudoku_label = pyglet.text.Label('Sudoku',
                                 font_name='Times New Roman',
                                 font_size=22,
                                 x=w_one_fourth * 3.5,
                                 y=h_one_third * 2.85,
                                 anchor_x='center',
                                 anchor_y='center',
                                 color=(255, 0, 0, 255)
                                 )

start_label = pyglet.text.Label('Start',
                                font_name='Times New Roman',
                                font_size=22,
                                x=w_one_fourth * 3.5,
                                y=h_one_third * 0.45,
                                anchor_x='center',
                                anchor_y='center',
                                color=(0, 200, 0, 255)
                                )

reset_label = pyglet.text.Label('Reset',
                                font_name='Times New Roman',
                                font_size=22,
                                x=w_one_fourth * 3.5,
                                y=h_one_third * 1.25,
                                anchor_x='center',
                                anchor_y='center',
                                color=(0, 200, 0, 255)
                                )
labels = []
start_button_disabled = False

for x in range(1, 10):
    for y in range(1, 10):
        number = " " if lines[0][(x - 1) * 9 + (y - 1)] == "0" else lines[0][(x - 1) * 9 + (y - 1)]
        labels.append(
            pyglet.text.Label(number,
                              font_name='Times New Roman',
                              font_size=22,
                              x=(w_one_fourth * y) // 3 - 25,
                              y=(h_one_third * (10 - x)) // 3 - 25,
                              anchor_x='center',
                              anchor_y='center'
                              )
        )

timeLabelAC3 = pyglet.text.Label(f'AC3 Algorithm\nTaken time: 0s',
                                 font_name='Times New Roman',
                                 font_size=12,
                                 x=w_one_fourth * 3 + 85,
                                 y=h_one_third * 3 - 105,
                                 anchor_x='center',
                                 anchor_y='center',
                                 multiline=True,
                                 width=150
                                 )

timeLabelBacktracking = pyglet.text.Label(f'Backtracking Algorithm\nTaken time: 0s',
                                          font_name='Times New Roman',
                                          font_size=12,
                                          x=w_one_fourth * 3 + 107,
                                          y=h_one_third * 2,
                                          anchor_x='center',
                                          anchor_y='center',
                                          multiline=True,
                                          width=200
                                          )


@window.event
def on_mouse_press(x, y, button, modifiers):
    global start_button_disabled, lines, labels

    if start_button_sprite.x < x < (start_button_sprite.x + start_button_sprite.width):
        if start_button_sprite.y < y < (start_button_sprite.y + start_button_sprite.height):
            if start_button_disabled:
                return
            start_button_sprite.opacity = 128

            start = time.time()
            answer = ac3.main(lines[0])

            timeLabelAC3.text = f'AC3 Algorithm\nTaken time: {(time.time() - start):.4f}s'

            start = time.time()
            answer = backtracking.main(lines[0])[:-1]
            timeLabelBacktracking.text = f'Backtracking Algorithm\nTaken time: {(time.time() - start):.4f}s'

            for i in range(len(answer)):
                if labels[i].text != answer[i]:
                    labels[i].color = (0, 255, 0, 255)
                labels[i].text = answer[i]
                labels[i].draw()

            start_label.color = (255, 0, 0, 255)
            start_button_disabled = True

    if reset_button_sprite.x < x < (reset_button_sprite.x + reset_button_sprite.width):
        if reset_button_sprite.y < y < (reset_button_sprite.y + reset_button_sprite.height):
            lines.pop(0)
            reset_button_sprite.opacity = 128
            i = 0
            for x in range(1, 10):
                for y in range(1, 10):
                    labels[i].text = " " if lines[0][(x - 1) * 9 + (y - 1)] == "0" else lines[0][(x - 1) * 9 + (y - 1)]
                    labels[i].color = (255, 255, 255, 255)
                    labels[i].draw()
                    i += 1

            start_label.color = (0, 200, 0, 255)
            start_button_disabled = False


@window.event
def on_mouse_release(x, y, button, modifiers):
    if start_button_sprite.x < x < (start_button_sprite.x + start_button_sprite.width):
        if start_button_sprite.y < y < (start_button_sprite.y + start_button_sprite.height):
            start_button_sprite.opacity = 255

    if reset_button_sprite.x < x < (reset_button_sprite.x + reset_button_sprite.width):
        if reset_button_sprite.y < y < (reset_button_sprite.y + reset_button_sprite.height):
            reset_button_sprite.opacity = 255


@window.event
def on_draw():
    window.clear()

    start_button_sprite.scale_x = 0.75
    start_button_sprite.scale_y = 0.25
    start_button_sprite.draw()

    reset_button_sprite.scale_x = 0.75
    reset_button_sprite.scale_y = 0.25
    reset_button_sprite.draw()

    timeLabelAC3.draw()
    timeLabelBacktracking.draw()
    start_label.draw()
    reset_label.draw()
    sudoku_label.draw()

    for i in labels:
        i.draw()

    for i in range(1, 10):
        if i % 3 == 0:
            glLineWidth(7)
        else:
            glLineWidth(1)
        glBegin(GL_LINES)
        glVertex2f(0, h_one_third * i // 3)
        glVertex2f(window.width - w_one_fourth, h_one_third * i // 3)
        glEnd()

    for i in range(1, 10):
        if i % 3 == 0:
            glLineWidth(7)
        else:
            glLineWidth(1)
        glBegin(GL_LINES)
        glVertex2f(w_one_fourth * i // 3, 0)
        glVertex2f(w_one_fourth * i // 3, window.height)
        glEnd()


pyglet.app.run()
