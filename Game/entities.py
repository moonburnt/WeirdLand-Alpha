from pygame import mouse, sprite, Surface, display, transform, Rect
from WGF import game, loader, shared
from WGF.tasks import Animation
import logging

log = logging.getLogger(__name__)


class Entity(sprite.Sprite):
    # scale = 0

    def __init__(self):
        super().__init__()
        # print(self.scale)
        # if self.scale:
        #     size = self.image.get_size()
        #     x = size[0] * self.scale
        #     y = size[1] * self.scale
        #     self.image = transform.scale(self.image, (x, y))

        self.rect = self.image.get_rect()


class Enemy(Entity):
    scale: int = 4
    horizontal_speed: int = 4
    # Rotation angle. If not 0, character will start spinning
    # angle: int = 0

    def __init__(self, pos=(100, 450), hp: int = 1):
        # self.image = game.assets.images["enemy"]
        sheet = loader.Spritesheet(game.assets.images["enemy"])
        self.animation = Animation(sheet.get_sprites((32, 32)), scale=self.scale)
        self.image = self.animation[0]
        super().__init__()

        # Make it possible for entity to move around screen-sized area
        self.area = display.get_surface().get_rect()
        # This will set position of creature to spawn on
        self.rect.center = pos

        self.hp = hp
        self.alive = True

    def update(self):
        """Make entity do different things, depending on current status effects"""
        if self.alive:
            self.walk()

    def walk(self):
        """Make entity walk across the screen and turn at its corners"""
        # For now it can only move horizontally
        pos = self.rect.move((self.horizontal_speed, 0))
        # Ensuring new position wouldnt be out of screen's bounds
        # For now, only checks for horizontal "out of bounds" situations
        if not self.area.contains(pos):
            self.horizontal_speed = -self.horizontal_speed
            pos = self.rect.move((self.horizontal_speed, 0))
            # This will flip image horizontally
            self.animation.flip(horizontally=True)
            # self.image = transform.flip(self.image, True, False)

        nxt = self.animation.next()
        if nxt:
            self.image = nxt

        self.rect = pos

    def get_damage(self, amount: int):
        self.hp -= amount
        # #TODO: maybe make it configurable?
        shared.score += 10
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False


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
