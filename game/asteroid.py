# asteroid.py – Classe do asteroide

import pygame
import random
import math
from settings import (
    LARGURA,
    ASTEROIDE_VELOCIDADE_MIN, ASTEROIDE_VELOCIDADE_MAX,
    ASTEROIDE_RAIO_MIN, ASTEROIDE_RAIO_MAX,
    CINZA, BRANCO
)


class Asteroid(pygame.sprite.Sprite):
    """Asteroide que desce verticalmente com forma poligonal aleatória."""

    def __init__(self):
        super().__init__()

        self.raio      = random.randint(ASTEROIDE_RAIO_MIN, ASTEROIDE_RAIO_MAX)
        self.velocidade = random.uniform(ASTEROIDE_VELOCIDADE_MIN, ASTEROIDE_VELOCIDADE_MAX)

        # Gera os pontos do polígono irregular UMA VEZ
        self.pontos_rel = self._gerar_pontos()

        # Surface quadrada que contém o asteroide
        tam = self.raio * 2 + 4
        self.image = pygame.Surface((tam, tam), pygame.SRCALPHA)
        self._desenhar()

        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(self.raio, LARGURA - self.raio)
        self.rect.bottom   = 0  # aparece no topo

    # ── Desenho ──────────────────────────────────────────────────────────────
    def _gerar_pontos(self):
        """Cria vértices de um polígono irregularmente circular."""
        num_pontos = random.randint(7, 12)
        pontos = []
        for i in range(num_pontos):
            angulo   = (2 * math.pi / num_pontos) * i
            variacao = random.uniform(0.55, 1.0)
            r = self.raio * variacao
            x = r * math.cos(angulo)
            y = r * math.sin(angulo)
            pontos.append((x, y))
        return pontos

    def _desenhar(self):
        """Renderiza o polígono na surface."""
        cx = cy = self.raio + 2  # centro da surface
        pts_abs = [(cx + px, cy + py) for px, py in self.pontos_rel]

        # Sombra/corpo
        pygame.draw.polygon(self.image, CINZA, pts_abs)
        # Contorno branco estilo Atari
        pygame.draw.polygon(self.image, BRANCO, pts_abs, 2)

        # Crateras decorativas
        num_crateras = random.randint(2, 4)
        for _ in range(num_crateras):
            cr = random.randint(3, max(4, self.raio // 4))
            cx2 = cx + random.randint(-self.raio // 2, self.raio // 2)
            cy2 = cy + random.randint(-self.raio // 2, self.raio // 2)
            pygame.draw.circle(self.image, (100, 100, 100), (cx2, cy2), cr)
            pygame.draw.circle(self.image, BRANCO, (cx2, cy2), cr, 1)

    # ── Atualização ──────────────────────────────────────────────────────────
    def update(self):
        """Move o asteroide para baixo."""
        self.rect.y += self.velocidade
