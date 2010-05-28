
import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet.window import Window

from .camera import Camera
from .render import Render
from .world import World, populate

class Gameloop(object):

    def __init__(self):
        self.window = None

    def start(self):
        self.world = World()
        self.world.init()
        populate(self.world)

        self.render = Render()
        self.camera = Camera(zoom=10.0)

        self.window = Window(fullscreen=False, visible=False)
        self.window.set_exclusive_mouse(True)
        self.window.on_draw = self.draw
        self.window.on_resize = self.render.resize

        self.render.init()
        pyglet.clock.schedule(self.update)
        self.hud_fps = pyglet.clock.ClockDisplay()

        self.window.set_visible()
        pyglet.app.run()


    def update(self, dt):
        # scale dt such that the 'standard' framerate of 60fps gives dt=1.0
        dt *= 60.0
        # prevent explosion when game is paused then restarted for any reason
        dt = min(dt, 2)
        self.world.update(dt)
        self.window.invalid = True


    def draw(self):
        self.window.clear()
        self.camera.world_projection(self.window.width, self.window.height)
        self.camera.look_at()
        self.render.draw(self.world)
        self.hud_fps.draw()
        return EVENT_HANDLED

    def stop(self):
        if self.window:
            self.window.close()

