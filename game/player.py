# player.py – Classe da nave do jogador

import pygame
from settings import (
    LARGURA, ALTURA,
    NAVE_VELOCIDADE, NAVE_LARGURA, NAVE_ALTURA,
    COOLDOWN_TIRO, BRANCO, VERDE_NEON, AZUL_ESCURO, AMARELO
)
from projectile import Projectile


class Player(pygame.sprite.Sprite):
    """Nave controlada pelo jogador. Move‑se horizontalmente e atira projéteis."""

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((NAVE_LARGURA, NAVE_ALTURA), pygame.SRCALPHA)
        self._desenhar()

        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA  // 2
        self.rect.bottom   = ALTURA - 20

        self._ultimo_tiro = 0  # timestamp do último disparo

    # ── Desenho ──────────────────────────────────────────────────────────────
    def _desenhar(self):
        """Desenha a nave no estilo vetorial/Atari."""
        w, h = NAVE_LARGURA, NAVE_ALTURA

        # Corpo triangular principal (branco)
        corpo = [
            (w // 2, 0),           # ponta superior (frente)
            (0,      h - 6),       # canto inferior esquerdo
            (w,      h - 6),       # canto inferior direito
        ]
        pygame.draw.polygon(self.image, BRANCO, corpo)
        pygame.draw.polygon(self.image, VERDE_NEON, corpo, 2)

        # Asas laterais
        asa_esq = [(0, h - 6), (w // 4, h // 2), (w // 2 - 2, h - 6)]
        asa_dir = [(w, h - 6), (3 * w // 4, h // 2), (w // 2 + 2, h - 6)]
        pygame.draw.polygon(self.image, AZUL_ESCURO, asa_esq)
        pygame.draw.polygon(self.image, VERDE_NEON, asa_esq, 1)
        pygame.draw.polygon(self.image, AZUL_ESCURO, asa_dir)
        pygame.draw.polygon(self.image, VERDE_NEON, asa_dir, 1)

        # Cockpit (bolha central)
        pygame.draw.ellipse(
            self.image, AMARELO,
            (w // 2 - 5, h // 3, 10, 8)
        )

        # Propulsores (base)
        pygame.draw.rect(self.image, VERDE_NEON, (w // 4, h - 6, w // 2, 4))
        pygame.draw.rect(self.image, AMARELO,    (w // 4 + 4, h - 4, 6, 4))
        pygame.draw.rect(self.image, AMARELO,    (w - w // 4 - 10, h - 4, 6, 4))

    # ── Atualização ──────────────────────────────────────────────────────────
    def update(self, teclas):
        """Processa movimento horizontal com base nas teclas pressionadas."""
        if teclas[pygame.K_LEFT]:
            self.rect.x -= NAVE_VELOCIDADE
        if teclas[pygame.K_RIGHT]:
            self.rect.x += NAVE_VELOCIDADE

        # Impede saída pelas bordas
        self.rect.left  = max(0, self.rect.left)
        self.rect.right = min(LARGURA, self.rect.right)

    # ── Disparo ──────────────────────────────────────────────────────────────
    def atirar(self, grupo_projeteis: pygame.sprite.Group) -> bool:
        """
        Cria um projétil respeitando o cooldown.
        Retorna True se o tiro foi efetuado.
        """
        agora = pygame.time.get_ticks()
        if agora - self._ultimo_tiro >= COOLDOWN_TIRO:
            proj = Projectile(self.rect.centerx, self.rect.top)
            grupo_projeteis.add(proj)
            self._ultimo_tiro = agora
            return True
        return False
