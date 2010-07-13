
import operator


class Event(object):

    def __init__(self):
        self.listeners = []

    def __iadd__(self, listener):
        self.listeners.append(listener)
        return self

    def fire(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)



class World(object):

    clearColor = (0.3, 0.3, 0.3, 1)

    def __init__(self):
        self.items = {}
        self.time = 0.0
        self.add_item = Event()


    def add(self, item):
        self.items[item.id] = item
        self.add_item.fire(item)

        if hasattr(item, 'camera'):
            self.camera = item

    def product(self, *args):
        return reduce(operator.mul, list(*args), 1)


    def _get_rate(self):
        rate = min(
            item.slowmo()
            for item in self.items.itervalues()
            if hasattr(item, 'slowmo'))
        return rate


    def update(self, dt):
        dt *= self._get_rate()
        self.time += dt
        for item in self.items.itervalues():
            if hasattr(item, 'move'):
                item.position = item.move(self.time, dt)
            if hasattr(item, 'spin'):
                item.orientation = item.spin(self.time, dt)

