from pygame import Surface, transform, Rect
from WGF import game, loader, shared, Point
from WGF.nodes import VisualNode, Cursor
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


class Creature(VisualNode):
    def __init__(
        self,
        name: str,
        surface,
        hitbox: Rect,
        pos: Point,
        hp: int,
        distance: float = 1.0,
        score: int = 10,
    ):
        super().__init__(name=name, surface=surface, pos=pos, distance=distance)

        self.hp = hp
        self.alive = True
        # This reffers to reward granted to player for killing creature
        self.score = score
        # I could make hitboxes more preciese with masks, but I wont do that for
        # now, since animations would need to update these each frame
        self.hitbox = hitbox

    def _updatemethod(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery

    def get_damage(self, amount: int):
        self.hp -= amount
        shared.score += self.score
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False
        shared.kill_counter += 1
        self.hide()


class Grass(VisualNode):
    def __init__(self, pos: Point, bg: bool = False):
        if bg:
            image = game.assets.images["grass_bg"]
            distance = 0.9
        else:
            image = game.assets.images["grass"]
            distance = 1

        super().__init__(
            name="grass",
            surface=image,
            pos=pos,
            distance=distance,
        )


class Mountains(VisualNode):
    def __init__(self, pos: Point):
        super().__init__(
            name="mountains",
            surface=game.assets.images["mountains"],
            pos=pos,
            distance=0.3,
        )


@enemy
class Dummy(Creature):
    def __init__(self, pos: Point, hp: int = 1):
        super().__init__(
            name="dummy",
            surface=game.assets.images["dummy"],
            hitbox=Rect(80, 80, 80, 80),
            pos=pos,
            hp=hp,
            score=5,
        )


class MovingEnemy(Creature):
    horizontal_speed: int = 1

    def __init__(self, name: str, pos: Point, hp: int = 1):
        if not name in game.assets.spritesheets:
            sheet = loader.Spritesheet(game.assets.images[name])
            side = 32 * shared.sprite_scale
            game.assets.spritesheets[name] = sheet.get_sprites((side, side))
        self.animation = Animation(game.assets.spritesheets[name])

        super().__init__(
            name=name,
            surface=self.animation[0],
            hitbox=Rect(80, 80, 80, 80),
            pos=pos,
            hp=hp,
            score=10,
        )

        self.direction = Direction.right

    def _updatemethod(self):
        if self.alive:
            self.walk()

    def walk(self):
        """Make entity walk across the screen and turn at its corners"""

        new_x = self.pos.x + self.horizontal_speed * self.direction.value

        if new_x > shared.bg_size.width:
            self.direction = Direction.left
            new_x = self.pos.x + self.horizontal_speed * self.direction.value
            self.animation.flip(horizontally=True)
        elif new_x < 0:
            self.direction = Direction.right
            new_x = self.pos.x + self.horizontal_speed * self.direction.value
            self.animation.flip(horizontally=True)

        self.pos = Point(new_x, self.pos.y)

        nxt = self.animation.update()
        if nxt:
            self.surface = nxt

        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery


@enemy
class Walker(MovingEnemy):
    horizontal_speed: int = 4

    def __init__(self, pos: Point):
        super().__init__(
            name="walker",
            pos=pos,
        )


@enemy
class Bat(MovingEnemy):
    horizontal_speed: int = 6

    def __init__(self, pos: Point):
        # Not the best way to handle different spawn heights, but will do for now
        # #TODO
        pos.y -= 400

        super().__init__(
            name="bat",
            pos=pos,
        )


# Its has weird naming, coz I wanted actual weapon to inherit from it
class MousePointer(Cursor):
    attacking: bool = False

    def __init__(self):
        if not "crosshairs" in game.assets.spritesheets:
            side = 16 * shared.extra_scale
            game.assets.spritesheets["crosshairs"] = loader.Spritesheet(
                game.assets.images["crosshairs"]
            ).get_sprites((side, side))
        sprites = game.assets.spritesheets["crosshairs"]

        self.sprites = {
            "attack": sprites[1],
            "idle": sprites[0],
        }

        image = self.sprites["idle"]

        super().__init__(name="gun", surface=image)

        self.hit_sound = game.assets.sounds["hit"]
        self.miss_sound = game.assets.sounds["miss"]

        self.hitbox = Rect(1, 1, 1, 1)

    def _updatemethod(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery

    def attack(self, targets: list):
        """Attack target with weapon and check if collision has happend"""
        if self.attacking:
            return False

        self.attacking = True
        hit = False
        for target in targets:
            if self.hitbox.colliderect(target.rect):
                self.hit_sound.play()
                target.on_click()
                hit = True
                break
        if not hit:
            self.miss_sound.play()

        self.surface = self.sprites["attack"]

    def pullback(self):
        self.attacking = False
        self.surface = self.sprites["idle"]


class Gun(MousePointer):
    def __init__(self, damage: int = 1):
        super().__init__()
        self.damage = damage

    def attack(self, targets: list):
        """Attack target with weapon and check if collision has happend"""
        if self.attacking:
            return False

        self.attacking = True
        hit = False
        # Its reversed coz newer entities appear under older, so their hitbox
        # will count for hit first
        for target in reversed(targets):
            if self.hitbox.colliderect(target.hitbox):
                self.hit_sound.play()
                target.get_damage(self.damage)
                hit = True
                # #TODO: make this break configurable, to allow some weapons to
                # pierce enemies
                break
        if not hit:
            self.miss_sound.play()

        self.surface = self.sprites["attack"]
