# main.py – Loop principal do jogo Space Shooter

import sys
import random
import pygame

from settings import (
    LARGURA, ALTURA, FPS, TITULO,
    PRETO, BRANCO, VERDE_NEON, VERMELHO, AMARELO, AZUL_ESCURO,
    INTERVALO_SPAWN, SPAWN_MINIMO, PONTOS_POR_ASTEROIDE
)
from player    import Player
from asteroid  import Asteroid
from projectile import Projectile


# ── Funções auxiliares ────────────────────────────────────────────────────────

def desenhar_estrelas(surface, estrelas):
    """Renderiza o fundo estrelado com brilho sutil."""
    for (x, y, brilho) in estrelas:
        cor = (brilho, brilho, brilho)
        pygame.draw.circle(surface, cor, (x, y), 1)


def gerar_estrelas(n=120):
    """Gera posições e brilho aleatórios para as estrelas do fundo."""
    return [
        (random.randint(0, LARGURA),
         random.randint(0, ALTURA),
         random.randint(60, 200))
        for _ in range(n)
    ]


def desenhar_texto(surface, texto, tamanho, cor, x, y, centralizado=False):
    """Utilitário para renderizar texto na tela."""
    fonte = pygame.font.SysFont("Courier New", tamanho, bold=True)
    img   = fonte.render(texto, True, cor)
    rect  = img.get_rect()
    if centralizado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)


def tela_game_over(surface, relogio, pontuacao):
    """Exibe a tela de Game Over e aguarda o jogador reiniciar ou sair."""
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    desenhar_texto(surface, "GAME OVER", 64, VERMELHO,
                   LARGURA // 2, ALTURA // 2 - 80, centralizado=True)
    desenhar_texto(surface, f"PONTUAÇÃO FINAL: {pontuacao}", 30, AMARELO,
                   LARGURA // 2, ALTURA // 2, centralizado=True)
    desenhar_texto(surface, "Pressione R para reiniciar", 22, BRANCO,
                   LARGURA // 2, ALTURA // 2 + 60, centralizado=True)
    desenhar_texto(surface, "Pressione ESC para sair", 22, BRANCO,
                   LARGURA // 2, ALTURA // 2 + 90, centralizado=True)

    pygame.display.flip()

    # Aguarda input
    while True:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True   # reiniciar
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def desenhar_hud(surface, pontuacao, nivel):
    """Desenha a pontuação e o nível no canto superior esquerdo."""
    desenhar_texto(surface, f"SCORE: {pontuacao:06d}", 22, VERDE_NEON, 12, 12)
    desenhar_texto(surface, f"NÍVEL: {nivel}", 18, AMARELO, 12, 38)


def desenhar_borda(surface):
    """Borda luminosa ao redor da tela (estilo arcade)."""
    pygame.draw.rect(surface, VERDE_NEON, (0, 0, LARGURA, ALTURA), 2)


# ── Loop de jogo ──────────────────────────────────────────────────────────────

def iniciar_jogo(tela):
    """Reinicia e executa um ciclo completo de jogo."""

    # Grupos de sprites
    grupo_todos      = pygame.sprite.Group()
    grupo_asteroides = pygame.sprite.Group()
    grupo_projeteis  = pygame.sprite.Group()

    nave = Player()
    grupo_todos.add(nave)

    pontuacao        = 0
    nivel            = 1
    intervalo_spawn  = INTERVALO_SPAWN
    tempo_ultimo_spawn = pygame.time.get_ticks()

    estrelas = gerar_estrelas()

    rodando = True
    clock   = pygame.time.Clock()

    while rodando:
        clock.tick(FPS)
        agora = pygame.time.get_ticks()

        # ── Eventos ──────────────────────────────────────────────────────────
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # ── Entrada do teclado ───────────────────────────────────────────────
        teclas = pygame.key.get_pressed()
        nave.update(teclas)

        if teclas[pygame.K_SPACE]:
            nave.atirar(grupo_projeteis)
            grupo_todos.add(*grupo_projeteis)   # adiciona novos projéteis ao grupo geral

        # ── Spawn de asteroides ──────────────────────────────────────────────
        if agora - tempo_ultimo_spawn > intervalo_spawn:
            asteroide = Asteroid()
            grupo_asteroides.add(asteroide)
            grupo_todos.add(asteroide)
            tempo_ultimo_spawn = agora

            # Dificuldade progressiva: a cada 200 pontos reduz o intervalo
            nivel = 1 + pontuacao // 200
            intervalo_spawn = max(SPAWN_MINIMO, INTERVALO_SPAWN - (nivel - 1) * 80)

        # ── Atualização ──────────────────────────────────────────────────────
        grupo_projeteis.update()
        grupo_asteroides.update()

        # ── Colisões: projétil × asteroide ───────────────────────────────────
        acertos = pygame.sprite.groupcollide(
            grupo_asteroides, grupo_projeteis,
            True, True          # remove ambos ao colidir
        )
        for asteroide in acertos:
            pontuacao += PONTOS_POR_ASTEROIDE

        # ── Colisão: nave × asteroide ─────────────────────────────────────────
        if pygame.sprite.spritecollide(nave, grupo_asteroides, False,
                                       pygame.sprite.collide_circle):
            rodando = False
            break

        # ── Asteroide fora da tela (fundo) ───────────────────────────────────
        for ast in list(grupo_asteroides):
            if ast.rect.top > ALTURA:
                rodando = False
                break

        # ── Desenho ──────────────────────────────────────────────────────────
        tela.fill(AZUL_ESCURO)
        desenhar_estrelas(tela, estrelas)
        desenhar_borda(tela)
        grupo_todos.draw(tela)
        desenhar_hud(tela, pontuacao, nivel)

        pygame.display.flip()

    return pontuacao


# ── Ponto de entrada ──────────────────────────────────────────────────────────

def main():
    pygame.init()
    pygame.display.set_caption(TITULO)

    tela    = pygame.display.set_mode((LARGURA, ALTURA))
    relogio = pygame.time.Clock()

    # Tela de introdução
    tela.fill(AZUL_ESCURO)
    estrelas_intro = gerar_estrelas()
    desenhar_estrelas(tela, estrelas_intro)
    pygame.draw.rect(tela, VERDE_NEON, (0, 0, LARGURA, ALTURA), 2)
    desenhar_texto(tela, "SPACE SHOOTER", 56, VERDE_NEON,
                   LARGURA // 2, ALTURA // 2 - 80, centralizado=True)
    desenhar_texto(tela, "← → para mover  |  ESPAÇO para atirar", 20, BRANCO,
                   LARGURA // 2, ALTURA // 2, centralizado=True)
    desenhar_texto(tela, "Pressione qualquer tecla para começar", 20, AMARELO,
                   LARGURA // 2, ALTURA // 2 + 40, centralizado=True)
    desenhar_texto(tela, "ESC para sair", 16, (130, 130, 130),
                   LARGURA // 2, ALTURA // 2 + 75, centralizado=True)
    pygame.display.flip()

    # Aguarda início
    esperando = True
    while esperando:
        relogio.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                esperando = False

    # Loop principal com suporte a reinício
    while True:
        pontuacao = iniciar_jogo(tela)
        reiniciar = tela_game_over(tela, relogio, pontuacao)
        if not reiniciar:
            break


if __name__ == "__main__":
    main()
