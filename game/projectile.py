# projectile.py – Classe do projétil disparado pela nave

import pygame
from settings import (
    PROJETIL_VELOCIDADE, PROJETIL_LARGURA, PROJETIL_ALTURA,
    VERDE_NEON, AMARELO
)


class Projectile(pygame.sprite.Sprite):
    """Projétil que sobe verticalmente a partir da posição da nave."""

    def __init__(self, x: int, y: int):
        super().__init__()

        # Surface com transparência para desenhar o "laser"
        self.image = pygame.Surface((PROJETIL_LARGURA, PROJETIL_ALTURA), pygame.SRCALPHA)
        self._draw()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom   = y

    # ── Desenho ──────────────────────────────────────────────────────────────
    def _draw(self):
        """Desenha um laser com gradiente de cor."""
        w, h = PROJETIL_LARGURA, PROJETIL_ALTURA
        for i in range(h):
            # A ponta é amarela, a base é verde neon
            ratio  = i / h
            r = int(AMARELO[0] * (1 - ratio) + VERDE_NEON[0] * ratio)
            g = int(AMARELO[1] * (1 - ratio) + VERDE_NEON[1] * ratio)
            b = int(AMARELO[2] * (1 - ratio) + VERDE_NEON[2] * ratio)
            pygame.draw.line(self.image, (r, g, b), (0, i), (w - 1, i))

    # ── Atualização ──────────────────────────────────────────────────────────
    def update(self):
        """Move o projétil para cima e remove se sair da tela."""
        self.rect.y -= PROJETIL_VELOCIDADE
        if self.rect.bottom < 0:
            self.kill()
