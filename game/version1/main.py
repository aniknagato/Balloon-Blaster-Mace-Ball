import pyglet
import resources
import random
import math
from pyglet.window import key

score = 0
game_window = pyglet.window.Window()
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()
ast_img = pyglet.resource.image("player.png")

def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

class PhysicalObject(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)
        self.dead = False
        self.velocity_x, self.velocity_y = 0.0, 0.0

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def collides_with(self, other_object):
        collision_distance = self.image.width/2 + other_object.image.width/2
        actual_distance = distance(self.position, other_object.position)
        return (actual_distance <= collision_distance)
    
    def handle_collision_with(self, other_object):
        self.dead = True
        global score
        score += 1

class Asteroid(PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(Asteroid, self).__init__(*args, **kwargs)

def asteroids(num_asteroids, player_position):
    asteroids = []
    for i in range(num_asteroids):
        asteroid_x, asteroid_y = player_position
        while distance((asteroid_x, asteroid_y), player_position) < 10:
            asteroid_x = random.randint(0, 800)
            asteroid_y = random.randint(0, 600)
        
        new_asteroid = Asteroid(img=ast_img, x=asteroid_x, y=asteroid_y)
        new_asteroid.rotation = random.randint(0, 360)
        new_asteroid.velocity_x = random.random()*100 - 50
        new_asteroid.velocity_y = random.random()*100 - 50
        new_asteroid.rotation = random.randint(0, 360)
        asteroids.append(new_asteroid)
    return asteroids

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


player_image = pyglet.resource.image("ship.png")
bullet_image = pyglet.resource.image("player.png")
asteroid_image = pyglet.resource.image("player.png")
score_label = pyglet.text.Label(text="Score: {}".format(score), x=10, y=460)
level_label = pyglet.text.Label(text="Balloon Blaster Mace Ball",
    x=game_window.width//2, y=460, anchor_x='center')
center_image(player_image)
player_ship = pyglet.sprite.Sprite(img=player_image, x=400, y=300)
asteroids = asteroids(20, player_ship.position)



class Player(PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(Player,self).__init__(*args, **kwargs)
        self.keys = dict(left=False, right=False, up=False, down = False)
        self.rotate_speed = 200.0
        self.velocity_x = 0
        self.velocity_y = self.velocity_x

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = True
        elif symbol == key.LEFT:
            self.keys['left'] = True
        elif symbol == key.RIGHT:
            self.keys['right'] = True
        elif symbol == key.DOWN:
            self.keys['down'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = False
        elif symbol == key.LEFT:
            self.keys['left'] = False
        elif symbol == key.RIGHT:
            self.keys['right'] = False
        elif symbol == key.DOWN:
            self.keys['down'] = False
    
    def update(self, dt):
        super(Player, self).update(dt)
        if self.keys['left']:
            self.x -= 100 * dt
        if self.keys['right']:
            self.x += 100 * dt
        if self.keys['up']:
            self.y += 100 * dt
        if self.keys['down']:
            self.y -= 100 * dt

player = Player(img=player_image, x=400, y=300)
game_objects = asteroids + [player]

def update(dt):
    for obj in game_objects:
        obj.update(dt)
    
    player = game_objects[-1]
    baloons = game_objects[0:-1]

    score_label.text = "Score: {}".format(score)

    for b in baloons:

        if not b.dead and b.collides_with(player):
            b.handle_collision_with(player)
    for to_remove in [obj for obj in game_objects if obj.dead]:
        to_remove.delete()
        game_objects.remove(to_remove)


@game_window.event
def on_draw():
    game_window.clear()
    level_label.draw()
    score_label.draw()
    player.draw()
    for asteroid in asteroids:
        if not asteroid.dead:
            asteroid.draw()
game_window.push_handlers(player)
pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()
