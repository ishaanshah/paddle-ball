import config

from object import Object


class Boss():
    def __init__(self, x, y, screen):
        self.x = x - 10
        self.y = y - 1
        self.width = 20
        self.height = 3
        self.top_layer = Object(x-7, y-1, 14, 1, config.boss["color"], screen)
        self.mid_layer = Object(x-10, y, 20, 1, config.boss["color"], screen)
        self.bot_layer = Object(x-3, y+1, 6, 1, config.boss["color"], screen)
        self.health = 100

    def update(self):
        self.top_layer.update()
        self.mid_layer.update()
        self.bot_layer.update()

    def move(self, x):
        self.x = x - 10
        self.top_layer.x = x - 7
        self.mid_layer.x = x - 10
        self.bot_layer.x = x - 3

    def hit_boss(self):
        self.health -= 10
