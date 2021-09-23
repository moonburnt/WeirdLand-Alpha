from pygame import mouse, sprite, Surface, display, transform, Rect
from WGF import game, loader, shared, Point
from WGF.tasks import Animation
from enum import Enum
import logging

log = logging.getLogger(__name__)


class Direction(Enum):
    left: int = -1
    right: int = 1


enemies = {}


def enemy(cls):
    name = cls.__name__
    enemies[name] = cls

    def inner(*args, **kwargs):
        return enemies[name](*args, **kwargs)

    return inner


class Entity(sprite.Sprite):
    def __init__(self, pos: Point):
        super().__init__()
        self.rect = self.image.get_rect()

        self.set_pos(pos)

    def update(self):
        self.set_pos(self.pos)

    def set_pos(self, pos: Point):
        self.pos = pos
        self.rect.x = shared.camera_offset.x + self.pos.x
        self.rect.y = shared.camera_offset.y + self.pos.y


class Creature(Entity):
    def __init__(self, pos: Point, hp: int):
        super().__init__(pos=pos)

        self.hp = hp
        self.alive = True

    def get_damage(self, amount: int):
        self.hp -= amount
        # #TODO: maybe make it configurable?
        shared.score += 10
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False


class Grass(Entity):
    scale: int = 4

    def __init__(self, pos: Point):
        self.image = game.assets.images["grass"]

        if self.scale:
            size = self.image.get_size()
            x = size[0] * self.scale
            y = size[1] * self.scale
            self.image = transform.scale(self.image, (x, y))

        super().__init__(pos=pos)


@enemy
class Dummy(Creature):
    scale: int = 4

    def __init__(self, pos: Point, hp: int = 1):
        self.image = game.assets.images["dummy"]

        if self.scale:
            size = self.image.get_size()
            x = size[0] * self.scale
            y = size[1] * self.scale
            self.image = transform.scale(self.image, (x, y))

        super().__init__(pos=pos, hp=hp)


@enemy
class Walker(Creature):
    scale: int = 4
    horizontal_speed: int = 4

    def __init__(self, pos: Point, hp: int = 1):
        sheet = loader.Spritesheet(game.assets.images["enemy"])
        self.animation = Animation(sheet.get_sprites((32, 32)), scale=self.scale)
        self.image = self.animation[0]
        super().__init__(pos=pos, hp=hp)

        self.direction = Direction.right

    def update(self):
        """Make entity do different things, depending on current status effects"""
        super().update()
        if self.alive:
            self.walk()

    def walk(self):
        """Make entity walk across the screen and turn at its corners"""

        new_x = self.pos.x + self.horizontal_speed * self.direction.value

        if new_x > shared.bg_size.width - 150:
            self.direction = Direction.left
            new_x = self.pos.x + self.horizontal_speed * self.direction.value
            self.animation.flip(horizontally=True)
        elif new_x < 0:
            self.direction = Direction.right
            new_x = self.pos.x + self.horizontal_speed * self.direction.value
            self.animation.flip(horizontally=True)

        self.set_pos(Point(new_x, self.pos.y))

        nxt = self.animation.next()
        if nxt:
            self.image = nxt


# #TODO: rework this into "weapon", make it serve as base for others
class Gun(sprite.Sprite):
    scale: int = 2
    attacking: bool = False

    def __init__(self, damage: int = 1):
        sprites = loader.Spritesheet(game.assets.images["crosshairs"]).get_sprites(
            (16, 16)
        )

        self.sprites = {
            "attack": sprites[1],
            "idle": sprites[0],
        }

        # #TODO: add support for rescaling to get_sprites(), maybe?
        if self.scale:
            size = self.sprites["attack"].get_size()
            x = size[0] * self.scale
            y = size[1] * self.scale
            self.sprites["attack"] = transform.scale(self.sprites["attack"], (x, y))
            self.sprites["idle"] = transform.scale(self.sprites["idle"], (x, y))

        self.image = self.sprites["idle"]

        # I think, this should make hitbox smaller?
        point = 1 * self.scale
        self.rect = Rect(point, point, point, point)
        super().__init__()

        self.hit_sound = game.assets.sounds["hit"]
        self.miss_sound = game.assets.sounds["miss"]

        self.damage = damage

    def update(self):
        self.rect.midtop = mouse.get_pos()

    def attack(self, targets: list) -> bool:
        """Attack target with weapon and check if collision has happend"""
        if self.attacking:
            return False

        self.attacking = True
        hit = False
        for target in targets:
            if self.rect.colliderect(target.rect):
                self.hit_sound.play()
                target.get_damage(self.damage)
                hit = True
        if not hit:
            self.miss_sound.play()

        self.image = self.sprites["attack"]

    def pullback(self):
        self.attacking = False
        self.image = self.sprites["idle"]
