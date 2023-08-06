import pygame as pg
from pygame.mask import Mask
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

from .util import round_pos


class _StaticSprite(Sprite):
    id: int

    image: Surface
    rect: Rect
    mask: Mask

    def __init__(
        self, containers: list[Group], id: int, image: Surface, pos: Vector2
    ) -> None:
        Sprite.__init__(self, *containers)

        self.id = id

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = round_pos(pos)

        self.mask = pg.mask.from_surface(self.image)
