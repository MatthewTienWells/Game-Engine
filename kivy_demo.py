import convert_coordinates
from kivy import graphics as gr
from kivy import Widget
from kivy import App
import kivy


class GameWindow(Widget):
    def __init__(self):
        self.polygons = []

    def update_canvas(self):
        self.canvas.clear()
        for polygon in self.polygons:
            Color(*polygon['color'])
            Line(points=*polygon['points'], width=polygon['width'])


class KIVY_DEMOApp():
    def __init__(self, *args, **kwargs):
        App.__init__(self, *args, **kwargs)

    def on_start(self):
        self.appl = kivy.get_running_app()

    def add_cube(self, center, size, colors):
        game_window = self.appl.root_window.children[-1]
        bottom = [
            (center+size, center+size, center-size),
            (center+size, center-size, center-size),
            (center-size, center+size, center-size),
            (center-size, center-size, center-size)
            ]
        top = [
            (center+size, center+size, center+size),
            (center+size, center-size, center+size),
            (center-size, center+size, center+size),
            (center-size, center-size, center+size)
            ]
        left = [
            (center-size, center+size, center+size),
            (center-size, center-size, center+size),
            (center-size, center+size, center-size),
            (center-size, center-size, center-size)
            ]
        right = [
            (center+size, center+size, center+size),
            (center+size, center-size, center+size),
            (center+size, center+size, center-size),
            (center+size, center-size, center-size)
            ]
        front = [
            (center+size, center-size, center+size),
            (center-size, center-size, center+size),
            (center+size, center-size, center-size),
            (center-size, center-size, center-size)
            ]
        back = [
            (center+size, center+size, center+size),
            (center-size, center+size, center+size),
            (center+size, center+size, center-size),
            (center-size, center+size, center-size)
            ]
        color = 0
        for side in (bottom, top, left, right, front, back):
            points = [
                convert_coordinates.plane_point(side[0]),
                convert_coordinates.plane_point(side[1]),
                convert_coordinates.plane_point(side[2]),
                convert_coordinates.plane_point(side[3]),
                ]
            drawing = {'points' = points, 'color'=colors[color], 'width'=10}
            game_window.polygons.append(drawing)
            color += 1
        game_window.update_canvas()
